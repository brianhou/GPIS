import IPython
import logging
import matplotlib as mpl; mpl.use('Agg') # this doesn't seem to work...
import matplotlib.pyplot as plt
import models
import numpy as np
import pickle as pkl
import os
import sys
import scipy.spatial.distance as ssd

from brute_correlated_bandits import BanditCorrelatedExperimentResult
import experiment_config as ec

if __name__ == '__main__':
    config_file = sys.argv[1]
    result_dir = sys.argv[2]

    logging.getLogger().setLevel(logging.INFO)
    config = ec.ExperimentConfig(config_file)
    with open(os.path.join(result_dir, 'config.yaml'), 'w') as f:
        f.write(config.file_contents)

    # read in all pickle files
    results = []
    for _, dirs, _ in os.walk(result_dir):
        # compile each subdirectory
        for d in dirs:
            # get the pickle files from each directory
            for root, _, files in os.walk(os.path.join(result_dir, d)):
                for f in files:
                    if f.endswith('.pkl'):
                        result_pkl = os.path.join(root, f)
                        f = open(result_pkl, 'r')
                        
                        logging.info('Reading %s' %(result_pkl))
                        try:
                            p = pkl.load(f)
                        except Exception as e:
                            logging.error(e)
                            continue

                        if p is not None:
                            results.append(p)

    # aggregate results
    if len(results) == 0:
        exit(0)

    all_results = BanditCorrelatedExperimentResult.compile_results(results)

    # plot params
    line_width = config['line_width']
    font_size = config['font_size']
    dpi = config['dpi']

    # plot the prior distribution of grasp quality
    grasp_qualities = np.zeros(0)
    for result in results:
        pfc = result.true_avg_reward
        grasp_qualities = np.r_[grasp_qualities, pfc]

    # plot correlation vs pfc diff
    for i, result in enumerate(results):
        logging.info('Result %d' %(i))

        estimated_pfc = result.true_avg_reward 
        k_vec = result.kernel_matrix.ravel()
        pfc_arr = np.array([estimated_pfc]).T
        pfc_diff = ssd.squareform(ssd.pdist(pfc_arr))
        pfc_vec = pfc_diff.ravel()

        plt.figure()
        plt.scatter(k_vec, pfc_vec)
        plt.xlabel('Kernel', fontsize=font_size)
        plt.ylabel('PFC Diff', fontsize=font_size)
        plt.title('Correlations for object %d' %(i), fontsize=font_size)

        figname = 'correlations_obj_%s.png' %(result.obj_key)
        plt.savefig(os.path.join(result_dir, figname), dpi=dpi)

        
        plt.figure()
        plt.plot(result.iters, result.ua_reward, c=u'b', linewidth=line_width, label='Uniform Allocation')
        plt.plot(result.iters, result.ts_reward, c=u'g', linewidth=line_width, label='Thompson Sampling (Uncorrelated)')
        plt.plot(result.iters, result.ts_corr_reward, c=u'r', linewidth=line_width, label='Thompson Sampling (Correlated)')

        plt.xlim(0, np.max(all_results.iters[0]))
        plt.ylim(0.5, 1)
        plt.xlabel('Iteration', fontsize=font_size)
        plt.ylabel('Normalized Probability of Force Closure', fontsize=font_size)
        plt.title('Avg Normalized PFC vs Iteration', fontsize=font_size)

        handles, labels = plt.gca().get_legend_handles_labels()
        plt.legend(handles, labels, loc='lower right')

        figname = 'avg_reward_obj_%s.png' %(result.obj_key)
        plt.savefig(os.path.join(result_dir, figname), dpi=dpi)

    # plot all correlations on one plot
    plt.figure()
    for i, result in enumerate(results):
        estimated_pfc = result.true_avg_reward 
        k_vec = result.kernel_matrix.ravel()
        pfc_arr = np.array([estimated_pfc]).T
        pfc_diff = ssd.squareform(ssd.pdist(pfc_arr))
        pfc_vec = pfc_diff.ravel()

        plt.scatter(k_vec, pfc_vec)

    plt.xlabel('Kernel', fontsize=font_size)
    plt.ylabel('PFC Diff', fontsize=font_size)
    plt.title('Correlations for object %d' %(i), fontsize=font_size)

    figname = 'all_correlations.png'
    plt.savefig(os.path.join(result_dir, figname), dpi=dpi)
        

    # plot histograms
    num_bins = 100
    bin_edges = np.linspace(0, 1, num_bins+1)
    plt.figure()
    n, bins, patches = plt.hist(grasp_qualities, bin_edges)
    plt.xlabel('Probability of Success', fontsize=font_size)
    plt.ylabel('Num Grasps', fontsize=font_size)
    plt.title('Histogram of Grasps by Probability of Success', fontsize=font_size)

    figname = 'histogram_success.png'
    plt.savefig(os.path.join(result_dir, figname), dpi=dpi)

    # plotting of final results
    ua_avg_norm_reward = np.mean(all_results.ua_reward, axis=0)
    ts_avg_norm_reward = np.mean(all_results.ts_reward, axis=0)
    ts_corr_avg_norm_reward = np.mean(all_results.ts_corr_reward, axis=0)

    ua_std_norm_reward = np.std(all_results.ua_reward, axis=0)
    ts_std_norm_reward = np.std(all_results.ts_reward, axis=0)
    ts_corr_std_norm_reward = np.std(all_results.ts_corr_reward, axis=0)

    # plot avg simple regret
    plt.figure()

    plt.plot(all_results.iters[0], ua_avg_norm_reward, c=u'b', linewidth=line_width, label='Uniform Allocation')
    plt.plot(all_results.iters[0], ts_avg_norm_reward, c=u'g', linewidth=line_width, label='Thompson Sampling (Uncorrelated)')
    plt.plot(all_results.iters[0], ts_corr_avg_norm_reward, c=u'r', linewidth=line_width, label='Thompson Sampling (Correlated)')

    plt.xlim(0, np.max(all_results.iters[0]))
    plt.ylim(0.5, 1)
    plt.xlabel('Iteration', fontsize=font_size)
    plt.ylabel('Normalized Probability of Force Closure', fontsize=font_size)
    plt.title('Avg Normalized PFC vs Iteration', fontsize=font_size)

    handles, labels = plt.gca().get_legend_handles_labels()
    plt.legend(handles, labels, loc='lower right')

    figname = 'avg_reward.png'
    plt.savefig(os.path.join(result_dir, figname), dpi=dpi)

    # plot avg simple regret w error bars
    plt.figure()

    plt.errorbar(all_results.iters[0], ua_avg_norm_reward, yerr=ua_std_norm_reward, c=u'b', linewidth=line_width, label='Uniform Allocation')
    plt.errorbar(all_results.iters[0], ts_avg_norm_reward, yerr=ts_std_norm_reward, c=u'g', linewidth=line_width, label='Thompson Sampling (Uncorrelated)')
    plt.errorbar(all_results.iters[0], ts_corr_avg_norm_reward, yerr=ts_corr_std_norm_reward, c=u'r', linewidth=line_width, label='Thompson Sampling (Correlated)')

    plt.xlim(0, np.max(all_results.iters[0]))
    plt.ylim(0.5, 1)
    plt.xlabel('Iteration', fontsize=font_size)
    plt.ylabel('Normalized Probability of Force Closure', fontsize=font_size)
    plt.title('Avg Normalized PFC with StdDev vs Iteration', fontsize=font_size)

    handles, labels = plt.gca().get_legend_handles_labels()
    plt.legend(handles, labels, loc='lower right')

    figname = 'avg_reward_with_error_bars.png'
    plt.savefig(os.path.join(result_dir, figname), dpi=dpi)

    # finally, show
    if config['plot']:
        plt.show()
