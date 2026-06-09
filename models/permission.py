from pydantic import BaseModel


class Permission(BaseModel):
    """
    Представляет конкретное RBAC-разрешение для субъекта.

    Атрибуты:
        subject_kind: Тип субъекта ("User", "ServiceAccount", "Group")
        subject_name: Имя субъекта
        subject_namespace: Пространство имён (для ServiceAccount)
        resource: Ресурс Kubernetes (например, "pods", "secrets")
        verb: Глагол операции ("get", "list", "create", "delete", "watch", "update", "patch")
        api_group: API-группа ресурса ("" для core API)
        scope: Область действия ("cluster" или "namespace")
        namespace: Конкретный namespace (если scope = "namespace")
    """
    subject_kind: str
    subject_name: str
    subject_namespace: str | None = None

    resource: str
    verb: str

    api_group: str
    scope: str
    namespace: str | None = None

