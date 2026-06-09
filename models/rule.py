from pydantic import BaseModel


class Rule(BaseModel):
    """
    Правило RBAC
    """
    api_groups: list[str]
    resources: list[str]
    verbs: list[str]