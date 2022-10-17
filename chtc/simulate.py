import argparse
import gym
import numpy as np


def simulate(env, num_episodes):
    '''
    Simulate random actions in a gym environment.

    :param env: Gym environment
    :param num_episodes: Number of episodes to simulate
    '''

    returns = []
    for episode_i in range(num_episodes):
        obs, info = env.reset()
        done = False

        ret = 0
        while not done:
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            ret += reward
        returns.append(ret)
    print(f'Average return over {num_episodes} episodes: {np.average(returns)} +/- {np.std(returns)}')

    return returns

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--env-id", type=str, default="Humanoid-v4", help="environment ID")
    parser.add_argument("--num-episodes", type=int, default=10, help="Number of episodes")
    args = parser.parse_args()

    env_ids = list(gym.envs.registry.keys())
    for env_id in env_ids:
        print(f'Simulating {env_id}...')
        env = gym.make(args.env_id)
        simulate(env, args.num_episodes)
        print()
    print('Successfully tested all environments')

