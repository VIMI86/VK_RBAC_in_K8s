import json

from models.permission import Permission
from models.dangerous_permission import DangerousPermission
from models.dangerous_pod import DangerousPod


def _permission_to_dict(permission: Permission) -> dict:
    return {
        "subject_kind": permission.subject_kind,
        "subject_name": permission.subject_name,
        "subject_namespace": permission.subject_namespace,
        "scope": permission.scope,
        "namespace": permission.namespace,
        "api_group": permission.api_group,
        "resource": permission.resource,
        "verb": permission.verb,
    }


def _dangerous_to_dict(dangerous: DangerousPermission) -> dict:
    return {
        **_permission_to_dict(dangerous.permission),
        "severity": dangerous.severity,
        "rule_name": dangerous.rule_name,
        "description": dangerous.description,
    }


def _dangerous_pod_to_dict(pod: DangerousPod) -> dict:
    return {
        "pod_name": pod.pod_name,
        "pod_namespace": pod.pod_namespace,
        "service_account_name": pod.service_account_name,
        "service_account_namespace": pod.service_account_namespace,
        "matched_rules": pod.matched_rules,
    }


def _build_subjects(
        permissions: list[Permission],
        dangerous_permissions: list[DangerousPermission],
) -> list[dict]:
    subjects: dict[tuple, dict] = {}

    for permission in permissions:
        key = (
            permission.subject_kind,
            permission.subject_name,
            permission.subject_namespace,
        )
        if key not in subjects:
            subjects[key] = {
                "subject_kind": permission.subject_kind,
                "subject_name": permission.subject_name,
                "subject_namespace": permission.subject_namespace,
                "permissions": [],
                "dangerous_permissions": [],
            }
        subjects[key]["permissions"].append(_permission_to_dict(permission))

    for dangerous in dangerous_permissions:
        permission = dangerous.permission
        key = (
            permission.subject_kind,
            permission.subject_name,
            permission.subject_namespace,
        )
        if key not in subjects:
            subjects[key] = {
                "subject_kind": permission.subject_kind,
                "subject_name": permission.subject_name,
                "subject_namespace": permission.subject_namespace,
                "permissions": [],
                "dangerous_permissions": [],
            }
        subjects[key]["dangerous_permissions"].append(
            _dangerous_to_dict(dangerous)
        )

    return list(subjects.values())


def export_to_txt(
        report: str,
        path: str
):

    with open(path, "w", encoding="utf-8") as file:
        file.write(report)


def export_to_json(
        permissions: list[Permission],
        dangerous_permissions: list[DangerousPermission],
        dangerous_pods: list[DangerousPod],
        path: str,
        danger_only: bool = False,
):

    result = {
        "danger_only": danger_only,
        "subjects": _build_subjects(permissions, dangerous_permissions),
        "dangerous_pods": [
            _dangerous_pod_to_dict(pod) for pod in dangerous_pods
        ],
    }

    if danger_only:
        result["subjects"] = [
            {
                "subject_kind": subject["subject_kind"],
                "subject_name": subject["subject_name"],
                "subject_namespace": subject["subject_namespace"],
                "dangerous_permissions": subject["dangerous_permissions"],
            }
            for subject in result["subjects"]
            if subject["dangerous_permissions"]
        ]

    with open(path, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)
