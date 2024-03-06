import importlib.metadata as importlib_metadata

__version__ = importlib_metadata.version(__name__)
__user_agent__ = f"OCRDownloader/{__version__}"
