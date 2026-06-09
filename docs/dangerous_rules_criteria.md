# Критерии опасных RBAC-правил

Документ описывает правила из `config/dangerous_rules.yaml`, обоснование выбора и критерии срабатывания.

## Источники

- [Kubernetes RBAC Good Practices](https://kubernetes.io/docs/concepts/security/rbac-good-practices/)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes) (раздел RBAC)
- [rbac.dev](https://rbac.dev/) — каталог типовых ролей и рисков

## Общие критерии

Право считается **опасным**, если совпадают все указанные в правиле поля:

| Поле | Критерий |
|------|----------|
| `apiGroups` | Совпадает с API-группой права. `*` в праве матчит любое правило. Пустой `apiGroups` в конфиге — любая группа. |
| `resources` | Совпадает с ресурсом. `*` в праве матчит любой ресурс из правила. |
| `verbs` | Совпадает с действием. `*` в праве матчит любой verb из правила. |

## Исключения для wildcard (`*`)

Не все правила с `*` опасны. Безопасные wildcard **не попадают** в отчёт:

| Условие | Почему безопасно |
|---------|------------------|
| `verbs` только `get`, `list`, `watch` и `resources: *` | Типичная read-only роль просмотра (аналог `view`), без модификации |
| `verbs` только `get`, `list`, `watch`, `apiGroups: *`, конкретный несенситивный ресурс | Чтение одного типа ресурсов без wildcard на resource |
| `verbs: *` | **Всегда опасно** — полный доступ ко всем действиям |
| Любой write-verb (`create`, `update`, `patch`, `delete`, …) с `*` | **Опасно** — может изменять или удалять объекты |

Сенситивные ресурсы (`secrets`, `roles`, `nodes`, …) при wildcard `apiGroups: *` **не** считаются безопасными.

## Каталог правил

### SecretRead (CRITICAL)

- **Права:** `get`, `list`, `watch` на `secrets` (core API)
- **Риск:** чтение паролей, токенов, TLS-сертификатов
- **Обоснование:** CIS 5.1.2 — ограничение доступа к Secrets

### WorkloadCreation (HIGH)

- **Права:** `create`, `patch`, `update` на workloads (`pods`, `deployments`, `daemonsets`, `statefulsets`, `replicasets`, `jobs`, `cronjobs`)
- **API groups:** `""`, `apps`, `extensions`, `batch`
- **Риск:** privilege escalation через подмену образа контейнера, монтирование hostPath, запуск privileged-подов
- **Обоснование:** пример из задания; K8s docs — workload-модификация как путь к эскалации

### PodExec (HIGH)

- **Права:** `create` на `pods/exec`, `pods/attach`, `pods/portforward`
- **Риск:** интерактивный доступ в контейнер, обход сетевых ограничений
- **Обоснование:** CIS — ограничение exec в production

### RBACEscalation (CRITICAL)

- **Права:** `create`, `update`, `patch`, `bind`, `escalate` на RBAC-объекты
- **API group:** `rbac.authorization.k8s.io`
- **Риск:** прямое повышение привилегий (создание RoleBinding с admin-ролью)
- **Обоснование:** K8s RBAC Good Practices — `escalate` и `bind` как критичные verbs

### Impersonation (CRITICAL)

- **Права:** `impersonate` на `users`, `groups`, `serviceaccounts`
- **Риск:** действия от имени другого субъекта
- **Обоснование:** CIS — impersonation только для администраторов

### ServiceAccountToken (CRITICAL)

- **Права:** `create` на `serviceaccounts/token`
- **Риск:** создание долгоживущих токенов SA (TokenRequest)
- **Обоснование:** K8s 1.24+ — legacy secret tokens; TokenRequest как вектор

### NodeAccess (HIGH)

- **Права:** `get`, `proxy` на `nodes`, `nodes/proxy`
- **Риск:** доступ к kubelet API, метаданные нод
- **Обоснование:** nodes/proxy — обход Pod Security

### CertificateApproval (CRITICAL)

- **Права:** `create`, `approve` на `certificatesigningrequests`
- **API group:** `certificates.k8s.io`
- **Риск:** выпуск клиентских сертификатов с произвольными CN/O
- **Обоснование:** CIS — контроль CSR approvers

### NamespaceDeletion (HIGH)

- **Права:** `delete` на `namespaces`
- **Риск:** удаление всего namespace и ресурсов в нём

### PersistentVolumeModification (MEDIUM)

- **Права:** `create`, `patch`, `update` на PV/PVC
- **Риск:** доступ к данным через подмену томов

### NodeDeletion (HIGH)

- **Права:** `delete` на `nodes`
- **Риск:** вывод нод из кластера, DoS

### SecretDeletion / ConfigMapDeletion (HIGH / MEDIUM)

- **Права:** `delete` на `secrets` / `configmaps`
- **Риск:** удаление критичных данных, нарушение работы приложений

## Добавление своих правил

Добавьте запись в `config/dangerous_rules.yaml`:

```yaml
- name: MyCustomRule
  apiGroups:
    - ""
  resources:
    - myresource
  verbs:
    - create
  severity: HIGH
  description: Why this is dangerous
```

Перезапуск скрипта подхватит изменения без правки Python-кода.
