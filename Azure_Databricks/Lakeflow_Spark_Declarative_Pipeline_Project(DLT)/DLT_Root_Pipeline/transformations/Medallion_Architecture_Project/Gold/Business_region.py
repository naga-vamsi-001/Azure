import dlt
from pyspark.sql.functions import *


#Creating a Materialzed View
@dlt.table(
    name = "business_sales"
)

def business_sales():
  """Create a materialized view aggregating sales by region and category.

  Joins the fact_sales table with dimension tables (dim_customer and
  dim_product) and aggregates total sales by region and product category.
  Used for business analytics and reporting purposes.

  Returns:
      DataFrame: Aggregated DataFrame with columns: region, category, total_sales.
  """
  df_fact = spark.read.table("fact_sales")
  df_dimCust = spark.read.table("dim_customer")
  df_dimProd = spark.read.table("dim_product")

  df_join = df_fact.join(df_dimCust, df_fact.customer_id == df_dimCust.customer_id, "inner").join\
  (df_dimProd, df_fact.product_id == df_dimProd.product_id, "inner")

  df_prun = df_join.select("region", "category", "total_amount")

  df_agg = df_prun.groupBy("region", "category").agg(sum("total_amount").alias("total_sales"))

  return df_agg


