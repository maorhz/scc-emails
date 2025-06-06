# Deploy the function using the following gcloud commands 

- Ensure project id is set correctly

gcloud config set project my-project-76851-371010

- Deploy the function

gcloud functions deploy scc-parser-publisher \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=process_pubsub_message \
  --trigger-topic=scc-findings
  --set-env-vars GCP_PROJECT=$(gcloud config get-value project)
