#! /usr/local/bin/python
import argparse
import disco
import os
import pathlib
from disco import Job

"""TOP CONFIG"""
job_type = 'sg'
max_running_jobs = 4


def alert_and_exit(error_msg: str):
    print("Error: {}".format(error_msg))
    exit(1)


def check_environ():
    """
    Checks that disco credentials are exported
    """
    fail = False
    for k in ['DISCO_EMAIL', 'DISCO_PASSWORD']:
        if k not in os.environ:
            print(f'please export {k}')
            fail = True
    if not fail:
        disco.set_credentials(os.environ['DISCO_EMAIL'],
                              os.environ['DISCO_PASSWORD'],
                              save_to_dot_file=True)
    print(f'Check environment {"Failed" if fail else "OK"}')
    return not fail


def get_current_running_count():
    """
    Returns the number of running jobs
    A running job is either queued (started and waiting for free resources)
    or actually running (agent is currently running the job)
    """
    statuses = disco.job.jobs_summary()
    for s in statuses:
        if s['status'] == disco.constants.JobStatus.working.value:
            return s['count']
    return 0


def upload_job_script(script_file_path: str):
    """
    Uploads the (required) actual script file for the job
    """
    print("Uploading script file {}...".format(script_file_path))
    if os.path.exists(script_file_path):
        try:
            return disco.upload_file(os.path.basename(script_file_path),
                                     pathlib.Path(script_file_path))
        except Exception as err:
            alert_and_exit("Unable to upload file {}: {}".format(script_file_path, err))
    alert_and_exit("File {} Doesn't exists".format(script_file_path))


def add_job(script_file_id: str, job_name: str):
    """
    Adds a new job to the system
    // Note: This doesn't start the job, see the start_job function //
    Returns: the job's id
    """
    print("Trying to add job: {}...".format(job_name))
    try:
        return disco.Job.add(script_file_id,
                             cluster_instance_type=job_type,
                             job_name=job_name)
    except Exception as err:
        alert_and_exit("Unable to add job {}: {}".format(job_name, err))


def stop_job(job_id: str):
    """
    stops a running job
    """
    print("Trying to stop job: {}...".format(job_id))
    try:
        return disco.Job.stop(job_id)
    except Exception as err:
        alert_and_exit("Unable to add job {}: {}".format(job_id, err))


def start_job(job: Job):
    """
    This will actually run the job (or queue it, depending on available resources)
    """
    print("Trying to start job {}...".format(job))
    try:
        job.start()
        print("Started job: {}".format(job))
    except Exception as err:
        alert_and_exit("Unable to start job {}: {}".format(job, err))


def get_tasks(job: Job):
    """
    This will return an array of tasks
    A job can contain multiple tasks
    A task is the unit that actually executes a script
    """
    print("Listing tasks for job {}...".format(job))
    try:
        job_tasks = job.get_tasks()
        for task in job_tasks:
            print(task)
    except Exception as err:
        alert_and_exit("Unable to get tasks for job {}: {}".format(job, err))


def get_running_jobs(limit=10):
    """
    This will return an array of running jobs
    limited to the default of 10
    """
    running_jobs = []
    try:
        all_jobs = disco.list_jobs(limit=limit)
        for job in all_jobs:
            if job['status'] == disco.constants.JobStatus.working.value:
                running_jobs.append(job)
        return running_jobs
    except Exception as err:
        alert_and_exit("Unable to get running jobs: {}".format(err))


def spawn_job(job_name, job_script):
    """
    Main Function for spawning a job
    """
    print("Checking for job allocation possibility...")
    if get_current_running_count() < max_running_jobs:
        print("Allocation is possible, Creating job of type: {}".format(
            job_type
        ))
        # Upload script file
        script_file_id = upload_job_script(job_script)
        # Add the job
        job = add_job(script_file_id, job_name)
        job_id = disco.Job.get_details(job)['job']['id']
        # Start the job
        start_job(job)
        # List the job tasks
        get_tasks(job)
    else:
        print("Unable to spawn a new job, maximum of {} jobs are running"
              .format(max_running_jobs))


def main():
    """Arguments"""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    # For Spawn
    spawn_p = subparsers.add_parser('spawn', help='Spawn a new job')
    spawn_p.add_argument("--name", required=True, help="Job name for job spawn")
    spawn_p.add_argument("--script", required=True, help="Script path for job spawn")
    spawn_p.set_defaults(func=spawn_job)
    # For Job Listing
    list_p = subparsers.add_parser('listjobs', help='List running jobs')
    list_p.set_defaults(func=get_running_jobs)

    args = parser.parse_args()

    """Required Credentials"""
    os.environ['DISCO_EMAIL'] = "your_disco_username"
    os.environ['DISCO_PASSWORD'] = "your_disco_password"

    """Main Event"""
    if check_environ():
        # RUN JOB
        if args.command == 'spawn':
            spawn_job(job_name=args.name, job_script=args.script)
        elif args.command == 'listjobs':
            # GET RUNNING JOBS
            print(get_running_jobs())
    else:
        exit(1)


if __name__ == '__main__':
    main()
