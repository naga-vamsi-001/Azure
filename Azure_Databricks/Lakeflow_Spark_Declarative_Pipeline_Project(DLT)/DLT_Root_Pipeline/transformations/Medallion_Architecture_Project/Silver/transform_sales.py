import dlt
from pyspark.sql.functions import *

#Transforming Sales Data
@dlt.view(
    name = "sales_stage_transformation_view"
)

def sales_stage_transformation():
    df = spark.readStream.table("sales_stg")
    df = df.withColumn("total_amount", col("quantity") * col("amount"))
    return df

#Creating Destination Silver table
dlt.create_streaming_table(
    name = "sales_enriched"
)

#Creating Auto CDC flow
dlt.create_auto_cdc_flow(
  target = "sales_enriched",
  source = "sales_stage_transformation_view",
  keys = ["sales_id"],
  sequence_by = "sale_timestamp",
  apply_as_deletes = None,
  except_column_list = None,
  stored_as_scd_type = "1",
  track_history_except_column_list = None
)