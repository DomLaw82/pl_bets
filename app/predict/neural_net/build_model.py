import numpy as np
import tensorflow as tf
import os
from define_environment import load_correct_environment_variables

load_correct_environment_variables()

N = 15

# TODO: Identify and handle outliers in your data, as they can significantly impact model performance.
# TODO: Test decreasing the number of neurons in the hidden layer to see if the model performs better.

def get_model(input_length: int, output_length: int, hidden_layers: list, dropout: float, learn_rate: float) -> tf.keras.models.Sequential:
	"""
	Creates a neural network model with the specified parameters.

	Parameters:
	input_length (int): Number of input features.
	output_length (int): Number of output features.
	hidden_layers (list[int]): Number of units in each hidden layer.
	dropout (float): Dropout rate, a fraction of the input units to drop.
	learn_rate (float): Learning rate for the optimizer.

	Returns:
	tf.keras.models.Sequential: The compiled neural network model.
	"""
	try:
		model = tf.keras.models.Sequential()
		model.add(tf.keras.layers.Dense(input_length, activation="relu", input_dim=input_length))

		for i in hidden_layers:
			model.add(tf.keras.layers.Dense(i, activation="relu"))

		model.add(tf.keras.layers.Dropout(dropout))
		model.add(tf.keras.layers.Dense(output_length, activation="relu"))

		model.compile(
			optimizer=tf.keras.optimizers.legacy.Adam(learning_rate=learn_rate),
			loss="mse",
			metrics=["accuracy"])

		return model
	except Exception as e:
		raise Exception(e)

def build_model(X: np.ndarray, y: np.ndarray) -> tf.keras.models.Sequential:
	"""
	Builds and saves a machine learning model using the provided dataframe.

	Args:
		dataframe (pd.DataFrame): The input dataframe containing the training data.

	Returns:
		tf.keras.models.Sequential: The trained machine learning model.
	"""
	try:
		# Get model parameters from environment variables
		hidden_layers = [int(i) for i in os.environ.get('hidden_layers').replace('[', '').replace(']', '').split(",")]
		learn_rate = float(os.environ.get('learn_rate'))
		dropout = float(os.environ.get('dropout'))
		batch_size = int(os.environ.get('batch_size'))
		epochs = int(os.environ.get('epochs'))
		print(f"Building model with parameters: hidden_layers={hidden_layers}, learn_rate={learn_rate}, dropout={dropout}, batch_size={batch_size}, epochs={epochs}")

		# Define fit, and save the model
		model = get_model(X.shape[1], y.shape[1], hidden_layers, dropout, learn_rate)

		model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=1)

		return model
	except Exception as e:
		raise Exception(e)