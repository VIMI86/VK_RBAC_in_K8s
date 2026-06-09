from parser.yaml_loader import load_roles, load_bindings, load_pods
from parser.dangerous_rule_loader import load_dangerous_rules
from analyzer.permission_builder import build_permissions
from analyzer.dangerous_rule_detector import detect_dangerous_permissions
from analyzer.pod_analyzer import find_pods_with_dangerous_sa
from reports.report_generator import generate_report
from reports.danger_report import generate_danger_report
from reports.pods_report import generate_pods_report
from reports.export_report import export_to_txt, export_to_json

import argparse


def main():

    parser = argparse.ArgumentParser(description="Kubernetes RBAC Analyzer")

    parser.add_argument("--roles",
                        default="examples/roles.yaml", help="Path to Roles YAML file")

    parser.add_argument("--clusterroles",
                        default="examples/clusterroles.yaml", help="Path to ClusterRoles YAML file")

    parser.add_argument("--rolebindings",
                        default="examples/rolebindings.yaml", help="Path to RoleBindings YAML file")

    parser.add_argument("--clusterrolebindings",
                        default="examples/clusterrolebindings.yaml", help="Path to ClusterRoleBindings YAML file")

    parser.add_argument("--pods",
                        default="examples/pods.yaml", help="Path to Pods YAML file")

    parser.add_argument("--danger-rules",
                        default="config/dangerous_rules.yaml", help="Path to dangerous rules config")

    parser.add_argument("--danger-only", action="store_true", help="Show only dangerous permissions")

    parser.add_argument("--output", choices=["txt", "json"], help="Export report")

    parser.add_argument("--output-file", help="Output file path (default: output/report.txt or output/report.json)")

    args = parser.parse_args()

    roles = load_roles(args.roles)
    clusterroles = load_roles(args.clusterroles)
    bindings = load_bindings(args.rolebindings)
    clusterbindings = load_bindings(args.clusterrolebindings)
    pods = load_pods(args.pods)

    permissions = build_permissions(
        roles,
        clusterroles,
        bindings,
        clusterbindings
    )

    dangerous_rules = load_dangerous_rules(args.danger_rules)
    dangerous_permissions = detect_dangerous_permissions(permissions, dangerous_rules)
    dangerous_pods = find_pods_with_dangerous_sa(pods, dangerous_permissions)

    if args.danger_only:
        report = generate_danger_report(dangerous_permissions)
    else:
        report = generate_report(permissions, dangerous_permissions)

    pods_report = generate_pods_report(dangerous_pods)

    print(report)
    print()
    print(pods_report)

    if args.output == "txt":
        output_path = args.output_file or "output/report.txt"
        export_to_txt(f"{report}\n\n{pods_report}", output_path)
        print(f"\nReport saved to {output_path}")

    elif args.output == "json":
        output_path = args.output_file or "output/report.json"
        export_to_json(
            permissions,
            dangerous_permissions,
            dangerous_pods,
            output_path,
            danger_only=args.danger_only,
        )
        print(f"\nReport saved to {output_path}")


if __name__ == "__main__":
    main()