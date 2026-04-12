from enum import StrEnum


class WorkflowType(StrEnum):
    CHAPTER_GENERATION = "chapter_generation"


class WorkflowStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    WAITING_APPROVAL = "waiting_approval"


class WorkflowStage(StrEnum):
    LOAD_CONTEXT = "load_context"
    GENERATE_BLUEPRINT = "generate_blueprint"
    GENERATE_OUTLINE = "generate_outline"
    GENERATE_WRITING = "generate_writing"
    GENERATE_SUMMARY = "generate_summary"
    GENERATE_CUMULATIVE_SUMMARY = "generate_cumulative_summary"


class WorkflowErrorCode(StrEnum):
    LLM_CALL_ERROR = "llm_call_error"
    PARSE_ERROR = "parse_error"
    SQLITE_WRITE_ERROR = "sqlite_write_error"
    VECTOR_WRITE_ERROR = "vector_write_error"
    CONTEXT_TOO_LONG = "context_too_long"
