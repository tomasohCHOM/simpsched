from setuptools import setup, find_packages

setup(
    name="simpsched",
    version="0.1.0",
    description="A CLI tool to easily manage my date-to-date tasks",
    url="https://github.com/tomasohCHOM/simpsched",
    packages=find_packages(),
    install_requires=["click", "questionary", "rich"],
    entry_points={
        "console_scripts": ["simpsched=simpsched.cli:cli"],
    },
)
