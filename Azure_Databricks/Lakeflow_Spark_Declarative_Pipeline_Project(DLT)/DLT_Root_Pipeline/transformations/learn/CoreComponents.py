import dlt

#Creating a Streaming Table
@dlt.table(
  name="streaming_table"
)
def streaming_table():
    '''This table only read lastest data from the source,
        for example day 1 we have 10 records and day 2 we have 20 records so the 
        streaming table will only read the latest 20 records.'''

    df = spark.readStream.table("nagadatabricks.source.orders")
    return df

#Creating a Materialized view 
@dlt.table(
    name = "materialized_view"
  )
def materialized_view():
    '''This view will read all the data from the source, 
        for example day 1 we have 10 records and day 2 we have 15 records so 
        the  materialized view will read all 35 records.'''
    
    df = spark.readStream.table("nagadatabricks.source.orders")
    return df

#Creating a Batch view
@dlt.table(
  name="batch_view"
)
def batch_view():
  """Create a batch view for non-streaming data processing.

  Reads order data from the source in batch mode (not streaming).
  Suitable for one-time loads or periodic batch processing.

  Returns:
      DataFrame: Batch DataFrame containing order records.
  """
  df = spark.read.table("nagadatabricks.source.orders")
  return df

#Creating a Streaming view
@dlt.view(
  name="streaming_view"
)
def streaming_view():
  """Create a streaming view for real-time data processing.

  Reads order data from the source in streaming mode, enabling
  real-time processing of incoming records.

  Returns:
      DataFrame: Streaming DataFrame containing order records.
  """
  df = spark.readStream.table("nagadatabricks.source.orders")
  return df