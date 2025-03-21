import os
import sys
import logging
import argparse
from datetime import datetime
from google.cloud import storage

logging.basicConfig(level=logging.INFO)

BUCKET_NAME = os.getenv("GCS_BUCKET", "your-default-bucket")
ENV = os.getenv('ENV', 'STAGING')

def get_tstamp():
    return datetime.now().strftime("%Y%m%d%H%M%S")

def upload_to_gcs(val):
    """Upload data to Google Cloud Storage."""
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    tstamp = get_tstamp()
    blob = bucket.blob(f"data_{tstamp}.txt")
    blob.upload_from_string(val)
    logging.info(f"Data uploaded to gs://{BUCKET_NAME}/data_{tstamp}.txt")

def job(job_id):
	tstamp = get_tstamp()
	val = f'job {job_id} executed @ {tstamp}'
	if ENV != 'DEV':
		upload_to_gcs(val)
	else:
		logging.info(f"{job_id} output: {val}")

def job_a():
	logging.info("Executing job-a")
	job("job-a")

def job_b():
	logging.info("Executing job-b")
	job("job-b")

def main(job_name):
    
    if job_name == "job-a":
        job_a()
    elif job_name == "job-b":
        job_b()
    else:
        print("No valid job specified.")
        sys.exit(1)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument("job", type=str, help="The name of the job to execute")

	args = parser.parse_args()

	main(args.job)
