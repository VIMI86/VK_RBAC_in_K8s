from pydantic import BaseModel


class Pod(BaseModel):
    """
    Представляет Kubernetes Pod для анализа его ServiceAccount.

    Атрибуты:
        name: Имя пода
        namespace: Пространство имён, в котором запущен под
        service_account_name: Имя сервисного аккаунта, связанного с подом
    """
    name: str
    namespace: str
    service_account_name: str
