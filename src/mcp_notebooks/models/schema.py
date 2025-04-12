from pydantic import BaseModel, Field
from typing import List, Dict


class StartKernelResponse(BaseModel):
    session_id: str | None = Field(
        ...,
        description="Unique ID for the created kernel session.",
        json_schema_extra={"example": "12a3bc45-678d-901e-fg23-456789abcdef"},
    )
    message: str = Field(
        ...,
        description="Status message confirming session creation.",
        json_schema_extra={"example": "success"},
    )


class CodeSnippet(BaseModel):
    session_id: str = Field(
        ...,
        description="ID of the active kernel session.",
        json_schema_extra={"example": "12a3bc45-678d-901e-fg23-456789abcdef"},
    )
    code: str = Field(
        ...,
        description="Code snippet to be executed within the session.",
        json_schema_extra={
            "example": "print('Hello, world!')",
        },
    )


class ExecuteResponse(BaseModel):
    outputs: List[Dict[str, str | None]] = Field(
        ...,
        description="List of outputs from executing the code.",
        json_schema_extra={
            "example": [
                {"output_type": "stream", "name": "stdout", "text": "Hello, world!\n"}
            ]
        },
    )
    execution_count: int = Field(
        ...,
        description="The execution count (incremented with each execution).",
        json_schema_extra={"example": 1},
    )


class ShutdownResponse(BaseModel):
    message: str = Field(
        ...,
        description="Shutdown status message.",
        json_schema_extra={"example": "success"},
    )
    notebook: str = Field(
        ...,
        description="Notebook code as a string.",
    )
