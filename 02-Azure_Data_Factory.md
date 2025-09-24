# Azure Data Factory (ADF) – Data Engineer Notes

## 📌 What is ADF?
- **Azure Data Factory (ADF)** is a **cloud-based ETL/ELT and orchestration service**.
- It helps move and transform data between **on-premises, cloud, and SaaS sources**.
- Think of it as **Azure’s version of AWS Glue + Step Functions combined**.

---

## 🏗️ Core Components
- **Pipeline** → Container for workflow.
- **Activities** → Individual steps (Copy, Lookup, Data Flow, etc.).
- **Datasets** → Schema/structure reference to source/target data.
- **Linked Services** → Connection info (DB, Blob, ADLS, API).
- **Integration Runtime (IR)** → Compute engine that executes pipelines.

---

## 🔹 Integration Runtime (IR)
**IR = the worker/bridge that connects and moves data.**

### Types of IR
1. **Azure IR**
   - Fully managed.
   - For cloud-to-cloud transfers.
   - Also spins up **Spark clusters** for Mapping Data Flows.
   - No setup required.

2. **Self-Hosted IR (SHIR)**
   - Installed on an on-premises VM/server.
   - For on-prem → Azure or private network → Azure.
   - Can cluster multiple SHIR nodes.
   - Outbound HTTPS only.

3. **Azure-SSIS IR**
   - Special runtime for running SSIS packages in Azure.

👉 **Simple rule:**  
- Cloud → Cloud = Azure IR  
- On-Prem → Azure = SHIR  
- SSIS migration = Azure-SSIS IR

---

## 🔹 Data Movement
- **Copy Activity** = main activity for ingestion.
- Can extract from on-prem, cloud, or SaaS.
- Can write into ADLS, Blob, SQL DB, Synapse, Cosmos DB, etc.
- **Data Integration Units (DIU):**
  - Controls compute power for Copy Activity in **Azure IR**.
  - More DIU = faster throughput, but higher cost.
  - SHIR performance depends on VM size, not DIU.

---

## 🔹 Data Transformation
- **Mapping Data Flows**
  - Visual ETL on top of Spark clusters.
  - Joins, filters, aggregates, derived columns, sinks.
  - Supports **SCD Type 1 & Type 2** for dimension handling.
- **Wrangling Data Flows**
  - Power Query style.
  - More for data exploration/cleanup.
- **Other options**
  - Call **Databricks Notebook**.
  - Call **Stored Procedure**.
  - Push-down to external compute.

---

## 🔹 Control Flow Activities
- **Lookup** → query or return a value.
- **Get Metadata** → inspect schema, file properties.
- **Set Variable / Append Variable**.
- **If Condition, Switch** → branching logic.
- **ForEach, Until, Wait** → looping & control.
- **Execute Pipeline** → modular design (call sub-pipelines).
- **Validation** → check resources before execution.
- **Error handling paths** → On Success / On Failure / On Completion.

---

## 🔹 Activities for Data Engineers
- **Copy Data** (most common).
- **Lookup** (fetch config/control data).
- **Get Metadata** (check files/tables).
- **ForEach** (loop through files/tables).
- **Data Flow** (transform).
- **Web Activity** (call REST API).
- **Azure Function** (run custom logic).
- **Stored Procedure** (DB-side transformations).
- **Databricks Notebook** (advanced transformations/ML).

---

## 🔹 Triggers
1. **Schedule Trigger**  
   - Runs pipelines on a fixed schedule (like cron jobs).  
   - Fire-and-forget, no monitoring of missed runs.

2. **Event Trigger**  
   - Runs when a blob/file arrives in Blob/ADLS.  
   - Near-real-time ingestion.

3. **Tumbling Window Trigger**  
   - Fixed-size, non-overlapping windows (hourly/daily).  
   - Tracks state (success/failure).  
   - Supports **backfill** (reprocess missed windows).  
   - Supports **dependencies** (N+1 waits until N succeeds).  

👉 **Tumbling = Scheduler + Monitor + Retry + Backfill.**

---

## 🔹 Parameterization & Metadata-Driven Design
- **Pipeline parameters vs variables** → pass dynamic values.
- Parameterize **datasets** (schema, table, file path).
- Parameterize **linked services** (DB name, server).
- Use **Lookup + ForEach + Copy** → one pipeline can ingest 100+ tables.
- Metadata-driven pipelines = best practice for scalability.

---

## 🔹 Optimization in Data Flows
Partitioning strategies:
1. **Round-Robin** → evenly spread rows across partitions.
2. **Hash** → distribute by column hash (best for joins/aggregations).
3. **Dynamic Range** → split by ranges (avoids skew).
4. **Use Current** → keep upstream partitioning.

Other optimizations:
- **Broadcast joins** (when one dataset is small).
- **Skew handling** (split uneven distributions).
- **Cache/reuse** intermediate results.
- **Sink optimization** (batch sizes, partition writes).

---

## 🔹 SCD (Slowly Changing Dimensions)
- **Type 1**: Overwrite → update existing row (no history).
- **Type 2**: Historical → expire old row, insert new row with validity range.
- ADF Mapping Data Flow has **SCD transformation** (supports Type 1 & 2).
- Types 0 & 3 possible with custom logic.

---

## 🔹 UPSERT
- **UPDATE + INSERT** combined.
- If row exists → update. If not → insert.
- Supported in:
  - Azure SQL DB, Synapse (via MERGE).
  - Cosmos DB (via upsert API).
  - Data Flows → Alter Row transformation.
- For file sinks (Blob/ADLS) → no row-level upsert → usually overwrite files.

---

## 🔹 Monitoring
- **Monitor dashboard in ADF Studio**:
  - Pipeline Runs (success/failure, reruns).
  - Trigger Runs.
  - Activity Runs (drill down).
  - Integration Runtime health (CPU, memory).
- Integrates with **Azure Monitor / Log Analytics** for alerts.
- Can notify via Email, Teams, Webhook.

---

## 🔹 Security
- Linked Service authentication:
  - **Access Keys** (root credentials).
  - **SAS Tokens** (delegated, time-bound).
  - **Service Principal / Managed Identity** (best practice).
- Integrate with **Azure Key Vault** for secret storage.
- Use **RBAC** + **Private Endpoints** for network security.

---

## 🔹 CI/CD & Deployment
- Best practice → separate ADF per environment:
  - **Dev**, **Test/QA**, **Prod**.
- Use **Git Integration** with ADF Studio:
  - Work in feature branches.
  - Merge to main → publish.
- **ARM Templates**:
  - Exported from Dev.
  - Deployed into Test/Prod via **Azure DevOps Pipelines** or **GitHub Actions**.
- Override **parameters** (e.g., storage account, DB connection).
- IR per environment (esp. SHIR).

---

## 🔹 Best Practices
- Metadata-driven pipelines (control tables/files).
- Modular pipelines → avoid monolithic.
- Handle schema drift.
- Implement error handling & logging.
- Monitor and alert on failures.
- Optimize cost:
  - Use **parallelism** before scaling DIUs.
  - Use **Parquet** for analytics.
  - Archive old data (Hot → Cool → Archive tiers).

---

## 🔹 ADF Flowchart
flowchart LR
    SRC[Source system]
    LSSRC[Linked service - source]
    DSSRC[Source dataset]
    ACT[ADF activity: Copy or Transform]
    DSTGT[Sink dataset]
    LSTGT[Linked service - target]
    TGT[Target system]

    SRC --> LSSRC --> DSSRC --> ACT --> DSTGT --> LSTGT --> TGT

---

## 🔹 AWS vs Azure Mapping (Quick Reference)
| AWS | Azure |
|-----|-------|
| **S3** | **Blob/ADLS** |
| **Athena** | **Synapse Serverless SQL Pools** |
| **Redshift** | **Synapse Dedicated Pools** |
| **Glue** | **ADF Pipelines** |
| **Glue Jobs (Spark)** | **ADF Data Flows / Databricks** |
| **Lake Formation** | **ADLS + RBAC/ACLs** |
| **DMS** | **ADF SHIR / Azure Migration Services** |

---

## ✅ Key Takeaways
- **ADF = Orchestration + ETL service.**
- **IR = worker/connector** (Azure IR, Self-Hosted IR, SSIS IR).
- **Copy Activity** = ingestion; **Data Flow** = transformation.
- **Triggers** = schedule, event, tumbling window.
- **Optimize** with partitioning, parallelism, staged copy, DIUs.
- **Deployment** = Git + ARM templates → Dev/Test/Prod.
- **Security** = Managed Identity + Key Vault.
- **Monitoring** = ADF Monitor + Azure Monitor integration.

---
