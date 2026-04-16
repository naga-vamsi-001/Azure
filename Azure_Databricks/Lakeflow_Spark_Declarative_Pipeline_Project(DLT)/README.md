# Databricks Declarative Pipelines (DLT)

## 1. Overview
Databricks Declarative Pipelines, still commonly called **Delta Live Tables (DLT)**, is Databricks' managed framework for building **batch and streaming data pipelines** in **SQL or Python**. In current naming, the broader product direction is **Lakeflow Declarative Pipelines**.

The model is declarative: define datasets, transformations, and dependencies; Databricks manages execution order, refresh behavior, incremental processing, and monitoring.

## 2. Why teams use DLT
- **Data quality with Expectations**: define rules such as `policy_id IS NOT NULL` or `premium_amount > 0`
- **Automatic dependency management**: Databricks determines the correct execution order from lineage
- **Incremental processing**: process only new or changed data when possible
- **Unified batch and streaming**: support both in one framework
- **Reduced orchestration code**: fewer manual jobs, retries, and dependency chains
- **Built-in visibility**: event logs, metrics, and monitoring in the platform

## 3. DLT vs traditional Spark jobs
| Area | Traditional Spark Jobs | DLT |
|---|---|---|
| Dependency ordering | Manual | Automatic |
| Data quality | Custom code | Expectations |
| CDC handling | MERGE/custom logic | AUTO CDC |
| Batch + streaming | Separate patterns | Unified framework |
| Monitoring | Manual/external | Built-in pipeline monitoring |

DLT uses Spark, but adds a managed pipeline layer on top of it.

## 4. Workspace and editor structure
A separate dedicated workspace is **not** required. A normal Databricks workspace is enough.

Common project folders:
- **transformations**: SQL/Python pipeline logic evaluated during execution
- **explorations**: notebooks, experiments, ad hoc analysis
- **utilities**: helper functions or reusable modules

Teams often create subfolders under `transformations` by domain, source system, or medallion layer.

## 5. Main dataset types
### Streaming table
A **streaming table** processes data **incrementally** as new records arrive. Use it for Auto Loader, Kafka, Event Hubs, and append-style sources. Key point: it handles **new arriving data**, not simply “latest snapshot rows.”

### Materialized view
A **materialized view** stores the result of a query as a **physical dataset**. Use it for batch-style transformations, aggregations, and reporting-ready outputs. Key point: it is physically stored and refreshed by the pipeline.

### Temporary view
A **temporary view** is an intermediate logical step inside the pipeline. Use it to break large transformations into smaller, cleaner stages.

## 6. Dataset type comparison
| Type | Storage | Best use |
|---|---|---|
| Streaming table | Physical | Incremental ingestion and streaming-style processing |
| Materialized view | Physical | Batch-style outputs, aggregations, serving/reporting layers |
| Temporary view | Logical/intermediate | Reusable transformation steps inside the pipeline |

Memory trick: **Streaming table = new incoming data; Materialized view = stored query result; Temporary view = intermediate logic.**

## 7. Expectations and data quality
**Expectations** are built-in data quality rules in DLT.

Examples:
- `policy_id IS NOT NULL`
- `premium_amount > 0`
- `application_date <= current_date()`

Typical actions for invalid data:
- track as warnings
- drop invalid records
- fail the pipeline

A quarantine design can also be implemented by routing bad records into a separate dataset.

![expectations.png](https://raw.githubusercontent.com/naga-vamsi-001/Images/main/DLT_project/expectations.png)

## 8. Flows in DLT
A pipeline is not only tables and views; it also includes how data is written into targets.

- **Append flow**: append data into a target streaming table
- **Once flow**: process data one time, not continuously
- **AUTO CDC flow**: apply insert, update, and delete changes into a target streaming table

Common append pattern: create an empty target streaming table, then use multiple append flows to load sources such as `EAST_table` and `WEST_table` into the same target.

## 9. Append vs upsert vs overwrite
- **Append**: only add new rows
- **Upsert**: update existing matching rows and insert new non-matching rows
- **Overwrite**: replace the target dataset with a new result set

## 10. Upsert and MERGE
An **upsert** means update the row if it exists and insert it if it does not. In Delta Lake, upserts are commonly implemented with **MERGE**.

Example: target has `id=2, name=Mary`; source has `id=2, name=Maria` and `id=3, name=David`; result: row 2 is updated, row 3 is inserted.

## 11. What AUTO CDC is
**AUTO CDC** stands for **Automatic Change Data Capture**. It is related to upsert, but broader than upsert.

AUTO CDC can handle:
- inserts
- updates
- deletes
- event sequencing
- SCD Type 1
- SCD Type 2

So:
- **Upsert** = insert + update
- **AUTO CDC** = insert + update + delete + sequencing + SCD handling

AUTO CDC is the recommended DLT approach for CDC-style pipelines.

## 12. Key AUTO CDC concepts
- **target**: target streaming table receiving the applied changes
- **source**: CDC source dataset, often a DLT view
- **keys**: business key columns identifying the same row across events
- **sequence_by**: column used to order CDC events correctly
- **apply_as_deletes**: condition identifying delete events
- **apply_as_truncates**: condition identifying truncate events
- **except_column_list**: processing columns excluded from final target output, such as `operation` or `sequenceNum`
- **stored_as_scd_type**: whether DLT stores **Type 1** current-state data or **Type 2** historical versions

## 13. SCD Type 1 vs Type 2
- **SCD Type 1**: overwrites the old value; no history is kept
- **SCD Type 2**: preserves historical versions over time

Use Type 1 when only the latest state matters. Use Type 2 when audit history or point-in-time tracking is required.

## 14. AUTO CDC from snapshot
When the source system does **not** provide CDC events but does provide periodic snapshots, Databricks also supports **AUTO CDC FROM SNAPSHOT** patterns. This is useful when change tracking is needed without a native CDC feed.

## 15. Auto Loader in DLT
Many real DLT pipelines start with **Auto Loader** for incremental ingestion from cloud storage. Common use cases include JSON, CSV, Parquet, or Avro files landing in ADLS, S3, or other cloud object storage.

## 16. Schema evolution
DLT pipelines often need to handle changing source schemas such as new columns, optional fields, evolving nested structures, or source-format changes over time.

## 17. Monitoring and troubleshooting
Important operational areas:
- pipeline status
- event logs
- expectation metrics
- refresh history
- errors and warnings
- lineage context

The **event log** is one of the most useful places for troubleshooting pipeline behavior.

## 18. Refresh behavior
Understand how datasets refresh:
- streaming tables process new data incrementally
- materialized views refresh stored query results based on upstream changes
- configuration or logic changes can sometimes trigger recomputation

This matters for performance, cost, and debugging.

## 19. Best-practice guidance
Use:
- **streaming tables** for ingestion and incremental data arrival
- **materialized views** for batch-style outputs and reporting layers
- **temporary views** for intermediate logic
- **AUTO CDC** when the source sends inserts, updates, and deletes
- **append flows** when multiple sources feed a single target and only appends are needed

## 20. Summary
Databricks Declarative Pipelines, also known as DLT, is a managed framework for building reliable batch and streaming pipelines in SQL or Python. It simplifies dependency management, data quality enforcement, CDC processing, monitoring, and incremental processing. The main dataset types are streaming tables, materialized views, and temporary views. For CDC, Databricks recommends AUTO CDC, which goes beyond simple upserts by handling deletes, sequencing, and SCD Type 1 or Type 2 logic. In real projects, DLT is commonly used with Auto Loader, schema evolution handling, medallion architecture, and event-log-based monitoring.
