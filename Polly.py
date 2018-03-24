from boto3 import  client
import boto3
import io
from contextlib import closing
import botocore

polly = client("polly", 'us-east-1' )
questions= ["what is meant by the term latent heat?",
            "Explain the energy changes undergone by the molecules of a substance during the period when latent heat of vaporization is being supplied?",
            "State one way in which energy is lost from the transformer, and from which part it is lost.",
            "State two things which could be done to increase the speed of rotation of the coil.",
            "A beam of αlpha particles and Beta particles passes, in a vacuum, between the poles of a strong magnet. Compare the deflections of the paths of the two types of particle.",
            "A beam of αlpha particles and Beta particles passes, in a vacuum, between the poles of a strong magnet. Compare the deflections of the paths of the two types of particle."
            ]
i=0
for q in questions:

	response = polly.synthesize_speech(
	    Text=q,
	    OutputFormat="mp3",
		VoiceId="Joanna")

	print(response)

	if "AudioStream" in response:
		with closing(response["AudioStream"]) as stream:
			data = stream.read()
			fo = open("question"+str(i)+".mp3", "wb")
			fo.write( data )
			fo.close()
			s3 = boto3.resource('s3')
			s3.Object('testquestions-8853-5742-7832',"question"+str(i)+".mp3").put(Body=open("question"+str(i)+".mp3", 'rb'))
			object_acl = s3.ObjectAcl('testquestions-8853-5742-7832',"question"+str(i)+".mp3")
			response = object_acl.put(ACL='public-read')

	i+=1
