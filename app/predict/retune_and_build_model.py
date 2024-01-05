from neural_net.tune_model_params import tune_model_params
from neural_net.build_and_save_model import build_and_save_model
from dataset_creation.create_dataset import create_dataset

def retune_and_build_model():
	create_dataset()
	# TODO: Add combined dataframe as argument here so path is consistent, as dataframe will be change tot be the output of create_dataset
	score, params = tune_model_params()
	build_and_save_model()
	# TODO: model to be returned from build_and_save_model, save model in this script
	return score, params
