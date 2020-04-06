import json
import boto3
from twilio.rest import Client


def lambda_handler(event, context):
    # TODO implement
    in_file = event["Records"][0]["s3"]["object"]["key"]
    out_file = in_file.split('.')[0] + '.mp3'
    
    etc = boto3.client('elastictranscoder', region_name='ap-southeast-2')
    
    response = etc.create_job(
        PipelineId='1585916327820-5reir7',
        Input={
            'Key': in_file
        },
        Output={
            'Key': out_file,
            'PresetId': '1351620000001-300040'
        }
        )
        
    print(response)
    
    file_split = in_file.split('_')[1]
    phone_number = file_split.split('.')[0]
        
    account_sid = 'AC9xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    auth_token = '53xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
                                  body=f'Just converting to MP3\n{in_file}\nHold tight...',
                                  from_='whatsapp:+14155238886',
                                  to=f'whatsapp:+{phone_number}'
                              )
    
    print(message.sid)
    print('SID?')
    return response
