from fastapi.testclient import TestClient
import uuid
from mcp_notebooks.app.api import app  # adjust import as needed

client = TestClient(app)


def is_valid_uuid(value):
    try:
        uuid.UUID(str(value))

        return True
    except ValueError:
        return False


def test_hello_world_execution():
    # Start a new kernel session
    start_response = client.post("/start")
    assert start_response.status_code == 200

    data = start_response.json()
    session_id = data["session_id"]
    assert data["message"] == "success"
    assert is_valid_uuid(session_id)

    # Execute a Hello World snippet
    snippet = {
        "session_id": session_id,
        "code": 'print("Hello, world!")',
    }
    exec_response = client.post("/execute", json=snippet)
    assert exec_response.status_code == 200

    exec_data = exec_response.json()

    assert isinstance(exec_data["outputs"], list)
    assert exec_data["execution_count"] >= 1

    # Check that "Hello, world!" is in one of the output strings
    output_strings = exec_data["outputs"][0]
    assert output_strings["text"] == "Hello, world!\n"

    # Shutdown the session
    shutdown_response = client.post(f"/shutdown/{session_id}")
    assert shutdown_response.status_code == 200

    shutdown_data = shutdown_response.json()
    assert shutdown_data["message"] == "success"
    assert isinstance(shutdown_data["notebook"], str)


if __name__ == "__main__":
    test_hello_world_execution()
