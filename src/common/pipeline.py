from metaflow import FlowSpec
from common.logger import get_project_logger
from pathlib import Path
import logging

class Pipeline(FlowSpec):
    """
    Base class for all Metaflow pipelines in this project.

    Provides common configuration, helper methods,
    and a consistent entrypoint for all flows.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Example: set up shared paths, logging, etc.
        # self.data_dir = Path("data")
        # self.logger = get_project_logger()
        # ---------------------------------------------------------------------
        # Logging setup
        # ---------------------------------------------------------------------
        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

        # ---------------------------------------------------------------------
        # Common project paths
        # ---------------------------------------------------------------------
        # Root directory (one level up from where flows typically live)
        self.project_root = Path(__file__).resolve().parents[2]
        self.data_dir = self.project_root / "data"
        self.data_dir.mkdir(exist_ok=True)

    # -------------------------------------------------------------------------
    # Optional helper methods
    # -------------------------------------------------------------------------
    def save_dataframe(self, df, filename: str, **to_csv_kwargs) -> Path:
        """
        Save a pandas DataFrame to the project's data directory.

        Returns the Path of the saved file.
        """
        out_path = self.data_dir / filename
        df.to_csv(out_path, index=False, **to_csv_kwargs)
        self.logger.info("Saved DataFrame to %s", out_path)
        return out_path

    def load_dataframe(self, filename: str, **read_csv_kwargs):
        """
        Load a pandas DataFrame from the project's data directory.
        """
        import pandas as pd

        path = self.data_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Data file not found: {path}")
        self.logger.info("Loaded DataFrame from %s", path)
        return pd.read_csv(path, **read_csv_kwargs)