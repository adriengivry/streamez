from setuptools import setup, find_packages
import streamez

# Read the requirements from the generated requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()
    
setup(
    name="streamez",
    version=streamez.__version__,
    author="Adrien Givry",
    description="Lightweight system tray application designed to simplify your livestreaming and meeting lighting setups ",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "streamez = streamez.__main__:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
)
