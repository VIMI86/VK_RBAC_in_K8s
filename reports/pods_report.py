from models.dangerous_pod import DangerousPod


def generate_pods_report(dangerous_pods: list[DangerousPod]) -> str:
    lines = ["=" * 60, "Pods with dangerous ServiceAccounts", ""]

    if not dangerous_pods:
        lines.append("NONE")
        return "\n".join(lines)

    for pod in dangerous_pods:
        lines.append(
            f"Pod: {pod.pod_namespace}/{pod.pod_name} "
            f"(SA: {pod.service_account_namespace}/{pod.service_account_name})"
        )
        lines.append(f"  Rules: {', '.join(pod.matched_rules)}")
        lines.append("")

    return "\n".join(lines).rstrip()
