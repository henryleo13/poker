from pathlib import Path

import markdown
from google.adkagents import LlmAgent, SequentialAgent
from google.adkagents.models.lite_llm import LiteLLM
from google.adk.tools.tool_context import ToolContext
from langchain_community.vectorstores import FAISS

from common.embeddings import CustomEmbeddingModel

from .prompts import RETRIEVER_INSTRUCTIONS

EMBEDDING_MODEL = "gemini/text-embedding-004"


def retrieve(tool_context: ToolContext, question: str) -> list[dict[str, str]]:
    """ Retrieve documentation and reference materials to answer the question."""
    # Let's start by initializing embedding model we want to use.
    custom_embedding_model = CustomEmbeddingModel(model=EMBEDDING_MODEL)

    # We need to define the path where the vetor store is located. To ensure the
    # code works regardless of where it's run from, we will use a path relative to
    # the location of this file.
    index_path = (
        Path(__file__).resolve().parents[3] / "data" / "index" / EMBEDDING_MODEL
    )

    # Now, we can load the vector store from disk, This vector store was created
    # by running the Indexing pipeline.
    vector_store = FAISS.load_local(
        str(index_path),
        custom_embedding_model,
        allow_dangerous_deserialization=True,   
    )

    # Finally, we can run a similarity search to find the most relevant documents
    # related to the supplied question.
    results = vector_store.similarity_search(
        question,
        k=4,
    )

    return [
        {
            "file":result.metadata["file"],
            "content": result.page_content,
        }
        for result in results
    ]

def markdown_to_html(tool_context: ToolContext, text: str) -> str:
    """ Convert the supplied markdown text to html."""
    # 53:54 in video
    pass

def base_agent(model: str = "gemini/gemini-2.5-flash"):
    """ Create the Retrieval-Augmented Generation (RAG) agent."""
    retriever_agent = LlmAgent(
        model = LiteLLM(model=model),
        name="retriever",
        description="Answers user questions by about poker",
        instruction=RETRIEVER_INSTRUCTIONS,
        tools=[retrieve],
        output_key="answer",
    )

    return retriever_agent()

root_agent = base_agent()