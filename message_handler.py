import json
import io
import boto3
import requests
from datetime import datetime
import urllib.parse
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

def lambda_handler(event, context):
    body = event['body']
    twilio_input = urllib.parse.parse_qs(body)
    
    resp = MessagingResponse()
    if int(twilio_input['NumMedia'][0]) > 0:
        media_url = twilio_input['MediaUrl0'][0]
        media_payload = requests.get(media_url)
        
        date_prefix = datetime.now().strftime("%m%d%Y-%H%M%S")
        from_number = twilio_input['From'][0].split("+")[-1]
        
        s3 = boto3.client('s3', region_name='ap-southeast-2')
        s3 = s3.upload_fileobj(io.BytesIO(media_payload.content), 'ansamual-stories', f'{date_prefix}_{from_number}.ogg')
        
        resp.message(f"Thanks for sharing.\n\nYour audio file is safely stored in S3\n\n{date_prefix}_{from_number}.ogg")
        
    else:
        resp.message("Hi there!  Try uploading some audio :)")
    
    return {
        'statusCode': 200,
        "headers": {
            "Content-Type": "text/xml",
        },
        'body': str(resp)
    }
