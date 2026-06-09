import yaml
from models.role import Role
from models.rule import Rule
from models.binding import Binding
from models.subject import Subject
from models.pod import Pod


def load_yaml(path: str):
    with open(path, "r") as file:
        return list(yaml.safe_load_all(file))


def load_roles(path: str) -> list[Role]:
    docs = load_yaml(path)
    roles = []

    for doc in docs:
        rules = []
        for rule in doc.get("rules", []):
            rules.append(
                Rule(
                    api_groups=rule.get("apiGroups", []),
                    resources=rule.get("resources", []),
                    verbs=rule.get("verbs", [])
                )
            )
        roles.append(
            Role(
                kind=doc["kind"],
                name=doc["metadata"]["name"],
                namespace=doc["metadata"].get("namespace"),
                rules=rules
            )
        )

    return roles


def load_bindings(path: str) -> list[Binding]:
    docs = load_yaml(path)
    bindings = []

    for doc in docs:
        subjects = []
        for s in doc.get("subjects", []):
            subjects.append(
                Subject(
                    kind=s["kind"],
                    name=s["name"],
                    namespace=s.get("namespace")
                )
            )
        bindings.append(
            Binding(
                kind=doc["kind"],
                name=doc["metadata"]["name"],
                namespace=doc["metadata"].get("namespace"),
                role_ref_kind=doc["roleRef"]["kind"],
                role_ref_name=doc["roleRef"]["name"],
                subjects=subjects
            )
        )

    return bindings


def load_pods(path: str) -> list[Pod]:
    docs = load_yaml(path)
    pods = []

    for doc in docs:
        if doc.get("kind") != "Pod":
            continue

        metadata = doc.get("metadata", {})
        spec = doc.get("spec", {})

        pods.append(
            Pod(
                name=metadata["name"],
                namespace=metadata.get("namespace", "default"),
                service_account_name=spec.get("serviceAccountName", "default"),
            )
        )

    return pods