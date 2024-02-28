import argparse
import os

import yaml
import gym, custom_envs
import numpy as np
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3 import A2C, DDPG, DQN, PPO, SAC, TD3

from src.utils import get_latest_run_id, StoreDict

ALGOS = {
    "a2c": A2C,
    "ddpg": DDPG,
    "dqn": DQN,
    "ppo": PPO,
    "sac": SAC,
    "td3": TD3,
}

def train(env, agent, num_timesteps, callbacks):
    agent.learn(total_timesteps=num_timesteps, callback=callbacks)

    obs, _ = env.reset()
    for i in range(num_timesteps):
        action, _state = agent.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        if done:
            obs, _ = env.reset()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", type=int, default=None, help='Suffix to add to save_dir')
    parser.add_argument("--seed", type=int, default=0, help="seed of the experiment")
    parser.add_argument("--env-id", type=str, default="Nav2d-v0", help="environment ID")
    parser.add_argument("--algo", type=str, default="ddpg", help="Aglorithm")
    parser.add_argument("--num-timesteps", type=int, default=30000, help="Number of episodes")

    parser.add_argument("-params", "--hyperparams", type=str, nargs="+", action=StoreDict, default={}, help="Overwrite hyperparameter (e.g. learning_rate:0.01 train_freq:10)",)

    parser.add_argument("--eval-freq", type=int, default=1000, help="Evaluate policy every eval_freq timesteps (or every eval_freq updates for on-policy algorithms)")
    parser.add_argument("--eval-episodes", type=int, default=20, help="Number of episodes over which policies are evaluated")
    parser.add_argument("--results-dir", "-f", type=str, default="results", help="Root directory to save results")
    parser.add_argument("--results-subdir", "-s", type=str, default="", help="results will be saved to <results_dir>/<env_id>/<algo>/<subdir>/")
    args = parser.parse_args()


    if args.seed is None:
        args.seed = np.random.randint(2 ** 32 - 1)

    save_dir = f"{args.results_dir}/{args.env_id}/{args.algo}/{args.results_subdir}"
    if args.run_id:
        save_dir += f"/run_{args.run_id}"
    else:
        run_id = get_latest_run_id(save_dir=save_dir) + 1
        save_dir += f"/run_{run_id}"
    args.save_dir = save_dir

    os.makedirs(args.save_dir, exist_ok=True)
    with open(os.path.join(args.save_dir, "config.yml"), "w") as f:
        yaml.dump(args, f, sort_keys=True)

    print(f'Training on {args.env_id}...')
    env = gym.make(args.env_id)
    eval_env = gym.make(args.env_id)

    algo_class = ALGOS[args.algo]
    agent = algo_class("MlpPolicy", env, **args.hyperparams, verbose=0)

    eval_callback = EvalCallback(eval_env, n_eval_episodes=args.eval_episodes, eval_freq=args.eval_freq, log_path=save_dir, best_model_save_path=save_dir)
    train(env, agent, num_timesteps=args.num_timesteps, callbacks=[eval_callback])

    agent.save(f'{save_dir}/final_model.zip')