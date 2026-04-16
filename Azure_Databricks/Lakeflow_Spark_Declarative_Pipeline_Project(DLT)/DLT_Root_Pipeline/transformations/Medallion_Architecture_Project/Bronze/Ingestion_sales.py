import dlt

sales_rules = {"rule_1": "sales_id IS NOT NULL"}

dlt.create_streaming_table(
    name="sales_stg",
    expect_all_or_drop= dict(sales_rules)
)

@dlt.append_flow(target="sales_stg")
def east_sales():
    """Ingest sales data from the East region into the Bronze layer.

    Reads streaming sales data from the East region source table
    and appends it to the sales_stg target table.

    Returns:
        DataFrame: Streaming DataFrame containing East region sales records.
    """
    df = spark.readStream.table("nagadatabricks.source.sales_east")
    return df

@dlt.append_flow(target="sales_stg")
def west_sales():
    """Ingest sales data from the West region into the Bronze layer.

    Reads streaming sales data from the West region source table
    and appends it to the sales_stg target table.

    Returns:
        DataFrame: Streaming DataFrame containing West region sales records.
    """
    df = spark.readStream.table("nagadatabricks.source.sales_west")
    return df