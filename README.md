# gcp-cloud-run-job-demo
This repo was built to explore the potential of Google Cloud Run jobs (as opposed to services). The benefit is that Google Cloud Run jobs can run for more than one hour. This isn't a requirement for my use case, but I was curious as to whether this approach would be simpler than creating an API/service soltuion.

## Findings
This is not a simpler architecture. Since Cloud Scheduler only sends HTTP requests, you have to create a Google Cloud Function as an intermediary. Since none of the jobs I'm looking at would run for anything close to that amount of time, it doesn't make sense to do this. I got as far as creating the jobs. 

# Environment setup
The following assumes that you've created a new Google Cloud project just for this demo.

1. Create an `env.sh` file from the `env_template.sh` file and populate the variable values.
2. Create a conda environment `conda create -n gcp-cloud-run-job-demo python=3.12`
3. Install python packages `pip install -r requirements.txt`
4. Install gcloud, and select the GC project created for this demo (`gcloud projects list` > `gcloud config set project <PROJECT_ID>`)
5. Run the commands below.

# GCP Commands
## Enable required APIs
gcloud services enable cloudbuild.googleapis.com \
    run.googleapis.com \
    artifactregistry.googleapis.com \
    logging.googleapis.com 

## Create artifact registry
gcloud artifacts repositories create demo-repo \
    --repository-format=Docker \
    --location=$GCP_REGION

## Build App
gcloud builds submit --config cloudbuild.yaml .

## Bucket Setup
### Create bucket
gcloud storage buckets create gs://$GCP_BUCKET_NAME \
    --location=$GCP_REGION

### Bucket permission setup
gcloud storage buckets add-iam-policy-binding gs://$GCP_BUCKET_NAME \
    --member=serviceAccount:$GCP_CLOUD_RUN_SA_EMAIL \
    --role=roles/storage.objectCreator

## Create Jobs
gcloud run jobs update demo-job-a \
  --image $GCP_REGION-docker.pkg.dev/$(gcloud config get-value project)/demo-repo/demo-job \
  --region $GCP_REGION \
  --task-timeout=600s \
  --args="job-a"

gcloud run jobs create demo-job-b \
  --image $GCP_REGION-docker.pkg.dev/$(gcloud config get-value project)/demo-repo/demo-job \
  --region $GCP_REGION \
  --task-timeout=600s \
  --args="job-b"
 
gcloud run jobs update demo-job-a \
	--set-env-vars GCS_BUCKET=$GCP_BUCKET_NAME

gcloud run jobs update demo-job-b \
    --set-env-vars GCS_BUCKET=$GCP_BUCKET_NAME
