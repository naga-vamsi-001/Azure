import dlt
from pyspark.sql.functions import *

@dlt.table(
    name = "staging_orders"
)
  
def staging_orders():
    """Create a staging table for raw order data ingestion.

    Reads streaming order data from the source into a staging area
    for initial processing and validation.

    Returns:
        DataFrame: Streaming DataFrame containing raw order records.
    """
    df = spark.readStream.table("nagadatabricks.source.orders")
    return df

#Creating Transformed Area
@dlt.view(
    name = "transformed_orders"
)

def transformed_orders():
    """Transform order data by normalizing order status to lowercase.

    Reads staging orders and applies transformations to standardize
    the order_status column by converting to lowercase.

    Returns:
        DataFrame: Transformed DataFrame with normalized order_status values.
    """
    df = spark.readStream.table("staging_orders")
    df = df.withColumn("order_status",lower(col("order_status")))
    return df

#Creating Aggregated Area

@dlt.table(
    name= "aggregated_orders"
)
def aggregated_orders():
    """Aggregate order counts by order status.

    Reads transformed orders and groups by order_status, calculating
    the count of orders for each status. Used for analytics and reporting.

    Returns:
        DataFrame: Aggregated DataFrame with columns: order_status, count.
    """
    df = spark.readStream.table("transformed_orders")
    df = df.groupBy("order_status").count()
    return df