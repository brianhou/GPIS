import argparse
import copy
import logging
import pickle as pkl
import os
import random
import string
import time

import IPython
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

import antipodal_grasp_sampler as ags
import database as db
import discrete_adaptive_samplers as das
import experiment_config as ec
import feature_functions as ff
import grasp_sampler as gs
import json_serialization as jsons
import kernels
import models
import objectives
import pfc
import pr2_grasp_checker as pgc
import random_variables as rvs
import robust_grasp_quality as rgq
import termination_conditions as tc




np.random.seed(100)
parser = argparse.ArgumentParser()
parser.add_argument('config')
parser.add_argument('output_dest')
args = parser.parse_args()

logging.getLogger().setLevel(logging.INFO)

# read config file
config = ec.ExperimentConfig(args.config)
database_filename = os.path.join(config['database_dir'], config['database_name'])
database = db.Hdf5Database(database_filename, config)

output_db_filename = os.path.join(args.output_dest, config['results_database_name'])
output_db = db.Hdf5Database(output_db_filename, config, access_level=db.WRITE_ACCESS)

for dataset_name in config['datasets'].keys():
    dataset = database.dataset(dataset_name)

    # make dataset output directory
    dest = os.path.join(args.output_dest, dataset.name)
    try:
        os.makedirs(dest)
    except os.error:
        pass
    output_ds = output_db.create_dataset(dataset_name)

    # label each object in the dataset with grasps
    for obj in dataset:
        obj_grasp = dataset.grasp_data(obj.key, "zeke")






database.close()
output_db.close()






