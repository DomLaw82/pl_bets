from neural_net.tune_model_params import tune_model_params
from neural_net.build_and_save_model import build_and_save_model
from dataset_creation.create_dataset import create_dataset

create_dataset()
tune_model_params()
build_and_save_model()
