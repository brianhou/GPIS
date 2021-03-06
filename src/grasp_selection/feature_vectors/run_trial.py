import train_cnn
from dataset_sorter import DatasetSorter
from feature_database import FeatureDatabase
from caffe_config import CaffeConfig
import sys
sys.path.insert(0, 'src/grasp_selection/')
import experiment_config as ec

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('config')
	args = parser.parse_args()
	config = ec.ExperimentConfig(args.config)

	feature_db = feature_database.FeatureDatabase(config)

	caffe_config = CaffeConfig()

	dataset_sorter = feature_db.feature_dataset_sorter()
	if dataset_sorter == None:
		dataset_sorter = DatasetSorter(feature_db)
		feature_db.save_dataset_sorter(dataset_sorter)

	train_cnn.train(feature_db, caffe_config, dataset_sorter)


