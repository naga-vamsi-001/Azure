# Azure Databricks – Data Engineer Notes

## 📌 What is Databricks?
- **Azure Databricks** = a **cloud-based big data + AI platform**, built on **Apache Spark**.
- Provides an **interactive workspace** for data engineers, data scientists, and analysts.
- Key capabilities:
  - **Data Engineering** → ETL/ELT pipelines on big data.
  - **Data Science & ML** → MLflow, TensorFlow, PyTorch, Scikit-learn.
  - **Analytics** → SQL queries, dashboards.
- Deep integration with **Azure services (ADLS, Synapse, ADF, Power BI).**

---

## 🏗️ Core Components
- **Workspace** → Shared UI environment for users and notebooks.
- **Notebooks** → Interactive coding in Python, SQL, Scala, or R.
- **Clusters** → Spark compute resources (single-node or multi-node).
- **Jobs (Workflows)** → Orchestrated tasks (schedule notebooks, scripts).
- **DBFS (Databricks File System)** → Built-in distributed storage.
- **Unity Catalog** → Central governance, security, lineage.

---

## 🔹 Personas
- **Data Engineering view** → ETL, data prep.
- **Machine Learning view** → MLflow, training, experiments.
- **SQL view** → BI, SQL queries, dashboards.

---

## 🔹 Databricks Runtime (DBR)
- **Software stack** that runs on each cluster.
- Includes **Apache Spark + Delta Lake + libraries**.
- **Types of Runtimes**:
  1. **Standard** → General-purpose Spark.
  2. **ML Runtime** → Adds TensorFlow, PyTorch, MLflow.
  3. **Genomics Runtime** → Specialized libraries for bioinformatics.
  4. **Light Runtime** → Lightweight Spark, lower-cost.
- **LTS (Long-Term Support)** versions → stable for production.

---

## 🔹 Workspace
- **Users folder** → personal notebooks.
- **Shared folder** → team collaboration area.
- Organize into **directories/projects**.

---

## 🔹 Notebooks
- Multi-language support: **Python, SQL, R, Scala**.
- Attach notebooks to a cluster for execution.
- Rich visualization and built-in commands like:
  - `spark` → SparkSession (auto-created).
  - `sc` → SparkContext.
  - `dbutils` → utilities for FS, secrets, widgets.
  - `display(df)` → pretty tables/charts.

---

## 🔹 Clusters
- **Single Node Cluster**
  - Driver + Worker on same VM.
  - Best for dev/testing, small jobs.
- **Multi-Node Cluster**
  - Driver + multiple workers.
  - Supports autoscaling and parallelism.
- **Cluster Access Modes**
  1. **Single User (Isolation)** → only one user/job runs.
  2. **Shared Access** → multiple users share, supports Unity Catalog.
  3. **Legacy (No Isolation)** → older mode, not recommended.
- **Cluster Pools**
  - Pre-warmed VMs to reduce startup time.
  - Used with job clusters for faster execution.

---

## 🔹 Nodes & Spot Instances
- **Driver Node** → coordinates the Spark job (always keep on-demand).
- **Worker Nodes** → execute tasks (can be spot to save cost).
- **Spot Instance**
  - Discounted VM (up to 80% cheaper).
  - Can be evicted anytime if Azure needs capacity.
  - Best for workers, not drivers.
  - Good for ETL, stateless jobs.

---

## 🔹 Data Access
### Mounting ADLS/Blob
1. **Access Key** (not secure, dev only).
2. **SAS Token** (time-limited).
3. **Service Principal (OAuth)** → best practice for production.
4. **Direct `abfss://` access** → recommended with Unity Catalog + RBAC.

```python
# Example: Service Principal OAuth mount
configs = {
  "fs.azure.account.auth.type": "OAuth",
  "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
  "fs.azure.account.oauth2.client.id": "<client-id>",
  "fs.azure.account.oauth2.client.secret": dbutils.secrets.get(scope="myscope", key="mysecret"),
  "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/<tenant-id>/oauth2/token"
}

dbutils.fs.mount(
  source = "abfss://raw@mydatalake.dfs.core.windows.net/",
  mount_point = "/mnt/raw",
  extra_configs = configs
)
```

---

## 🔹 Views in Databricks (Spark SQL)
- **Temporary View** (`createOrReplaceTempView`) → session-scoped, vanishes after cluster stops.
- **Global Temporary View** (`createOrReplaceGlobalTempView`) → lives in `global_temp` DB, accessible across notebooks in same cluster.
- **Permanent View** (`CREATE VIEW`) → stored in metastore/Unity Catalog, persists across sessions.
- **Replace Temp View** → overwrites an existing temp view.

---

## 🔹 Sample Datasets
- Available at `/databricks-datasets/`.
- Examples:
  - `/databricks-datasets/airlines/`
  - `/databricks-datasets/nyctaxi/`
  - `/databricks-datasets/COVID/`

```python
df = spark.read.csv("/databricks-datasets/airlines/part-00000", header=True, inferSchema=True)
df.show(5)
```

---

## 🔹 Workflows (Jobs)
- **Jobs** = way to schedule and orchestrate work.
- Can run:
  - Notebooks
  - JARs
  - Python scripts
  - SQL queries
- **Job Clusters** (ephemeral) vs **Existing Clusters** (interactive).
- Supports retries, notifications, dependencies.

---

## 🔹 Integration with ADF
Ways to run Databricks from ADF:
1. **Native Activity** → Databricks Notebook, Python, JAR activity.
2. **REST API** → call Databricks Jobs API with Web Activity.
3. **Azure Function/Logic App** → ADF triggers function, which triggers Databricks.

Cluster options in ADF:
- **New Job Cluster** → clean, reproducible (best for Prod).
- **Existing Cluster** → fast startup (best for Dev).
- **Cluster Pool** → faster startup by reusing warm VMs.

---

## 🔹 Unity Catalog
- Central governance & metadata layer for Databricks.
- Manages **tables, views, schemas, functions, ML models**.
- Features:
  - Fine-grained **security (row, column-level)**.
  - **Data lineage** tracking.
  - **Cross-workspace access** (one catalog for all).
- Uses **3-level namespace**:
  ```
  catalog.schema.table
  ```
  Example:
  ```sql
  SELECT * FROM main.sales.customers;
  ```

---

## 🔹 Best Practices
- Use **Job Clusters** for production workloads.
- Keep **driver node on-demand**, workers can be spot.
- Prefer **Service Principal + Key Vault** for mounts.
- Use **Delta Lake** instead of raw Parquet/CSV.
- Organize workspace with **Shared** (team) and **Users** (personal).
- Implement governance with **Unity Catalog**.
- Monitor jobs with **Jobs UI + ADF Monitor**.
- Optimize with autoscaling, partitioning, caching.

---

## ✅ Key Takeaways
- **Databricks = Spark + Collaboration + Cloud integration.**
- **Databricks Runtime (DBR)** defines the software stack (Spark + Delta + libs).
- **Clusters** = compute backbone (Single/Multi-node, job vs interactive).
- **Spot workers save cost, but driver should stay on-demand.**
- **Mount ADLS securely** with Service Principal or direct ABFS.
- **Unity Catalog** = central metadata + governance + security.
- **ADF + Databricks** work together for enterprise pipelines.
