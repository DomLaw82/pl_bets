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
	dataset = create_dataset()
	dataset.to_csv("../final_combined_dataframe.csv", index=False)
	recreate_scaler()
	recreate_pca_object()
	model = build_and_save_model(dataset)
	model.save("stats_regression_model.h5")