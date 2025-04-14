"""
Kernel handler for managing Jupyter kernel sessions.
"""

import json
from jupyter_client.manager import KernelManager
from mcp_notebooks.models.schema import ExecuteResponse
from mcp_notebooks.core.util import convert_message_to_output


class KernelSession:
    def __init__(self):
        """
        Start a new Jupyter kernel session and initialize notebook history.
        """
        self.km = KernelManager()
        self.km.start_kernel()
        self.kc = self.km.client()
        self.kc.start_channels()

        self.nb_hist = {"cells": []}
        self.executions = 0

    def getID(self) -> str:
        """
        Get the kernel ID.
        """
        return self.km.kernel_id

    def get_notebook(self) -> str:
        """
        Get the notebook history as a JSON string.
        """
        return json.dumps(self.nb_hist, indent=2)

    def stop(self) -> str:
        """
        Shut down the kernel session and return the accumulated notebook (as a JSON string).
        The JSON includes each cell with its code and outputs (converted to nbformat-compliant structures),
        so you can manually save the string to a .ipynb file and view it in Jupyter Notebook.
        """

        nb = {
            "cells": self.nb_hist["cells"],
            "metadata": {
                "language_info": {"name": "python", "version": "3.x"},
                "orig_nbformat": 4,
            },
            "nbformat": 4,
            "nbformat_minor": 2,
        }

        nb_string = json.dumps(nb, indent=2)
        self.km.shutdown_kernel(now=True)

        return nb_string

    def execute(self, snippet: str) -> ExecuteResponse:
        """
        Execute a code snippet in an active kernel session and capture its output.
        The cell—including the code, nbformat-compliant outputs, and execution count—is appended to the
        notebook history.
        """

        self.kc.execute(snippet)
        outputs = []

        # TODO: Take a second look at this
        try:
            # Retrieve messages until the kernel goes back to idle.
            while True:
                msg = self.kc.get_iopub_msg(timeout=10)
                msg_type = msg["header"]["msg_type"]
                content = msg["content"]

                if msg_type in ("stream", "execute_result", "display_data", "error"):
                    output = convert_message_to_output(msg)
                    outputs.append(output)
                elif msg_type == "status" and content.get("execution_state") == "idle":
                    break
        except Exception as e:
            raise KernelException(f"Error retrieving output: {e}")

        # Build an nbformat-compliant cell.
        cell = {
            "cell_type": "code",
            "execution_count": self.executions,
            "metadata": {},
            "outputs": outputs,
            "source": snippet,
        }
        self.nb_hist["cells"].append(cell)
        self.executions += 1

        return ExecuteResponse(outputs=outputs, execution_count=self.executions)


class KernelException(Exception):
    """
    Kernel execution and session errors.
    """

    pass
