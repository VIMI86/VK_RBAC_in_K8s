from collections import defaultdict
from models.permission import Permission
from models.dangerous_permission import DangerousPermission


def _format_subject_header(permission: Permission) -> str:
    header = f"Subject: {permission.subject_kind} {permission.subject_name}"

    if permission.subject_namespace:
        header += f" (sa-namespace: {permission.subject_namespace})"

    return header


def _format_scope(permission: Permission) -> str:
    if permission.scope == "namespace" and permission.namespace:
        return f"namespace:{permission.namespace}"
    return permission.scope


def generate_report(
        permissions: list[Permission],
        dangerous_permissions: list[DangerousPermission]
) -> str:
    report_lines = []
    permissions_by_subject = defaultdict(list)

    for permission in permissions:
        key = (
            permission.subject_kind,
            permission.subject_name,
            permission.subject_namespace,
        )
        permissions_by_subject[key].append(permission)

    dangerous_by_subject = defaultdict(list)

    for dangerous in dangerous_permissions:
        key = (
            dangerous.permission.subject_kind,
            dangerous.permission.subject_name,
            dangerous.permission.subject_namespace,
        )
        dangerous_by_subject[key].append(dangerous)

    for subject, perms in permissions_by_subject.items():
        report_lines.append("=" * 60)
        report_lines.append(_format_subject_header(perms[0]))
        report_lines.append("")
        report_lines.append("Permissions:")

        for permission in perms:
            report_lines.append(
                f"[{_format_scope(permission)}] "
                f"{permission.api_group or 'core'}/"
                f"{permission.resource}/"
                f"{permission.verb}"
            )

        report_lines.append("")
        report_lines.append("Dangerous permissions:")

        if subject not in dangerous_by_subject:
            report_lines.append("NONE")
        else:
            for dangerous in dangerous_by_subject[subject]:
                report_lines.append("")
                report_lines.append(f"[{dangerous.severity}]")
                report_lines.append(f"Rule: {dangerous.rule_name}")
                report_lines.append(
                    f"Permission: "
                    f"[{_format_scope(dangerous.permission)}] "
                    f"{dangerous.permission.api_group or 'core'}/"
                    f"{dangerous.permission.resource}/"
                    f"{dangerous.permission.verb}"
                )
                report_lines.append(f"Reason: {dangerous.description}")

        report_lines.append("")

    return "\n".join(report_lines)
