from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='Task-Scheduler',
    version='0.1.0',
    description='In memory task scheduler',
    long_description=readme,
    author='Prashant Lokhande',
    url='https://github.com/lprashant-94/task-scheduler'
)

