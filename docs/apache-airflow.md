
# Apache Airflow

Resources:

* [What is Airflow? - Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/index.html)
* [Apache Airflow: The Hands-On Guide - Udemy Course](https://udemy.com/course/the-ultimate-hands-on-course-to-master-apache-airflow/)

## The basics of Apache Airflow

### What is Airflow?

#### Airflow is a Data Orchestrator.

Apache Airflow is an open-source platform for developing, scheduling, and monitoring batch-oriented workflows. Airflow’s extensible Python framework enables you to build workflows connecting with virtually any technology. A web interface helps manage the state of your workflows. Airflow is deployable in many ways, varying from a single process on your laptop to a distributed setup to support even the biggest workflows.

### Why a Data Orchestrator?

Data Orchestration is the process of coordinating and automating the movement, transformation, and integration of data across various systems and processes to ensure efficient and reliable data workflows.

For example, you need to build a data workflow to:

Extract >>> Clean >>> Transform >>> Load data

With a Data Orchestrator you can define dependencies between those steps, ensuring that the execution order is continually respected. The Data Orchestrator will automatically retry tasks that fail and if it doesn’t succeed, it will not execute the rest of the tasks.

Data Orchestrator enables you to run and monitor data workflows at scale.

### Why Airflow?

#### 1. Reliably orchestrate your data workflows at scale.

Airflow can run multiple tasks in parallel across multiple machines. It leverages frameworks like [Celery](https://docs.celeryq.dev/en/stable/), [Kubernetes](https://kubernetes.io/) and [Dask](https://www.dask.org/). 

Airflow has one component called Scheduler responsible for monitoring and triggering tasks. The Scheduler component can be replicated to distribute the workload, so if one goes down, you have others able to run your tasks.

#### 2. Integrations and customizations

Airflow can integrate with many different platforms, you can check them [here](https://registry.astronomer.io/). And it has modules called providers that you can install that bring built-in integrations to the platform. Here are some examples:

* apache-airflow-providers-snowflake
* apache-airflow-providers-amazon

You can also build your own integration if that’s not yet available.

#### 3. Accessibility and dynamism

Airflow leverages the Python programming language so it can be really easy and straightforward to set up a workflow.

#### 4. Monitoring and data lineage capabilities

Airflow provides a built-in integration with [OpenLineage](https://openlineage.io/), that way you can trace the relationships and dependencies between your workflows.

#### 5. Community and support

Airflow is open source and is being updated frequently due to its engaged community.

#### Core Components and Concepts

* WebServer is in charge of setting up a User Interface.
* Meta database contains Airflow metadata, for example task instances statuses and workflows. The Database can be MySQL, Postgres, or others.
* Scheduler is responsible for managing the tasks while checking dependencies.
* Executor defines how and in which system to run the tasks. It can be a Kubernetes or a Celery Executor for example. It pushes the tasks into a queue.
* Worker is a subprocess in charge of executing tasks by pulling them out from the queue.
* Operator triggers tasks.
* DAG (Directed Acyclic Graph) is the core concept of Airflow, collecting tasks together, organized with dependencies and relationships. It doesn’t care about what is happening inside the tasks; it is merely concerned with how to execute them - the order to run them in, how many times to retry them, if they have timeouts, and so on.
   * DAG Run is an object representing an instantiation of the DAG in time. It can have different statuses and it’s independent from one another, so you can have many runs of a DAG at the same time.




