from pandas import DataFrame, merge

def remove_duplicate_rows(connector, df:DataFrame, columns:list, table_name:str) -> DataFrame:
	all_data_df = connector.get_df(f"SELECT {', '.join(columns)} FROM {table_name}")

	unique_df = merge(df, all_data_df, on=columns, how='outer', indicator=True).loc[lambda x: x['_merge'] == 'left_only'].drop(columns=["_merge"])

	return unique_df