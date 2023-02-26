import os


def write_to_file(f, args):
    args = args.replace(' ', '*')
    print(args)
    f.write(args + "\n")

def gen_command(env_id, num_episodes):
    python_command = f'simulate.py --env-id {env_id} --num-episodes {num_episodes}'
    mem = 1
    disk = 6

    command = f"\\\"{mem},{disk},{python_command}\\\""

    return command

if __name__ == "__main__":

    env_ids = ['Hopper-v4', 'HalfCheetah-v4', 'Ant-v4', 'Walker2d-v4', 'Humanoid-v4', 'Swimmer-v4'
               'InvertedPendulum-v4', 'InvertedDoublePendulum-v4']

    os.makedirs('commands', exist_ok=True)
    f = open(f"commands/simulate.txt", "w")

    for env_id in env_ids:
        for num_episodes in [10, 20, 30]:
            command = gen_command(env_id, num_episodes)
            write_to_file(f, command)

