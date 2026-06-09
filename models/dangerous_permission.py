from pydantic import BaseModel
from models.permission import Permission


class DangerousPermission(BaseModel):
    """
    Dangerous rule info
    """
    permission: Permission
    rule_name: str
    severity: str
    description: str
