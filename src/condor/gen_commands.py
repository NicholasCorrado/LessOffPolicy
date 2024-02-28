import os


def gen_command(env_id, num_episodes, eval_freq, learning_rate):
    python_command = f'python -u train.py --results-subdir lr_{lr}' \
                     f' --env-id {env_id}' \
                     f' --num-timesteps {num_episodes}' \
                     f' --eval-freq {eval_freq}' \
                     f' --learning-rate {learning_rate}'
    mem = 1
    disk = 6

    command = f"{mem},{disk},{python_command}"

    return command

if __name__ == "__main__":

    env_ids = ['Hopper-v4', 'HalfCheetah-v4', 'Ant-v4', 'Walker2d-v4', 'Humanoid-v4', 'Swimmer-v4'
               'InvertedPendulum-v4', 'InvertedDoublePendulum-v4']

    os.makedirs('commands', exist_ok=True)
    f = open(f"commands/train.txt", "w")

    num_timesteps = int(10e3)

    for env_id in env_ids:
        for lr in [1e-3, 1e-4]:
            command = gen_command(env_id, num_timesteps, eval_freq=1000, learning_rate=lr)
            print(command)
            command = command.replace(' ', '*')
            f.write(command + "\n")
