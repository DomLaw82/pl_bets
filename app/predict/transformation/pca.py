import pandas as pd
from sklearn.decomposition import PCA
from joblib import dump
import numpy as np

def create_pca_object(n:int, df:pd.DataFrame) -> PCA:
	pca = PCA(n_components = n, random_state=938)
	pca.fit(df)
	return pca

def recreate_pca_object(columns: list, n:int = 15, data:np.array = None):
	df = data
	pca_obj = create_pca_object(n, df)
	feature_to_pc_map = pd.DataFrame(pca_obj.components_, columns=columns)
	feature_to_pc_map.to_csv("./files/feature_to_15_pcs.csv", index=False)