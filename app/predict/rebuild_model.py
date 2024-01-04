from dataset_creation.create_dataset import create_dataset
from neural_net.build_and_save_model import build_and_save_model

def rebuild_model():
	create_dataset()
	build_and_save_model()