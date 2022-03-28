import sys
import requests_call as tv_client
import boto3, json


AWS_ACCESS_KEY = 'AKIAJHQ7I5KGYVIOUNQQ'
AWS_ACCESS_SECRET_KEY = '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'
S3_BUCKET_NAME = 'mdawadud'


n = len(sys.argv)

if(n==1):
  print("Please Enter a Month in yyyy-dd Format")
elif(n>2):
  print("Please Enter Only One Month in yyyy-dd Format")
else:
  month = str(sys.argv[1])
  print("Processing Excecution of "+sys.argv[0])
    
  print("Passed Argument:", month)
  dict_shows = tv_client.fetchAllShows()
  dict_shows_ep = tv_client.fetchAllShowsEpisodes()
    
  dict_mon1 = tv_client.fetchAllShowsByMonthWithDate(month, dict_shows_ep)
    
  if(dict_mon1["status"]==200):      
    s3 = boto3.resource('s3',
    region_name='us-east-2',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_ACCESS_SECRET_KEY).Bucket(S3_BUCKET_NAME)
    json.dump_s3 = lambda obj, f: s3.Object(key=f).put(Body=json.dumps(obj))
        
    file = None
    key = ""
    fetched_rec = [item for item in dict_mon1['list']]
    show_list = []
    for show_details in dict_shows.get("list"):
      for item in fetched_rec:
        if len(item["date_list"])>0:
          key = str(len(item['date_list']))+"/"+show_details["name"].replace(" ","_")
          print("Saving file: "+key)
          json.dump_s3(item['date_list'], key)
                        
    else:
      print(dict_mon1["message"])
