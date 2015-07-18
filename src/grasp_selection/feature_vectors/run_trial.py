import os
import yaml
from dataset_sorter import DatasetSorter
from object_database import Cat50ObjectDatabase
import train_cnn


if __name__ == '__main__':
	feature_db = feature_database.FeatureDatabase()
	caffe_config = caffe_config.CaffeConfig()

	dataset_sorter = feature_db.feature_dataset_sorter()
	if dataset_sorter == None:
		dataset_sorter = DatasetSorter(feature_db)
		feature_db.save_dataset_sorter(dataset_sorter)

	train_cnn.train(feature_db, caffe_config, dataset_sorter)


