class KernelCreationError(Exception):
    """Raised when a kernel session fails to initialize."""


class SessionNotFoundError(Exception):
    """Raised when an invalid or expired session ID is used."""
