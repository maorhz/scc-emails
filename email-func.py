# main.py

import json
import base64
from google.cloud import pubsub_v1
import os

# It's a good practice to initialize clients outside the function handler
# to take advantage of connection reuse.
publisher = pubsub_v1.PublisherClient()
# The topic path is now dynamically constructed using an environment variable
# for better portability and security.
PROJECT_ID = 'my-project-76851-371010'
DESTINATION_TOPIC = 'scc-findings-parsed'
topic_path = publisher.topic_path(PROJECT_ID, DESTINATION_TOPIC)


def process_pubsub_message(event, context):
    """
    This function processes a Pub/Sub message by decoding it,
    extracting finding details, and publishing the parsed data
    to another Pub/Sub topic.
    """
    print(f"Function triggered by messageId: {context.event_id} on topic: {context.resource['name']}")

    # Decode and load the Pub/Sub message data
    try:
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        pubsub_data = json.loads(pubsub_message)
        finding = pubsub_data.get('finding', {})
        resource = pubsub_data.get('resource', {})
    except Exception as e:
        print(f"Error decoding or parsing initial message: {e}")
        return  # Stop execution if the message is malformed

    # Extract the relevant values from the JSON object
    finding_data = {
        'title': finding.get('category', 'N/A'),
        'severity': finding.get('severity', 'N/A'),
        'resource': finding.get('resourceName', 'N/A'),
        'description': finding.get('description', 'N/A'),
        'project_name': resource.get('projectDisplayName', 'N/A'),
        'explanation': finding.get('sourceProperties', {}).get('Explanation', 'N/A'),
        'external_uri': finding.get('externalUri', 'N/A')
    }

    print("Successfully extracted finding data:")
    print(json.dumps(finding_data, indent=2))

    # --- PUBLISH TO THE DESTINATION TOPIC ---

    # Convert the finding_data dictionary to a JSON string, then encode to bytes
    message_data = json.dumps(finding_data).encode('utf-8')
    print("log: convert message from dictionary to json")

    # Publish the message to the new topic
    try:
        future = publisher.publish(topic_path, data=message_data)
        # The .result() method blocks until the message is published.
        print(f"Successfully published message ID {future.result()} to topic {topic_path}")
    except Exception as e:
        print(f"Error publishing to {topic_path}: {e}")
        # Re-raise the exception to signal a failure to Cloud Functions,
        # which can be useful for monitoring and retries.
        raise
    return 'OK'
