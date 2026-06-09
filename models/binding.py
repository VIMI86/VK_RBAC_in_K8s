from pydantic import BaseModel
from models.subject import Subject


class Binding(BaseModel):
    """
    Представляет привязку роли (RoleBinding или ClusterRoleBinding) в Kubernetes RBAC.

    Атрибуты:
        kind: Тип привязки ("RoleBinding" для namespace, "ClusterRoleBinding" для кластера)
        name: Уникальное имя привязки
        namespace: Пространство имён (только для RoleBinding, для ClusterRoleBinding = None)
        role_ref_kind: Тип ссылаемой роли ("Role" или "ClusterRole")
        role_ref_name: Имя ссылаемой роли
        subjects: Список субъектов, получающих разрешения роли
    """
    kind: str
    name: str
    namespace: str | None = None

    role_ref_kind: str
    role_ref_name: str

    subjects: list[Subject]

