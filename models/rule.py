from pydantic import BaseModel


class Rule(BaseModel):
    """
    Представляет отдельное правило RBAC внутри Role или ClusterRole.

    Атрибуты:
        api_groups: Список API-групп (["apps", "rbac.authorization.k8s.io"])
        resources: Список ресурсов (["pods", "deployments", "secrets"])
        verbs: Список глаголов операций (["get", "list", "create", "delete"])
    """
    api_groups: list[str]
    resources: list[str]
    verbs: list[str]