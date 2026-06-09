from pydantic import BaseModel
from models.subject import Subject


class Binding(BaseModel):
    """
    RoleBinding, ClusterRoleBinding
    """
    kind: str
    name: str
    namespace: str | None = None

    role_ref_kind: str
    role_ref_name: str

    subjects: list[Subject]

