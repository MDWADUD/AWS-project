from flask import Flask
from flask import Response
from flask import request
import boto3
app = Flask(__name__)

Bucket_name = "mdawadud"
# client--low-level AWS access
client = boto3.client('s3', aws_access_key_id = 'AKIAJHQ7I5KGYVIOUNQQ', aws_secret_access_key ='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')
# Resource--higher-level access
Resource = boto3.resource('s3',aws_access_key_id = 'AKIAJHQ7I5KGYVIOUNQQ', aws_secret_access_key ='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')


def uploads(username,file,filename):
  object = Resource.Object(Bucket_name, f"{username}/{filename}")
  object.put(Body=file)
@app.route('/upload/<id>',methods=["POST"])
def upload(id):
  if(request.method=="POST"):
    username = request.headers.get("api-key")
    file = request.files['file']
    users= users_name()
    return Response(status=200)
  if(username+'/' not in users):
    return Response(status=403)
  userfiles= get_user_files(username)
  if(f"{username}/{id}" in userfiles):
    return Response(status=403)
  uploads(username,file,id)
  return Response(status=200)


def users_name():
  Crear_folder_for_user = []
  objects = client.list_objects_v2(Bucket=Bucket_name, Delimiter='/', Prefix='')
  if(len(objects)==0):
    return []
  for i in objects["CommonPrefixes"]:
    Crear_folder_for_user.append(i["Prefix"])
  return Crear_folder_for_user
@app.route('/register/<username>')
def addfolder(folder_name):
  client.put_object(Bucket=Bucket_name, Key=(folder_name+'/'))
def register(username):
  users = users_name()
  print(users)
  if(username+'/' in users):
    return Response(status=403)
  addfolder(username)
  return Response(status=200)




def delete_user(key):
  bucket = Resource.Bucket(Bucket_name)
  bucket.objects.filter(Prefix=f"{key}/").delete()
@app.route('/remove/<username>')
def remove(username):
  users= users_name()
  if(username+'/' not in users):
    return Response(status=403)
  delete_user(username)
  return Response(status=200)


def get_user_files(username):
  files = []
  bucket = Resource.Bucket(Bucket_name)
  for object in bucket.objects.filter(Prefix=username):
    files.append(object.key)
  return files
@app.route('/files')
def files():
  username = request.headers.get("api-key")
  users= users_name()
  if(username+'/' not in users):
    return Response(status=403)
  return Response(data=get_user_files(username),status=200) 
@app.route('/files/<id>')
def filesContent(id):
  username = request.headers.get("api-key")
  users= users_name()
  if(username+'/' not in users):
    return Response(status=403)
  userfiles= get_user_files(username)
  if(f"{username}/{id}" in userfiles):
    return Response(data=filecontent,status=200)
  #else return 403 
  return Response(status=403)

def filecontent(username,id):
  bucket = Resource.Bucket(Bucket_name)
  file=bucket.objects.filter(Prefix=f"{username}/{id}")
  for object in file:
    return object.get()["Body"].read()


def delete(username,key):
  bucket = Resource.Bucket(Bucket_name)
  bucket.objects.filter(Prefix=f"{username}/{key}").delete()
@app.route('/delete/<id>')
def deleteContent(id):
  username = request.headers.get("api-key")
  users = users_name()
  if(username+'/' not in users):
    return Response(status=403)
  userfiles = get_user_files(username)
  print(userfiles)
  if(f"{username}/{id}") in userfiles:
    delete(username,id)
    return Response(status=200)
  return Response(status=403)



if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
