# Airflow Docker Starter

A simple, ready-to-use Apache Airflow setup with Docker for training junior developers. Start Airflow with a single command!

## 📋 Prerequisites

- **Docker Desktop** installed and running
  - [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
- **8GB RAM** minimum (recommended for Docker)
- **10GB free disk space**

## 🚀 Quick Start

### Option 1: One-Command Setup (Recommended)

```bash
./start.sh
```

This script will:
- Check Docker installation
- Create necessary directories
- Initialize Airflow database
- Start all Airflow services
- Display access information

### Option 2: Manual Setup

```bash
# Create directories
mkdir -p ./dags ./logs ./plugins ./config

# Set environment variables
echo -e "AIRFLOW_UID=$(id -u)" > .env

# Initialize Airflow
docker compose up airflow-init

# Start Airflow
docker compose up -d
```

## 🌐 Accessing Airflow

Once started, access the Airflow web interface:

- **URL**: http://localhost:8080
- **Username**: `airflow`
- **Password**: `airflow`

## 📚 Example DAGs Included

### 1. Hello World DAG (`example_hello_world`)
A simple DAG demonstrating:
- Basic task creation with PythonOperator
- BashOperator usage
- Task dependencies (sequential and parallel)
- Scheduling configuration

**Tasks**:
- `print_hello` → Prints "Hello World"
- `print_date` & `echo_message` → Run in parallel
- `print_goodbye` → Final task

### 2. Data Pipeline DAG (`example_data_pipeline`)
An ETL pipeline example demonstrating:
- Data extraction simulation
- Data transformation with XCom
- Data loading
- Pipeline validation

**Tasks**:
- `extract` → Simulates data extraction
- `transform` → Processes and enriches data
- `load` → Simulates loading to destination
- `validate` → Validates pipeline execution

## 🎓 Learning Path for Juniors

### Step 1: Explore the UI
1. Log in to Airflow UI
2. Navigate to the DAGs page
3. Click on `example_hello_world` to view details
4. Explore the Graph, Grid, and Code views

### Step 2: Run Your First DAG
1. Toggle the DAG to "On" (switch on the left)
2. Click the "Play" button → "Trigger DAG"
3. Watch the tasks execute in real-time
4. Check task logs by clicking on a task

### Step 3: Understand the Code
1. Open `dags/example_hello_world.py`
2. Read the comments explaining each section
3. Understand task dependencies: `task1 >> [task2, task3] >> task4`

### Step 4: Create Your Own DAG
1. Copy `example_hello_world.py` to a new file in `dags/`
2. Modify the DAG name and tasks
3. Save the file (Airflow auto-detects new DAGs)
4. Refresh the UI to see your new DAG

## 🛠️ Useful Commands

### View Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f airflow-webserver
docker compose logs -f airflow-scheduler
```

### Stop Airflow
```bash
docker compose down
```

### Restart Airflow
```bash
docker compose restart
```

### Stop and Remove All Data
```bash
docker compose down -v
```

### Check Service Status
```bash
docker compose ps
```

### Access Airflow CLI
```bash
docker compose run airflow-webserver airflow dags list
docker compose run airflow-webserver airflow tasks list example_hello_world
```

## 📁 Project Structure

```
Airflow-Docker/
├── dags/                          # Your DAG files go here
│   ├── example_hello_world.py     # Simple Hello World DAG
│   └── example_data_pipeline.py   # ETL Pipeline example
├── logs/                          # Airflow logs (auto-generated)
├── plugins/                       # Custom Airflow plugins
├── config/                        # Airflow configuration files
├── docker-compose.yml             # Docker services configuration
├── .env                           # Environment variables
├── start.sh                       # One-command startup script
└── README.md                      # This file
```

## 🔧 Configuration

### Default Settings
- **Executor**: LocalExecutor (suitable for development)
- **Database**: PostgreSQL 13
- **Airflow Version**: 2.10.4 (Latest stable release)
- **Web Server Port**: 8080
- **Load Examples**: Disabled (only custom DAGs shown)

### Customization
Edit `.env` file to customize:
```bash
AIRFLOW_UID=50000
_AIRFLOW_WWW_USER_USERNAME=airflow
_AIRFLOW_WWW_USER_PASSWORD=airflow
```

## 📖 Key Airflow Concepts

### DAG (Directed Acyclic Graph)
- A collection of tasks with dependencies
- Defines the workflow execution order
- Scheduled to run at specific intervals

### Task
- A single unit of work in a DAG
- Can be a Python function, Bash command, etc.
- Has a unique `task_id`

### Operator
- Defines what a task does
- Common operators:
  - `PythonOperator`: Runs Python functions
  - `BashOperator`: Runs Bash commands
  - `EmailOperator`: Sends emails

### Task Dependencies
```python
# Sequential
task1 >> task2 >> task3

# Parallel
task1 >> [task2, task3] >> task4

# Alternative syntax
task1.set_downstream(task2)
```

### XCom (Cross-Communication)
- Share data between tasks
- Push: `task_instance.xcom_push(key='data', value=data)`
- Pull: `task_instance.xcom_pull(task_ids='task_id', key='data')`

## 🐛 Troubleshooting

### Port 8080 Already in Use
```bash
# Change port in docker-compose.yml
ports:
  - "8081:8080"  # Use 8081 instead
```

### Permission Errors
```bash
# Reset permissions
sudo chown -R $(id -u):$(id -g) ./dags ./logs ./plugins
```

### DAG Not Appearing
1. Check file is in `dags/` directory
2. Verify Python syntax (no errors)
3. Wait 30 seconds for Airflow to scan
4. Check scheduler logs: `docker compose logs airflow-scheduler`

### Services Won't Start
```bash
# Clean restart
docker compose down -v
./start.sh
```

## 📚 Additional Resources

- [Official Airflow Documentation](https://airflow.apache.org/docs/)
- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [Airflow Tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html)

## 🤝 Contributing

This is a training repository. Feel free to:
- Add more example DAGs
- Improve documentation
- Share with other teams

## 📝 Notes for Trainers

- Start with `example_hello_world` for basic concepts
- Progress to `example_data_pipeline` for XCom and ETL patterns
- Encourage juniors to modify existing DAGs before creating new ones
- Use the Graph view to visualize task dependencies
- Demonstrate both successful and failed task executions

## ⚠️ Important Notes

- This setup is for **development/training only**
- Not suitable for production use
- Default credentials should be changed in production
- No authentication/security features enabled

---

**Happy Learning! 🎉**

For questions or issues, check the logs or consult the Airflow documentation.