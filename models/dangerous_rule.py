from pydantic import BaseModel


class DangerousRule(BaseModel):
    """
    Finding dangerous rule
    """

    name: str
    api_groups: list[str] = []
    resources: list[str]
    verbs: list[str]

    severity: str
    description: str
