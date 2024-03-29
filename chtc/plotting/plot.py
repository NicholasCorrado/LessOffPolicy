import os

import numpy as np
import seaborn
from matplotlib import pyplot as plt

from utils import get_paths, plot


if __name__ == "__main__":
    seaborn.set_theme()

    env_id = 'CartPole-v1'
    algo = 'ppo'

    path_dict = {}

    root_dir = f'../results/{env_id}/{algo}'
    key = f'{algo}'

    path_dict.update(
        get_paths(
        results_dir=f'{root_dir}',
        key=key)
    )

    plot(path_dict)
    plt.title(f'{env_id}', fontsize=16)
    plt.xlabel('Timesteps', fontsize=16)
    plt.ylabel('Return', fontsize=16)
    plt.tight_layout()
    plt.legend()

    save_dir = f'figures'
    save_name = f'{env_id}'
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(f'{save_dir}/{save_name}')

    plt.show()
