from neural_net.tune_model_params import tune_model_params
from neural_net.build_and_save_model import build_and_save_model
from dataset_creation.create_dataset import create_dataset

def retune_and_build_model():
	create_dataset()
	score, params = tune_model_params()
	build_and_save_model()
	return score, params
