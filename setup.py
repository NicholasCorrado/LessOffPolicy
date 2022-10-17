from setuptools import find_packages, setup

setup(
    name='chtc',
    version='0.1.0',
    python_requires='>=3.9',
    install_requires=[
        'mujoco',
        'gym'
    ]
)