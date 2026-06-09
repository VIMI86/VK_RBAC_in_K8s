from models.permission import Permission
from models.role import Role
from models.binding import Binding


def build_permissions(
        roles: list[Role],
        clusterroles: list[Role],
        bindings: list[Binding],
        clusterbindings: list[Binding]
):
    role_map = {}
    permissions = []

    for role in roles:
        role_map[("Role", role.name)] = role

    for clusterrole in clusterroles:
        role_map[("ClusterRole", clusterrole.name)] = clusterrole

    all_bindings = bindings + clusterbindings

    for binding in all_bindings:
        role = role_map.get(
            (
                binding.role_ref_kind,
                binding.role_ref_name
            )
        )

        if role is None:
            continue

        is_cluster_scope = binding.kind == "ClusterRoleBinding"
        effective_namespace = None if is_cluster_scope else binding.namespace

        for subject in binding.subjects:
            for rule in role.rules:
                for api_group in rule.api_groups:
                    for resource in rule.resources:
                        for verb in rule.verbs:
                            permissions.append(
                                Permission(
                                    subject_kind=subject.kind,
                                    subject_name=subject.name,
                                    subject_namespace=subject.namespace,
                                    resource=resource,
                                    verb=verb,
                                    api_group=api_group,
                                    scope="cluster"
                                    if is_cluster_scope
                                    else "namespace",
                                    namespace=effective_namespace,
                                )
                            )

    return permissions
