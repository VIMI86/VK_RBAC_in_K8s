from pydantic import BaseModel
from models.permission import Permission


class DangerousPermission(BaseModel):
    """
    Представляет опасное разрешение, обнаруженное при анализе RBAC.

    Атрибуты:
        permission: Объект Permission с деталями разрешения
        rule_name: Имя правила из конфигурации, которое сработало
        severity: Уровень опасности ("high", "medium", "low")
        description: Описание почему разрешение считается опасным
    """
    permission: Permission
    rule_name: str
    severity: str
    description: str
