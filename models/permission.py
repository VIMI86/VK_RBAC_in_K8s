from pydantic import BaseModel


class Permission(BaseModel):
    """
    Rule of subject
    """
    subject_kind: str
    subject_name: str
    subject_namespace: str | None = None

    resource: str
    verb: str

    api_group: str
    scope: str
    namespace: str | None = None

