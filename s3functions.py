import boto3
# Access Key ID:
PUBLICKEY = 'AKIAJHQ7I5KGYVIOUNQQ'
# Secret Access Key:
SECRETKEY = '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'
BUCKET_NAME = "shiplu"

s3 = boto3.client('s3', aws_access_key_id = PUBLICKEY, aws_secret_access_key = SECRETKEY)

s3Resource = boto3.resource('s3',aws_access_key_id = PUBLICKEY, aws_secret_access_key = SECRETKEY)

def get_users():
  foldernames = []
  objects = s3.list_objects_v2(Bucket=BUCKET_NAME, Delimiter='/', Prefix='')
  if(len(objects)==0):
    return []
  for i in objects["CommonPrefixes"]:
    foldernames.append(i["Prefix"])
  return foldernames

def addfolder(folder_name):
  s3.put_object(Bucket=BUCKET_NAME, Key=(folder_name+'/'))

def delete_user(key):
  bucket = s3Resource.Bucket(BUCKET_NAME)
  bucket.objects.filter(Prefix="{}/".format(key)).delete()
def get_user_files(username):
  files = []
  bucket = s3Resource.Bucket(BUCKET_NAME)
  for object in bucket.objects.filter(Prefix=username):
    files.append(object.key)
  return files
def getfilecontent(username,id):
  bucket = s3Resource.Bucket(BUCKET_NAME)
  file=bucket.objects.filter(Prefix="{}/{}".format(username,id))
  for object in file:
    return object.get()["Body"].read()
def delete_file(username,key):
  bucket = s3Resource.Bucket(BUCKET_NAME)
  bucket.objects.filter(Prefix="{}/{}".format(username,key)).delete()

def upload_file(username,file,filename):
  object = s3Resource.Object(BUCKET_NAME, "{}/{}".format(username,filename))
  object.put(Body=file)
