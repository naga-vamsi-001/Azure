import dlt

#Create Empty Streaming Table
dlt.create_streaming_table(
    name= "Dim_Customer"
)

#Auto CDC FLOW
dlt.create_auto_cdc_flow(
  target = "Dim_Customer",
  source = "customer_stage_transformation_view",
  keys = ["customer_id"],
  sequence_by = "last_updated",
  apply_as_deletes = None,
  except_column_list = None,
  stored_as_scd_type = "2",
  track_history_except_column_list = None
)