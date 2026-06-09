from models.permission import Permission

SAFE_READ_VERBS = frozenset({"get", "list", "watch"})
SENSITIVE_RESOURCES = frozenset({
    "secrets",
    "serviceaccounts/token",
    "roles",
    "clusterroles",
    "rolebindings",
    "clusterrolebindings",
    "users",
    "groups",
    "serviceaccounts",
    "nodes",
    "nodes/proxy",
    "namespaces",
    "persistentvolumes",
    "certificatesigningrequests",
    "pods/exec",
    "pods/attach",
    "pods/portforward",
})


def has_wildcard(permission: Permission) -> bool:
    return "*" in (
        permission.api_group,
        permission.resource,
        permission.verb,
    )


def is_safe_wildcard(permission: Permission) -> bool:

    if not has_wildcard(permission):
        return False

    if permission.verb == "*":
        return False

    if permission.verb not in SAFE_READ_VERBS:
        return False

    if permission.resource == "*":
        return True

    if permission.api_group == "*":
        return permission.resource not in SENSITIVE_RESOURCES

    return False


def matches_api_group(permission_value: str, rule_values: list[str]) -> bool:
    if not rule_values:
        return True
    if permission_value == "*":
        return True
    if "*" in rule_values:
        return True
    return permission_value in rule_values


def matches_resource(permission_value: str, rule_values: list[str]) -> bool:
    if permission_value == "*":
        return True
    if "*" in rule_values:
        return True
    return permission_value in rule_values


def matches_verb(permission_value: str, rule_values: list[str]) -> bool:
    if permission_value == "*":
        return True
    if "*" in rule_values:
        return True
    return permission_value in rule_values
