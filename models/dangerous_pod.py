from pydantic import BaseModel


class DangerousPod(BaseModel):
    pod_name: str
    pod_namespace: str
    service_account_name: str
    service_account_namespace: str
    matched_rules: list[str]
