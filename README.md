 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/README.md b/README.md
index d11d660bad318e54aa0c4a0a953a86caf185588d..421795900990afdce17cf1d28cc6843ba2068c43 100644
--- a/README.md
+++ b/README.md
@@ -1 +1,58 @@
-# First project on Git
+# Lightweight CRM API
+
+Небольшой прототип CRM на базе FastAPI + SQLite. Можно быстро стартовать, чтобы управлять клиентами, сделками и взаимодействиями.
+
+## Как запустить
+
+1. Установите зависимости:
+
+```bash
+pip install -r requirements.txt
+```
+
+2. Запустите сервер разработки:
+
+```bash
+uvicorn app.main:app --reload
+```
+
+Приложение поднимется на `http://127.0.0.1:8000`. Документация будет доступна в Swagger UI по `/docs`.
+
+## Основные возможности
+
+- **Клиенты**: создание и просмотр клиентов.
+- **Сделки**: добавление сделок к клиентам и обновление стадий.
+- **Взаимодействия**: логирование звонков, писем и заметок по клиентам.
+- **Здоровье сервиса**: `/health` возвращает статус.
+
+## Примеры запросов
+
+### Создать клиента
+
+```bash
+curl -X POST http://127.0.0.1:8000/customers \
+  -H "Content-Type: application/json" \
+  -d '{"name":"Иван Петров","email":"ivan@example.com","phone":"+79999999999","company":"ООО Пример"}'
+```
+
+### Добавить сделку
+
+```bash
+curl -X POST http://127.0.0.1:8000/deals \
+  -H "Content-Type: application/json" \
+  -d '{"title":"Подписка на сервис","value":120000,"stage":"proposal","customer_id":1}'
+```
+
+### Записать взаимодействие
+
+```bash
+curl -X POST http://127.0.0.1:8000/interactions \
+  -H "Content-Type: application/json" \
+  -d '{"subject":"Звонок","note":"Обсудили внедрение","channel":"call","customer_id":1}'
+```
+
+### Обновить стадию сделки
+
+```bash
+curl -X PATCH "http://127.0.0.1:8000/deals/1?stage=won"
+```
 
EOF
)
