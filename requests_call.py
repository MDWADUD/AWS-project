import requests
import datetime

def fetchAllShows():
  dict_resp = {}
  dict_shows = {}
  shows_list = [];
  dict_resp["list"] = shows_list
  resp = requests.get("http://api.tvmaze.com/shows")
  ok_flag = False
  try:
    if resp.status == 404:
        dict_resp["_status_desc"] = 'GET /tasks/ {}'.format(resp.status)
        dict_resp["_status_code"] = resp.status
    else:
      dict_resp["_status_desc"] = 'GET /tasks/ {}'.format(resp.status_code)
      dict_resp["_status_code"] = resp.status_code
  except:
    dict_resp["_status_desc"] = 'GET /tasks/ {}'.format(resp.status_code)
    dict_resp["_status_code"] = resp.status_code
  
    if(dict_resp["_status_code"]==200):
      ok_flag = True
                
    if ok_flag:
      for todo_item in resp.json():
        dict_shows["id"] = todo_item['id']
        dict_shows["url"] = todo_item['url']
        dict_shows["name"] = todo_item['name']
        dict_shows = todo_item
        shows_list.append(dict_shows)
        dict_shows = {}
      dict_resp["list"] = shows_list
    return dict_resp

def fetchAllShowsEpisodes(show_dict_resp=None):
  base_url = "http://api.tvmaze.com/shows/<show_id>/episodes"
    
  if show_dict_resp is None:
    show_dict_resp = fetchAllShows()
  show_id_list = [d["id"] for d in show_dict_resp.get("list")]
    
  air_date_list = []
  dict_resp = {}
  dict_resp_list = []
    
  for each_show in progressBar(show_id_list, prefix = 'Please Wait while the Program is Loading:', suffix = 'Complete', length = 50):
    dict_resp["show_id"]=each_show
    resp = requests.get(base_url.replace("<show_id>", str(each_show)))
    for todo_item in resp.json():
      air_date_list.append(todo_item["airdate"])
    dict_resp["air_date_list"]=air_date_list    
    dict_resp_list.append(dict_resp)
    air_date_list = []
    dict_resp = {}
                
    return dict_resp_list


def fetchAllShowsByMonth(month_url, episodes_dict=None):
  dict_resp = {}
  aired_show_list = []
  dict_resp["list"] = aired_show_list
    
  if episodes_dict is None:
    episodes_dict = fetchAllShowsEpisodes()
    
  date_range = get_day_dist_of_month(month_url)
  status_code = 200
  if(date_range["status"]==1):
    for each_day in date_range["range"]:
      for each_show_dict in episodes_dict:
        if each_show_dict["show_id"] not in aired_show_list:
          if(each_day in each_show_dict['air_date_list']):
            aired_show_list.append(each_show_dict['show_id'])
    if len(aired_show_list)==0:
      dict_resp["message"] = "No shows found"
    else:
      dict_resp["message"] = str(len(aired_show_list))+" shows found"
      dict_resp["status"] = status_code
      dict_resp["list"] = aired_show_list
  else:
    dict_resp["status"] = 400
    dict_resp["message"] = date_range['message']
    dict_resp["list"] = []
  return dict_resp

def fetchAllShowsByMonthWithDate(month_url, episodes_dict=None):
  dict_resp = {}
  aired_show_list = []
  dict_resp["list"] = aired_show_list
    
  if episodes_dict is None:
    episodes_dict = fetchAllShowsEpisodes()
    
  date_range = get_day_dist_of_month(month_url)
  status_code = 200
  if(date_range["status"]==1):
    for each_show_dict in episodes_dict:
      show_dates = []
      for each_day in date_range["range"]:
        if(each_day in each_show_dict['air_date_list']):
          show_dates.append(each_day)
        aired_show_list.append({"show_id": each_show_dict['show_id'], "date_list": show_dates})
        if len(aired_show_list)==0:
          dict_resp["message"] = "No shows found"
        else:
          dict_resp["message"] = str(len(aired_show_list))+" shows found"
        dict_resp["status"] = status_code
        dict_resp["list"] = aired_show_list
        dict_resp["show_id"] = each_show_dict['show_id']
    else:
      dict_resp["status"] = 400
      dict_resp["message"] = date_range['message']
      dict_resp["list"] = []
    return dict_resp

def get_day_dist_of_month(month_str):
  dict_resp = {}
  dict_resp["status"] = 1
  dict_resp["message"] = "Success"
  date_list = []
  dict_resp["range"] = date_list
  try:
    date_time_str = month_str
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m')
        
    last_day_str = (date_time_obj.date() + datetime.timedelta(days=32)).strftime("%Y-%m")
    last_date_obj = datetime.datetime.strptime(last_day_str, '%Y-%m').date() - datetime.timedelta(days=1)
    last_day_str = last_date_obj.strftime("%Y-%m-%d")

    for i in range(0,last_date_obj.day):
      date_t = (date_time_obj.date() + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
      date_list.append(date_t)
    dict_resp["range"] = date_list
  except:
        dict_resp["status"] = 0
        dict_resp["message"] = "Invalid date format"
        dict_resp["range"] = []
  return dict_resp

# for extra credits 
def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
      yield item
      printProgressBar(i + 1)
    # Print New Line on Complete
    print()
 

#print(fetchAllShowsByMonth('2013-07'))
#print(fetchAllShows('http://api.tvmaze.com/shows'));
