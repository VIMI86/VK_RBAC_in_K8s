from pydantic import BaseModel


class Subject(BaseModel):
    """
    Представляет субъекта в RBAC-привязке (RoleBinding/ClusterRoleBinding).

    Атрибуты:
        kind: Тип субъекта ("User", "ServiceAccount", "Group")
        name: Уникальное имя субъекта
        namespace: Пространство имён (только для ServiceAccount)
    """
    kind: str
    name: str
    namespace: str | None = None