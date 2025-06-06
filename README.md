# Deploy the function using gcloud commands 

- Ensure project id is set correctly

gcloud config set project my-project-76851-371010

- Deploy the function using gcloud

gcloud functions deploy scc-parser-publisher \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=process_pubsub_message \
  --set-env-vars GCP_PROJECT=$(gcloud config get-value project) \
  --trigger-topic=scc-findings


# Application Integration

The json file can be imported as a workflow in your gcp application integration module.
It will add a workflow that trigers every time a new message (scc event parsed and sent by the funtion) gets into a pub/sub topic and sent to the recipient configure in the "Send Email" task.
