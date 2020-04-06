# VoiceMemo

Proof of Concept for a Twilio pipeline to:

 - capture an incoming voice memo from WhatsApp (ogg format)
 - store it in S3
 - transcode it to mp3
 - transcrible the mp3 audio to text
 - capture general sentiment
 - respond to the user
 
 
Know security issues in current implementation:

 - No auth is required from Twilio via the API Gateway to Lambda
 - Twilio auth_token is hard coded in Lambda - should be pushed external (i.e Secrets Manager) 
