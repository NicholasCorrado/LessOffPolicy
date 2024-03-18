import os
from gym.envs.registration import register

# ENVS_DIR = os.path.join(os.path.dirname(__file__), 'envs')

register(
    id="Nav2d-v0",
    entry_point="custom_envs.nav2d:Nav2dEnv",
    max_episode_steps=100,
)

register(
    id="Nav2d-v1",
    entry_point="custom_envs.nav2d:Nav2dEnv",
    max_episode_steps=100,
)

register(
    id="Nav2d-H100",
    entry_point="custom_envs.nav2d:Nav2d_H100Env",
    max_episode_steps=100,
)
register(
    id="Nav2d-H75",
    entry_point="custom_envs.nav2d:Nav2d_H75Env",
    max_episode_steps=75, # horizon
)
register(
    id="Nav2d-H50",
    entry_point="custom_envs.nav2d:Nav2d_H50Env",
    max_episode_steps=50, 
)
register(
    id="Nav2d-H25",
    entry_point="custom_envs.nav2d:Nav2d_H25Env",
    max_episode_steps=25, 
)
# Hopper 
register(
    id="Hopper-v4-H100",
    entry_point="Hopper-v4",
    max_episode_steps=100, 
)
register(
    id="Nav2d-H25",
    entry_point="custom_envs.nav2d:Nav2d_H25Env",
    max_episode_steps=25, 
)
register(
    id="Nav2d-H25",
    entry_point="custom_envs.nav2d:Nav2d_H25Env",
    max_episode_steps=25, 
)
register(
    id="Nav2d-H25",
    entry_point="custom_envs.nav2d:Nav2d_H25Env",
    max_episode_steps=25, 
)
