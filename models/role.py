from pydantic import BaseModel
from models.rule import Rule


class Role(BaseModel):
    """
    Role and ClusterRole, роль выдает список прав для пользователя
    """
    kind: str
    name: str
    namespace: str | None = None
    rules: list[Rule]