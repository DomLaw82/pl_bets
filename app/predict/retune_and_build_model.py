from neural_net.tune_model_params import tune_model_params
from neural_net.build_and_save_model import build_and_save_model
from dataset_creation.create_dataset import create_dataset
from transformation.pca import recreate_pca_object
from transformation.scaling import recreate_scaler

def retune_and_build_model():
	"""
	Re-tunes the model parameters, builds and saves the model, and returns the score and parameters.

	Returns:
		score (float): The score of the model.
		params (dict): The tuned parameters of the model.
	"""
	try:
		dataset = create_dataset()
		dataset.to_csv("./files/final_combined_dataframe.csv", index=False)
		X_scaled = recreate_scaler()
		recreate_pca_object(data=X_scaled)
		score, params = tune_model_params(dataset)
		model = build_and_save_model(dataset)
		model.save("files/stats_regression_model.h5")
		return {"score": score, "params": params}
	except Exception as e:
		return {'error': str(e)}
