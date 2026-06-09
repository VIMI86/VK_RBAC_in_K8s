from pydantic import BaseModel


class DangerousPod(BaseModel):
    """
    Представляет Pod, который использует опасный ServiceAccount.

    Атрибуты:
        pod_name: Имя пода
        pod_namespace: Пространство имён пода
        service_account_name: Имя сервисного аккаунта, который использует под
        service_account_namespace: Пространство имён сервисного аккаунта
        matched_rules: Список названий опасных правил, которые сработали для этого SA
    """
    pod_name: str
    pod_namespace: str
    service_account_name: str
    service_account_namespace: str
    matched_rules: list[str]
