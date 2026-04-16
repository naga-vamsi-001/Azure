import dlt

#Customers Expectations
customers_rules = {
    "rule_1": "customer_id IS NOT NULL",
    "rule_2": "customer_name IS NOT NULL"
}

@dlt.table(
    name = "customers_stg"
)
@dlt.expect_all_or_drop(customers_rules)

def customers_stg():
    """Ingest customer data from the source into the Bronze layer.

    Reads streaming customer data from the source table and applies
    data quality expectations (customer_id and customer_name NOT NULL).

    Returns:
        DataFrame: Streaming DataFrame containing customer records.
    """
    df = spark.readStream.table("nagadatabricks.source.customers")
    return df