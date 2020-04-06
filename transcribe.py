import json
import boto3
from twilio.rest import Client

def lambda_handler(event, context):
    # TODO implement
    in_file = event["Records"][0]["s3"]["object"]["key"]
    
    transcribe_client = boto3.client('transcribe', region_name='ap-southeast-2')
    
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=in_file,
        LanguageCode='en-AU',
        Media={
            'MediaFileUri': f's3://ansamual-stories-mp3/{in_file}'
        },
        OutputBucketName='ansamual-stories-transcribed'
        )
        
    file_split = in_file.split('_')[1]
    phone_number = file_split.split('.')[0]
        
    account_sid = 'AC9xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    auth_token = '53dxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
                                  body=f'Now transcribing\n{in_file}\nnearly there...',
                                  from_='whatsapp:+14155238886',
                                  to=f'whatsapp:+{phone_number}'
                              )
    
    print(message.sid)
    
    
    return response
