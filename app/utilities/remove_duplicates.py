from pandas import DataFrame

def remove_duplicate_rows(connector, df:DataFrame, columns:list, table_name:str) -> DataFrame:
	all_data_df = connector.get_list(f"SELECT {', '.join(columns)} FROM {table_name}")
	return df[~df[columns].isin(all_data_df.to_dict('list')).all(1)]