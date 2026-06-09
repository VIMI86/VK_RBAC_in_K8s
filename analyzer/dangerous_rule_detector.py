from models.permission import Permission
from models.dangerous_rule import DangerousRule
from models.dangerous_permission import DangerousPermission
from analyzer.wildcard import (
    is_safe_wildcard,
    matches_api_group,
    matches_resource,
    matches_verb,
)


def detect_dangerous_permissions(
        permissions: list[Permission],
        dangerous_rules: list[DangerousRule]
) -> list[DangerousPermission]:

    dangerous_permissions = []

    for permission in permissions:

        if is_safe_wildcard(permission):
            continue

        for rule in dangerous_rules:

            if not matches_api_group(permission.api_group, rule.api_groups):
                continue

            if not matches_resource(permission.resource, rule.resources):
                continue

            if not matches_verb(permission.verb, rule.verbs):
                continue

            dangerous_permissions.append(
                DangerousPermission(
                    permission=permission,
                    rule_name=rule.name,
                    severity=rule.severity,
                    description=rule.description
                )
            )

    return dangerous_permissions
