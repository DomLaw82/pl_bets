from dataset_creation.create_dataset import create_dataset
from neural_net.build_and_save_model import build_and_save_model

def rebuild_model():
	"""
	Rebuilds the model by creating a dataset, building the model,
	and then saving it as "stats_regression_model.h5".

	Returns:
		None
	"""
	dataset = create_dataset()
	model = build_and_save_model(dataset)
	model.save("stats_regression_model.h5")