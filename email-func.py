import os
import base64
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    finding = json.loads(pubsub_message)

    # Extract relevant details from the finding
    finding_category = finding['finding']['category']
    project_id = finding['finding']['resourceName'].split('/')[1]
    description = finding['finding'].get('description', 'No description available.')

    message = Mail(
        from_email='your-sender-email@example.com',
        to_emails='your-recipient-email@example.com',
        subject=f'New Security Finding: {finding_category}',
        html_content=f"""
            <h2>New Security Finding Detected</h2>
            <p><strong>Project:</strong> {project_id}</p>
            <p><strong>Category:</strong> {finding_category}</p>
            <p><strong>Description:</strong> {description}</p>
            <p>For more details, please check the Security Command Center dashboard.</p>
        """
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
