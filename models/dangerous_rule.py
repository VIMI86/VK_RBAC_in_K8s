from pydantic import BaseModel


class DangerousRule(BaseModel):
    """
    Модель правила для определения опасных RBAC-разрешений.

    Атрибуты:
        name: Уникальное имя опасного правила
        api_groups: Список API-групп ([""] для core, ["apps"] и т.д.)
        resources: Список ресурсов (["pods", "secrets"])
        verbs: Список глаголов (["get", "list", "create", "delete"])
        severity: Уровень опасности ("high", "medium", "low")
        description: описание угрозы и рекомендации
    """
    name: str
    api_groups: list[str] = []
    resources: list[str]
    verbs: list[str]

    severity: str
    description: str
