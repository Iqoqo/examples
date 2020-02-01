# limit-running-example

This module is one example of how to use disco's python sdk.
it will limit the number of running jobs, by defining the max_running_job parameter.
usage case: You have x gpus and you want to allow only max of x jobs to run.

## Requirements
disco sdk, which can be installed by running:
`pip install disco`

## Config
- Change the max_running_jobs param at the top of the file to your desired maxium running jobs
- Change the job_type param at the top of the file to your desired job size (See disco documentation for the instance types)

## Usage Example
`$ python main.py spawn --name "NewJob" --script "/home/user/python_script.py"`

