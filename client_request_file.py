import requests
#import boto3

apikey = "md"

# security credentials for folder check in the s3 bucket
# Retrieve the list of existing buckets
# s3 = boto3.client('s3',aws_access_key_id = 'AKIAJHQ7I5KGYVIOUNQQ', aws_secret_access_key ='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')
# response = s3.list_buckets()

# Output the bucket names
# print('Existing buckets:')
# for bucket in response['Buckets']:
#   print(f'{bucket["Name"]}')



# delete = requests.get("https://FinalAWSRedo.mdwadud.repl.co/delete/test.txt",headers={"api-key":apikey})
# print(delete.status_code)


file = {'file':open('test.txt','r')}
upload = requests.post("https://FinalAWSRedo.mdwadud.repl.co/upload/asdf.txt",files=file,headers={"api-key":apikey})
print(upload.status_code)
