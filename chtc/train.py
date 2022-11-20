import argparse

import gym
from stable_baselines3 import PPO


def train(env):
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=1000)

    obs, _ = env.reset()
    for i in range(1000):
        action, _state = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        if done:
            obs, _ = env.reset()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--env-id", type=str, default="Humanoid-v4", help="environment ID")
    parser.add_argument("--num-episodes", type=int, default=10, help="Number of episodes")
    args = parser.parse_args()

    env_ids = list(gym.envs.registry.keys())
    for env_id in env_ids:
        print(f'Simulating {env_id}...')
        env = gym.make(args.env_id)
        train(env)
        print()
    print('Successfully tested all environments')