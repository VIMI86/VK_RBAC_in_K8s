from models.dangerous_permission import DangerousPermission
from reports.report_generator import _format_scope, _format_subject_header


def generate_danger_report(
        dangerous_permissions:
        list[DangerousPermission]
) -> str:
    lines = []

    for p in dangerous_permissions:
        lines.append("=" * 60)
        lines.append(_format_subject_header(p.permission))
        lines.append(f"Severity: {p.severity}")
        lines.append(
            f"Permission: "
            f"[{_format_scope(p.permission)}] "
            f"{p.permission.api_group or 'core'}/"
            f"{p.permission.resource}/"
            f"{p.permission.verb}"
        )
        lines.append(f"Reason: {p.description}")
        lines.append("")

    return "\n".join(lines)
