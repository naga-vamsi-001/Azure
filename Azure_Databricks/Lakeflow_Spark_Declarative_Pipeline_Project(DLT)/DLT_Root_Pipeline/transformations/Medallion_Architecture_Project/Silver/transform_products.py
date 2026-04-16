import dlt
from pyspark.sql.functions import *
from pyspark.sql.types import *

#Transforming Sales Data
@dlt.view(
    name = "product_stage_transformation_view"
)

def sales_stage_transformation():
    """Transform product data from Bronze to Silver layer.

    Reads streaming product data from the Bronze layer and applies
    transformations including casting price values to Integer type.
    Creates a view for further processing in the Auto CDC flow.

    Returns:
        DataFrame: Transformed DataFrame with price values cast to Integer.
    """
    df = spark.readStream.table("products_stg")
    df = df.withColumn("price", col("price").cast(IntegerType()))
    return df

#Creating Destination Silver table
dlt.create_streaming_table(
    name = "products_enriched"
)

#Creating Auto CDC flow
dlt.create_auto_cdc_flow(
  target = "products_enriched",
  source = "product_stage_transformation_view",
  keys = ["product_id"],
  sequence_by = "last_updated",
  apply_as_deletes = None,
  except_column_list = None,
  stored_as_scd_type = "1",
  track_history_except_column_list = None
)