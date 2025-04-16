from uuid import uuid4
from typing import Dict
from mcp_notebooks.core.kernel import KernelSession
from mcp_notebooks.core.exceptions import SessionNotFoundError, KernelCreationError
import asyncio
import logging

logger = logging.getLogger(__name__)


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
        nb_string = session.stop()
        del self.sessions[session_id]
        return nb_string

    async def cleanup(self, force: bool = False) -> None:
        while True:
            to_delete = []

            for session_id, session in self.sessions.items():
                if session.is_active() and not force:
                    pass
                else:
                    logger.warning(
                        f"Session {session_id} is no longer active, deleting..."
                    )
                    to_delete.append(session_id)

            for session_id in to_delete:
                self.delete_session(session_id)

            if force:
                break
            await asyncio.sleep(10)
