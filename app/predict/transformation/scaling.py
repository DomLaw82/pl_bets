import pandas as pd
from sklearn.preprocessing import StandardScaler
from joblib import dump, load
import numpy as np


def recreate_scaler(X: np.ndarray) -> None:

    scaler = StandardScaler(copy=True).fit(X)    

    dump(scaler, './files/prediction_scaler.bin', compress=True)

def perform_scaling(X_train: np.ndarray, X_test: np.ndarray = np.array([]), no_train: bool = False) -> tuple[np.ndarray, np.ndarray]:
	"""
	Perform scaling on the input data.

	Parameters:
	X_train (list): The training data.
	X_test (list): The testing data.

	Returns:
    	(X_train - np.ndarray, X_test - np.ndarray): The transformed training and testing data after scaling
	"""
	try:
		scaler: StandardScaler = load('files/prediction_scaler.bin')

		if not no_train:
			X_test = scaler.transform(X_test)

		X_train = scaler.transform(X_train)
		
		return X_train, X_test
	except Exception as e:
		raise Exception(e)
