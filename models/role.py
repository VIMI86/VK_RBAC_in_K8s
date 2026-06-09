from pydantic import BaseModel
from models.rule import Rule


class Role(BaseModel):
    """
    Представляет Role или ClusterRole в Kubernetes RBAC.

    Атрибуты:
        kind: Тип роли ("Role" для namespace, "ClusterRole" для кластера)
        name: Уникальное имя роли
        namespace: Пространство имён (только для Role, для ClusterRole = None)
        rules: Список правил RBAC, определяющих разрешения
    """
    kind: str
    name: str
    namespace: str | None = None
    rules: list[Rule]