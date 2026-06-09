# Kubernetes RBAC Analyzer

Анализатор RBAC для Kubernetes: парсит Roles, ClusterRoles, RoleBindings и ClusterRoleBindings, строит полный список прав по субъектам, определяет опасные permissions по конфигурируемым правилам, находит поды с опасными ServiceAccount.

## Установка

```bash
pip install -r requirements.txt
```

## Запуск

```bash
python main.py
```

С кастомными путями:

```bash
python main.py \
  --roles examples/roles.yaml \
  --clusterroles examples/clusterroles.yaml \
  --rolebindings examples/rolebindings.yaml \
  --clusterrolebindings examples/clusterrolebindings.yaml \
  --pods examples/pods.yaml \
  --danger-rules config/dangerous_rules.yaml
```

Только опасные права:

```bash
python main.py --danger-only
```

Экспорт:

```bash
python main.py --output txt
python main.py --output json
python main.py --output json --output-file output/my_report.json
```

## Структура проекта

```
models/          # Pydantic-модели (Role, Permission, Pod, DangerousRule, …)
parser/          # Загрузка YAML
analyzer/        # Сборка прав, wildcard-логика, детектор, анализ подов
reports/         # Формирование и экспорт отчётов
config/          # dangerous_rules.yaml — настраиваемые опасные правила
examples/        # Тестовые RBAC-манифесты и Pod-манифесты
docs/            # Критерии правил и алгоритмическая схема
```

## Конфигурация опасных правил

Правила в `config/dangerous_rules.yaml`. Добавление нового правила не требует изменения кода.

Подробное обоснование: [docs/dangerous_rules_criteria.md](docs/dangerous_rules_criteria.md)

Алгоритм: [docs/algorithm.md](docs/algorithm.md)

## Возможности

- Права по каждому User / Group / ServiceAccount
- Scope: `cluster` или `namespace:<имя>`
- Опасные права с severity (CRITICAL / HIGH / MEDIUM)
- Поддержка wildcard (`*`) с исключением безопасных read-only правил
- Поиск подов, использующих ServiceAccount с опасными правами
- Фильтр `--danger-only`
- Полный JSON-отчёт: субъекты, все права, опасные права, опасные поды

## Тестовые данные

| Субъект | Роль | Ожидание |
|---------|------|----------|
| User alice | pod-reader (default) | Безопасные read-права на pods |
| ServiceAccount app-sa | secret-reader (cluster) | CRITICAL: SecretRead |
| ServiceAccount deployer-sa | workload-modifier (production) | HIGH: WorkloadCreation (пример из задания) |
| User bob | cluster-viewer (`*/*` get,list,watch) | Безопасно — wildcard исключён |
| Group devops | cluster-admin-lite (`verbs: *`) | Опасно — полный wildcard |

| Pod | ServiceAccount | Ожидание |
|-----|----------------|----------|
| default/backend-api | app-sa | Опасный — SecretRead |
| default/web-frontend | default | Безопасный |
| production/deploy-worker | deployer-sa | Опасный — WorkloadCreation |
