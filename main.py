from flask import Flask, Response, request
from s3functions import get_users, addfolder, delete_user, get_user_files, getfilecontent, delete_file, upload_file

app = Flask(__name__)



# def get_users():
#   foldernames = []
#   objects = s3.list_objects_v2(Bucket=BUCKET_NAME, Delimiter='/', Prefix='')
#   if(len(objects)==0):
#     return []
#   for i in objects["CommonPrefixes"]:
#     foldernames.append(i["Prefix"])
#   return foldernames

@app.route('/register/<username>')
def register(username):
  users = get_users()
  print(users)
  if(username+'/' in users):
    return Response(status=403)
  addfolder(username)
  return Response(status=200)

@app.route('/remove/<username>')
def remove(username):
  users= get_users()
  if(username+'/' not in users):
    return Response(status=403)
  delete_user(username)
  return Response(status=200)

@app.route('/upload/<id>',methods=["POST"])
def upload(id):
  if(request.method=="GET"):
    return Response(status = 400)
  #get api key 
  username = request.headers.get("api-key")
  file = request.files['file']
  #check if the user exist
  users= get_users()
  if(username+'/' not in users):
    return Response(status=403)
  #check if filename is already taken
  userfiles= get_user_files(username)
  if("{}/{}".format(username,id) in userfiles):
    return Response(status=403)
  #if user exist and filename not taken, upload
  upload_file(username,file,id)
  return Response(status=200)

@app.route('/files')
def files():
  #get api key 
  username = request.headers.get("api-key")
  #check if the user exist
  users= get_users()
  if(username+'/' not in users):
    return Response(status=403)
  #if user exist: return all of that user's files  
  return Response(data=get_user_files(username),status=200) 
    

@app.route('/files/<id>')
def filesContent(id):
  #get apikey
  username = request.headers.get("api-key")
  # check if user exist
  users= get_users()
  if(username+'/' not in users):
    return Response(status=403)
  #check if file exist
  userfiles= get_user_files(username)
  #if file exist return that
  if("{}/{}".format(username,id) in userfiles):
    return Response(data=getfilecontent,status=200)
  #else return 403 
  return Response(status=403)


@app.route('/delete/<id>')
def deleteContent(id):
  #get apikey
  username = request.headers.get("api-key")
  # check if user exist
  users = get_users()
  if(username+'/' not in users):
    return Response(status=403)
  #check if file exist
  userfiles= get_user_files(username)
  print(userfiles)
  if("{}/{}".format(username,id) in userfiles):
    delete_file(username,id)
    return Response(status=200)
  return Response(status=403)

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')