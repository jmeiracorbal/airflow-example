# Apache Airflow Example

> This is an experimental example with Apache Airflow.

  <a href="https://airflow.apache.org/">
    <img src="https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=apache-airflow&logoColor=white" alt="Apache Airflow">
  </a>
  <a href="https://python.org/">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  </a>
  <a href="https://docker.com/">
    <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  </a>
  <a href="https://postgresql.org/">
    <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  </a>
  <a href="https://github.com/apache/airflow">
    <img src="https://img.shields.io/badge/Educational-Example-FF6B6B?style=for-the-badge" alt="Educational">
  </a>
  <a href="https://pages.github.com/">
    <img src="https://img.shields.io/badge/GitHub%20Pages-222222?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Pages">
  </a>

## 📋 Table of Contents

- [Concepts](#concepts)
- [Structure](#structure)
- [Standalone Setup](#standalone)
- [Containerized Setup](#containerized)
- [Troubleshooting](#troubleshooting)

---

# Concepts

- **DAGs** (Directed Acyclic Graphs): Define workflows as a collection of tasks with dependencies.
- **Tasks**: Individual units of work within a DAG (PythonOperator, BashOperator, etc.).
- **Operators**: Predefined task types that define what work to execute.
- **Schedulers**: Airflow component that monitors DAGs and triggers task execution.
- **Executors**: Determine how tasks are executed (SequentialExecutor, LocalExecutor, CeleryExecutor).
- **Web Server**: UI for monitoring and managing DAGs, tasks, and workflows.
- **Metadata Database**: Stores DAG definitions, task states, and execution history.
- **Fernet Key**: Encryption key for securing sensitive data like connection passwords and variables. Without this key, Airflow can't manage encrypted data with secure methods.

# Structure

```text
apache-airflow/
├── docker-compose.yml
├── dags/
├── logs/
├── plugins/
├── standalone/
│   ├── requirements.txt
│   ├── airflow.cfg
│   ├── pyproject.toml
│   └── airflow.db
└── docker/
    ├── Dockerfile
    ├── requirements.txt
    └── .dockerignore
```

# Standalone

> poetry as depednecy manager.

## Considerations

Using SQLite problems, it's recommended change to another complex engine:

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

> this install uses poetry as depednecy manager.

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

> DAGs can be executed from UI and API too.

Indicate where is AIRFLOW_HOME (using locally):

```bash
export AIRFLOW_HOME=$(pwd)
```

## Run Airflow

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
poetry run airflow api-server --port 8080
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

# Containerized

First of all, generate a fernet key:

```bash
openssl rand -base64 32
```

## Run

```bash
docker compose up -d
```

This will:
- Start PostgreSQL database
- Initialize Airflow database and create admin user
- Start Airflow webserver and scheduler.

Services on docker-compose:

- `postgres`: PostgreSQL database with persistent volume
- `airflow-init`: One-time database initialization and admin user creation
- `airflow`: Airflow webserver on port 8080
- `airflow-scheduler`: Airflow scheduler for task execution

Access the UI at `http://localhost:8080` with:

- Username: `admin`.
- Password: `admin`.

### Environment Variables

Customize user by setting with environment variables:

- `AIRFLOW__ADMIN__USER`: Admin username (default: admin)
- `AIRFLOW__ADMIN__PASSWORD`: Admin password (default: admin)
- `AIRFLOW__ADMIN__EMAIL`: Admin email (default: admin@example.com)
- `AIRFLOW__ADMIN__FIRSTNAME`: Admin first name (default: Admin)
- `AIRFLOW__ADMIN__LASTNAME`: Admin last name (default: User)

You can add a `.env` file and the attribute env_file to the `docker-compose.yml` too or you can define just in time:

```bash
AIRFLOW__ADMIN__USER=miadmin AIRFLOW__ADMIN__PASSWORD=mipassword docker-compose up -d
```

Volumes:

- `postgres_data`: PostgreSQL database persistence
- `./dags`: DAGs directory (bind mount)
- `./logs`: Logs directory (bind mount)
- `./plugins`: Plugins directory (bind mount)

# Troubleshooting

## Standalone

If first install fail, you can reset the database connection.

```bash
pkill -f airflow
```

```bash
export AIRFLOW_HOME=$(pwd) && poetry run airflow db reset --yes
```

> Create database, create admin user and run schedule again.

### Alternative: Standalone Mode

For a complete setup with automatic admin user creation:

```bash
cd standalone
poetry run airflow standalone
```

This starts API server, scheduler, and webserver in one command.

Check executor:

```bash
poetry run airflow config get-value core executor
```

Check the SQL alchemy:

```bash
poetry run airflow config get-value database sql_alchemy_conn
```

## Containerized

### Services Status

```bash
docker compose ps
```

### View Logs

```bash
docker compose logs airflow
docker compose logs airflow-scheduler
```

### Database Reset

```bash
docker compose down -v
docker compose up -d
```

> This removes all data and reinitializes the database.

