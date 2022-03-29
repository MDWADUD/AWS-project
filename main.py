{\rtf1\ansi\ansicpg1252\cocoartf2513
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import requests\
#import boto3\
\
apikey = "md"\
\
# security credentials for folder check in the s3 bucket\
# Retrieve the list of existing buckets\
# s3 = boto3.client('s3',aws_access_key_id = 'AKIAJHQ7I5KGYVIOUNQQ', aws_secret_access_key ='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')\
# response = s3.list_buckets()\
\
# Output the bucket names\
# print('Existing buckets:')\
# for bucket in response['Buckets']:\
#   print(f'\{bucket["Name"]\}')\
\
\
\
# delete = requests.get("https://FinalAWSRedo.mdwadud.repl.co/delete/test.txt",headers=\{"api-key":apikey\})\
# print(delete.status_code)\
\
\
file = \{'file':open('test.txt','r')\}\
upload = requests.post("https://FinalAWSRedo.mdwadud.repl.co/upload/asdf.txt",files=file,headers=\{"api-key":apikey\})\
print(upload.status_code)\
}