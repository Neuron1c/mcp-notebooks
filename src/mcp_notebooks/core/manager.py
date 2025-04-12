from uuid import uuid4
from typing import Dict
from mcp_notebooks.core.kernel import KernelSession
from mcp_notebooks.core.exceptions import SessionNotFoundError, KernelCreationError


class SessionManager:
    """
    Glorified dict to manage kernel sessions.
    Each session is identified by a unique ID (UUID).
    Use session ID to access your kernel session.

    Please don't lose your session ID.
    """

    def __init__(self):
        self.sessions: Dict[str, KernelSession] = {}

    def create_session(self) -> str:
        try:
            kernel = KernelSession()
        except Exception as e:
            raise KernelCreationError("Failed to create a kernel session") from e

        session_id = str(uuid4())

        self.sessions[session_id] = kernel
        return session_id

    def get_session(self, session_id: str) -> KernelSession:
        session = self.sessions.get(session_id)
        if session is None:
            raise SessionNotFoundError(f"Session ID {session_id} not found.")
        return session

    def delete_session(self, session_id: str) -> str:
        session = self.sessions.get(session_id)
        if session is None:
            raise SessionNotFoundError(f"Session ID {session_id} not found.")
        return session.stop()
