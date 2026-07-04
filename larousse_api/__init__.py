"""Python package for the Larousse API scraper."""

from larousse_api.larousse import Larousse, LarousseError

NAME = "larousse_api"
__version__ = "0.1.0"
__all__ = ["Larousse", "LarousseError", "NAME"]
