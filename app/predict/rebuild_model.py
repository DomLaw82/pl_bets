from dataset_creation.create_dataset import create_dataset
from neural_net.build_and_save_model import build_and_save_model

def rebuild_model():
	create_dataset()
	# TODO: Add combined dataframe as argument here so path is consistent
	build_and_save_model()
	# TODO: model to be returned from build_and_save_model, save model in this script