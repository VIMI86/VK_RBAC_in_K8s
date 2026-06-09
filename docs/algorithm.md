# Алгоритм работы RBAC Analyzer

## Схема

```mermaid
flowchart TD
    A[Входные YAML/JSON] --> B[Парсинг Roles / ClusterRoles]
    A --> C[Парсинг RoleBindings / ClusterRoleBindings]
    A --> D[Загрузка dangerous_rules.yaml]

    B --> E[Permission Builder]
    C --> E

    E --> F["Список Permission\n(субъект + apiGroup + resource + verb + scope + namespace)"]

    F --> G[Dangerous Rule Detector]
    D --> G

    G --> H{Wildcard?}
    H -->|read-only *| I[Пропуск — безопасно]
    H -->|write или verb *| J[Сопоставление с правилами]
    J --> K{Совпадение apiGroup,\nresource, verb?}
    K -->|да| L[DangerousPermission]
    K -->|нет| M[Не опасно]

    F --> N[Report Generator]
    L --> N

    N --> O{--danger-only?}
    O -->|да| P[Только опасные]
    O -->|нет| Q[Все права + метки опасности]

    P --> R[Консоль / txt / json]
    Q --> R

    F --> S[Pod Analyzer]
    L --> S
    C --> S
    S --> T["Поды с опасными SA\n(serviceAccountName → dangerous SA)"]
    T --> N
```

## Этапы

### 1. Парсинг

- Чтение мульти-документных YAML-файлов (`---`)
- Построение моделей: `Role`, `Binding`, `Subject`, `Rule`

### 2. Permission Builder

Для каждого binding:

1. Найти роль по `roleRef.kind` + `roleRef.name`
2. Для каждого subject и каждого rule развернуть декартово произведение `apiGroups × resources × verbs`
3. Определить scope:
   - `ClusterRoleBinding` → `scope: cluster`, `namespace: null`
   - `RoleBinding` → `scope: namespace`, `namespace: <binding.namespace>`

### 3. Dangerous Rule Detector

Для каждого permission:

1. Если `is_safe_wildcard()` — пропуск
2. Иначе для каждого правила из конфига проверить совпадение полей (с учётом `*`)
3. При совпадении — добавить `DangerousPermission` с severity и описанием

### 4. Отчёт

- Группировка по субъекту (`kind`, `name`, `sa-namespace`)
- Для каждого права: `[cluster]` или `[namespace:<ns>]`, apiGroup/resource/verb
- Секция dangerous permissions с правилом и причиной
