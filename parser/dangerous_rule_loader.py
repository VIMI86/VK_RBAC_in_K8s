import yaml
from models.dangerous_rule import DangerousRule


def load_dangerous_rules(path: str) -> list[DangerousRule]:

    with open(path, "r") as file:
        data = yaml.safe_load(file)

    rules = []

    for item in data:

        rules.append(
            DangerousRule(
                name=item["name"],
                api_groups=item.get("apiGroups", []),
                resources=item["resources"],
                verbs=item["verbs"],
                severity=item["severity"],
                description=item["description"]
            )
        )

    return rules