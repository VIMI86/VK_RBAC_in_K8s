from collections import defaultdict
from models.pod import Pod
from models.dangerous_permission import DangerousPermission
from models.dangerous_pod import DangerousPod


def _service_account_namespace(permission) -> str | None:
    return permission.subject_namespace or permission.namespace


def find_pods_with_dangerous_sa(
        pods: list[Pod],
        dangerous_permissions: list[DangerousPermission],
) -> list[DangerousPod]:
    rules_by_sa: dict[tuple[str, str], set[str]] = defaultdict(set)

    for dangerous in dangerous_permissions:
        permission = dangerous.permission

        if permission.subject_kind != "ServiceAccount":
            continue

        sa_namespace = _service_account_namespace(permission)
        if not sa_namespace:
            continue

        key = (permission.subject_name, sa_namespace)
        rules_by_sa[key].add(dangerous.rule_name)

    dangerous_pods = []

    for pod in pods:
        key = (pod.service_account_name, pod.namespace)

        if key not in rules_by_sa:
            continue

        dangerous_pods.append(
            DangerousPod(
                pod_name=pod.name,
                pod_namespace=pod.namespace,
                service_account_name=pod.service_account_name,
                service_account_namespace=pod.namespace,
                matched_rules=sorted(rules_by_sa[key]),
            )
        )

    return dangerous_pods
