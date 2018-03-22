from boto3 import  client
import boto3
import io
from contextlib import closing

polly = client("polly", 'us-east-1' )
response = polly.synthesize_speech(
    Text="Good Morning. My Name is Rajesh. I am Testing Polly AWS Service For Voice Application.",
    OutputFormat="mp3",
    VoiceId="Raveena")

print(response)

if "AudioStream" in response:
    with closing(response["AudioStream"]) as stream:
        data = stream.read()
        fo = open("pollytest.mp3", "wb")
        fo.write( data )
        fo.close()