from pandas import DataFrame, merge

def remove_duplicate_rows(connector, df:DataFrame, columns:list, table_name:str) -> DataFrame:
	try:
		all_data_df = connector.get_df(f"SELECT {', '.join(columns)} FROM {table_name}")

		if table_name == 'schedule':
			duplicate_rows = merge(df, all_data_df, on=columns, how='inner', indicator=True).loc[lambda x: x['_merge'] == 'both']
			for index, row in duplicate_rows.iterrows():
				update_query = f"UPDATE {table_name} SET result = {row['result']} WHERE " + ', '.join([f"{column} = {row[column]}" for column in columns])
				connector.execute(update_query)

		unique_df = merge(df, all_data_df, on=columns, how='outer', indicator=True).loc[lambda x: x['_merge'] == 'left_only'].drop(columns=["_merge"])

		return unique_df
	except Exception as e:
		print(f"Error: {e}")
		return df