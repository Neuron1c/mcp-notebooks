from typing import Dict


def convert_message_to_output(msg: dict) -> Dict[str, str | None]:
    """
    Convert a Jupyter kernel message to an nbformat-compliant output.
    """
    msg_type = msg["header"]["msg_type"]
    content = msg["content"]

    if msg_type == "stream":
        return {
            "output_type": "stream",
            "name": content.get("name", ""),
            "text": content.get("text", ""),
        }
    elif msg_type == "execute_result":
        return {
            "output_type": "execute_result",
            "execution_count": None,  # This will be set on the cell level.
            "data": content.get("data", {}),
            "metadata": content.get("metadata", {}),
        }
    elif msg_type == "display_data":
        return {
            "output_type": "display_data",
            "data": content.get("data", {}),
            "metadata": content.get("metadata", {}),
        }
    elif msg_type == "error":
        return {
            "output_type": "error",
            "ename": content.get("ename", ""),
            "evalue": content.get("evalue", ""),
            "traceback": content.get("traceback", []),
        }
    else:
        # For any other type of message, return a generic representation.
        return {"output_type": msg_type, "content": content}
