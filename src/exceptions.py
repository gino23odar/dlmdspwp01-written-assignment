# Custom exceptions used by the assignment application


class DataLoadError(Exception):
    """Raised when an input dataset cannot be loaded."""


class DataValidationError(Exception):
    """Raised when an input dataset has an invalid structure."""


class MappingError(Exception):
    """Raised when test data cannot be mapped correctly."""