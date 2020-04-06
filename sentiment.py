import json
import boto3
from twilio.rest import Client

def lambda_handler(event, context):
    # TODO implement
    in_bucket = event["Records"][0]["s3"]["bucket"]["name"]
    in_file = event["Records"][0]["s3"]["object"]["key"]
    
    # Get File
    s3 = boto3.resource('s3', region_name='ap-southeast-2')

    content_object = s3.Object(in_bucket, in_file)
    file_content = content_object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    
    print(json_content)
    
    transcription = json_content['results']['transcripts'][0]['transcript']
    
    # Get Sentiment
    comprehend = boto3.client('comprehend', region_name='ap-southeast-2')
    
    sentiment_response = comprehend.detect_sentiment(
        Text=transcription,
        LanguageCode='en'
    )
    
    print(sentiment_response)
    sentiment = sentiment_response['Sentiment'].lower()
    
    # Send Message
    file_split = in_file.split('_')[1]
    phone_number = file_split.split('.')[0]
        
    account_sid = 'AC9xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    auth_token = '53dxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
                                  body=f"You said the following with a '{sentiment}' sentiment:\n\n{transcription}",
                                  from_='whatsapp:+14155238886',
                                  to=f'whatsapp:+{phone_number}'
                              )
    
    print(message.sid)
    
    return 
