import dlt

#Create Empty Streaming Table
dlt.create_streaming_table(
    name= "Fact_Sales"
)


#Creating Auto CDC flow
dlt.create_auto_cdc_flow(
  target = "Fact_Sales",
  source = "sales_stage_transformation_view",
  keys = ["sales_id"],
  sequence_by = "sale_timestamp",
  apply_as_deletes = None,
  except_column_list = None,
  stored_as_scd_type = "2",
  track_history_except_column_list = None
)