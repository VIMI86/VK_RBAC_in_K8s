from pydantic import BaseModel


class Subject(BaseModel):
    """
    Subject Permission
    """
    kind: str
    name: str
    namespace: str | None = None