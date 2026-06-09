from pydantic import BaseModel


class Pod(BaseModel):
    name: str
    namespace: str
    service_account_name: str
