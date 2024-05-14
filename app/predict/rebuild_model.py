from dataset_creation.create_dataset import create_dataset
from neural_net.build_and_save_model import build_and_save_model
from transformation.pca import recreate_pca_object
from transformation.scaling import recreate_scaler

def rebuild_model():
	"""
	Rebuilds the model by creating a dataset, building the model,
	and then saving it as "stats_regression_model.h5".

	Returns:
		None
	"""
	try:
		dataset = create_dataset()
		dataset.to_csv("./files/final_combined_dataframe.csv", index=False)
		recreate_scaler()
		recreate_pca_object()
		model = build_and_save_model(dataset)
		model.save("files/stats_regression_model.h5")
		return {'message': 'Model rebuilt'}
	except Exception as e:
		return {'error': str(e)}
