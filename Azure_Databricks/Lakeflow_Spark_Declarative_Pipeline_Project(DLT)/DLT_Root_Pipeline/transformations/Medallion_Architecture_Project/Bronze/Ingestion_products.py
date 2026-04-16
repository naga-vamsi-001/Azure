import dlt

#Product Expectations
product_rules = {
    "rule_1": "product_id IS NOT NULL",
    "rule_2": "price >= 0"
}

#Ingesting Products
@dlt.table(name= "products_stg")
@dlt.expect_all_or_drop(product_rules)

def products_stg():
    """Ingest product data from the source into the Bronze layer.

    Reads streaming product data from the source table and applies
    data quality expectations (product_id NOT NULL and price >= 0).

    Returns:
        DataFrame: Streaming DataFrame containing product records.
    """
    df = spark.readStream.table("nagadatabricks.source.products")
    return df