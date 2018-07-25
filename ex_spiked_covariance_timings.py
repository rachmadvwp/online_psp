# Title: ex_spiked_covariance_timings.py
# Description: Testing online PCA algorithm timings on artificially generated data
# Author: Victor Minden (vminden@flatironinstitute.org) and Andrea Giovannucci (agiovannucci@flatironinstitute.org)
# Notes: Adapted from code by Andrea Giovannucci
# Reference: None

# %%
# imports
from online_pca_simulations import run_simulation
import os
import pylab as plt
import numpy as np

# general parameters


error_options = {}

generator_options = {
    'method': 'spiked_covariance',
    'lambda_q': 5e-1,
    'normalize': True,
    'rho': 1e-2 / 5,
    'scale_data': True
}

simulation_options = {
    'd': 8192,
    'q': 50,
    'n': 2,
    'n0': 0,
    'n_epoch': 1,
    'error_options': error_options,
    'pca_init': False,
    'init_ortho': True,
}

algos = ['if_minimax_PCA', 'incremental_PCA', 'CCIPCA', 'minimax_PCA']
algo = algos[0]
#algos = ['if_minimax_PCA','minimax_PCA', 'CCIPCA']
algorithm_options = {
    'pca_algorithm': algo,
    'tau': 0.5,
    'tol': 1e-7
}


def run_test(simulation_options=None, algorithm_options=None, generator_options=None):
    output_folder = os.getcwd() + '/test'

    timing = run_simulation(output_folder, simulation_options,
                            generator_options, algorithm_options)
    return timing


n_repetitions = 1
simulation_options['n'] = 10
qs = [64, 128, 256, 512, 1024, 2048, 4096]
results = dict()
counter = 0
colors = ['b', 'r', 'g','k']
d = 8192
counter += 1
ax = plt.subplot(1, 1, counter)
simulation_options['d'] = d
filename = './ex/timings/blah.blah'
os.makedirs(os.path.dirname(filename), exist_ok=True)

for algo in range(len(algos)):
    algo_timings = []
    for q in qs:
        timings = []
        # Take the mean over n_repetitions trials
        for reps in range(n_repetitions):
            simulation_options['q'] = q
            algorithm_options['pca_algorithm'] = algos[algo]
            timing = run_test(generator_options=generator_options, simulation_options=simulation_options,
                              algorithm_options=algorithm_options)
            timings.append(timing)
        algo_timings.append(np.mean(timings))
        output_dict = {
            'generator_options': generator_options,
            'simulation_options': simulation_options,
            'algorithm_options': algorithm_options,
            'd': d,
            'q': q,
            'n': simulation_options['n'],
            'n_epoch': 1,
            'n0': 0,
            'timing': np.mean(timings)
        }
        print(output_dict['timing'])
        np.savez('./ex/timings/' + 'd_%d_q_%d_algo_%s'
                 % (d, q, algos[algo]),
                 output_dict)

    line_timing, = ax.plot(qs, np.array(algo_timings) / simulation_options['n'], '-d' + colors[algo])
    # line_bat, = ax.plot(rhos, batch_err_avg, '-o' + colors[algo])
    line_timing.set_label(algos[algo])
    # line_bat.set_label(algos[algo] + '_batch')
qs = np.array(qs)
ax.plot(qs, qs / 5e4, '--r')
ax.plot(qs, qs ** 2 / 2e5, '--r')
ax.legend()
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Number of components')
plt.ylabel('Time per iteration (s)')
plt.savefig('./ex/timings/d_%d.png' % (d))
plt.show()