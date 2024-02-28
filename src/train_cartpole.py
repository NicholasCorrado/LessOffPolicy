import os

for i in range(10):
    os.system(
        'python train.py --algo ppo --env-id CartPole-v1 --num-timesteps 30000'
    )