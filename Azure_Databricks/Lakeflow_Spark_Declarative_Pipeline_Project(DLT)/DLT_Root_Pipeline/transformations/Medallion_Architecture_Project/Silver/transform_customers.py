import dlt
from pyspark.sql.functions import *
from pyspark.sql.types import *

#Transforming Sales Data
@dlt.view(
    name = "customer_stage_transformation_view"
)

def sales_stage_transformation():
    df = spark.readStream.table("customers_stg")
    df = df.withColumn("customer_name", upper(col("customer_name")))
    return df

#Creating Destination Silver table
dlt.create_streaming_table(
    name = "customers_enriched"
)

#Creating Auto CDC flow
dlt.create_auto_cdc_flow(
  target = "customers_enriched",
  source = "customer_stage_transformation_view",
  keys = ["customer_id"],
  sequence_by = "last_updated",
  apply_as_deletes = None,
  except_column_list = None,
  stored_as_scd_type = "1",
  track_history_except_column_list = None
)