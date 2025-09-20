import hashlib
from pathlib import Path

import pandas as pd
from metaflow import Parameter, step

from common.embeddings import CustomEmbeddingModel
from common.pipeline import Pipeline

class Indexing(Pipeline):
    """A Metaflow pipline used for indexing the documentation of the project.

    This pipeline implements the necessary steps to load, process, and index
    the documentation of the project.
    """

    location = Parameter(
        "location",
        help="The location of the documentation files.",
        default=".guides/fixed_transcripts/"
    )

    embedding_model = Parameter(
        "embedding-model",
        help="The model to use for generating embeddings.",
        default="gemeni/text-embedding-004"
    )

    @step
    def start(self):
        """Load documentation from local directory."""
        directory = Path(self.location)

        if not directory.exists():
            msg = f"Directory not found: {directory}"
            raise FileNotFoundError(msg)

        files: list[dict[str, str]] = []

        # Let's list every file in the documentation directory and filter
        # by file type before processing them.
        for f in directory.rglob("*"):
            text = f.read_text(encoding="utf-8")

            relative_path = f.relative_to(directory)
            parts = relative_path.parts
            section = parts[0] if len(parts) > 1 else ""

            file.append(
                {
                    "file": str(relative_path),
                    "content": text,
                    "section": section,
                    "type": "markdown" if f.suffix == ".md" else "python",
                }
            )

        files.sort(key=lambda r: r["file"])
        self.data = pd.DataFrame(files, columns=list(files[0].keys()))

        self.logger.info("Number of files: %d", len(self.data))

        self.next(self.prepare_documents)

    @step
    def prepare_documents(self):
        """Prepare the documents taht we'll add to the vector store."""
        from langchain_core.documents import Document

        # Let's go through every entry in the DataFrame and create a Document object
        # with the content of the file and the corresponding metadata.
        self.documents = [
            Document(
                page_content = d.content,
                metadata = {"file":d.file, "section": d.section, "type": d.type),}
            )
            for d in self.data.itertuples(index=False)
        ]

        # To index the documents in the vector store, we neded to generate unique
        # identifiers for each document. We can use the file path for this purpose
        # to ensure these identifiers are consistent across different runs.
        self.ids = [
            hashlib.sha256(f.encode("utf-8")).hexdigest()
            for f in self.data["file"].tolist()
        ]

        self.logger.info("Documents prepared: %d", len(self.documents))

        self.next(self.setup_embedding_model)

    @step
    def setup_embedding_model(self):
        """Initialize the embedding model we'll use to generate embeddings."""
        self.logger.info("Embedding model: %s", self.embedding_model)

        # We'll use custom embedding model to generate embeddings
        # using LiteLLM
        self.custom_embedding_model = CustomEmbeddingModel(self.embedding_model)

        #Since we don't know beforehand which embedding model we'll be using,
        # let's infer the dimensions by generating an embedding and checking
        # it's length.
        self.embedding_dimensions = len(
            self.custom_embedding_model.embed_query("dimensions")
        )
        