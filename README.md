# Apache Airflow Example

This it's an experimental example with Apache Airflow.

> poetry as depednecy manager.

## Using locally

Using SQLite problems:

1. One process write on DB.
2. Without concurrent connections
3. Limited concurrency

```text
# airflow.cfg
executor = SequentialExecutor
sql_alchemy_conn = sqlite:///airflow.db
```

If you use another database with paralelism:

```text
# airflow.cfg
executor = LocalExecutor
sql_alchemy_conn = postgresql://user:pass@localhost/airflow
```

> Configured to use SequentialExecutor. LocalExecutor is not compatible with SQLite.

## Install

Check python version:

```bash
ls (...)/bin/python*
```

```bash
poetry env use (...)/bin/python3.12
```

Install Airflow:

```
poetry add "apache-airflow>=2.7.0,<3.0.0"
```

Create DAGs (workflows) directory:

```bash
mkdir -p dags logs plugins
```

Indicate where is AIRFLOW_HOME (using locally):

```bash
export AIRFLOW_HOME=$(pwd)
```

# Running Airflow

```bash
poetry run airflow db init
```

You'll see:

```text
(...)
[2025-07-19T18:54:51.621+0200] {migration.py:211} INFO - Context impl SQLiteImpl.
[2025-07-19T18:54:51.621+0200] {migration.py:214} INFO - Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running stamp_revision  -> 5f2621c13b39
Initialization done
```

Create admin user:

```bash
poetry run airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.com --password admin
```

Example server (deploy locally):

```bash
poetry run airflow webserver --port 8080
```

```bash
cd airflow-learning-example-where-is-your-path && export AIRFLOW_HOME=$(pwd) && poetry run airflow scheduler
```

Check your DAGs:

```bash
poetry run airflow dags list
```

Run your DAGs:

```bash
poetry run airflow dags test hola_mundo 2024-01-01
```

> DAGs can be executed from UI and API too.

# Troubleshooting

If first install fail, you can reset the database connection.

```bash
pkill -f airflow
```

```bash
export AIRFLOW_HOME=$(pwd) && poetry run airflow db reset --yes
```

Check executor:

```bash
poetry run airflow config get-value core executor
```

Check the SQL alchemy:

```bash
poetry run airflow config get-value database sql_alchemy_conn
```

