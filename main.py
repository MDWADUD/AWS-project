import requests_call as tv_client
from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

global dict_shows
global dict_shows_ep

class LogRequests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accesstime = db.Column(db.String(100), nullable = False)
    call = db.Column(db.String(500), nullable = False)

db.create_all()

dict_shows = {}
dict_shows_ep = {}

def run_server():
  global dict_shows
  global dict_shows_ep
  dict_shows = tv_client.fetchAllShows()
  dict_shows_ep = tv_client.fetchAllShowsEpisodes()
  app.run(debug=True,use_reloader=False, port=5000)
    
class GetShows(Resource):
  global dict_shows
  global dict_shows_ep
  def get(self, month1, month2):
    print("Calling... /diff/"+month1+"/"+month2)
        
    date_time_str = datetime.datetime.now().strftime('%B %d, %Y %H:%M %p')
    url = "/diff/"+month1+"/"+month2
        
    dict_mon1 = tv_client.fetchAllShowsByMonth(month1, dict_shows_ep)
    dict_mon2 = tv_client.fetchAllShowsByMonth(month2, dict_shows_ep)
    #print(dict_mon1)
    #print(dict_mon2)
    show_id_list = [item for item in dict_mon2['list'] if item not in dict_mon1['list']]
    show_list = []
    for show_details in dict_shows.get("list"):
      if show_details["id"] in show_id_list:
        show_list.append({"id":show_details['id'],"name":show_details['name'], "url":show_details['url']})
        count = len(show_id_list)
        message = "Shows aired in month "+month2+" but not aired in "+month1
        log_request = LogRequests(accesstime=date_time_str, call=url)
        db.session.add(log_request)
        db.session.commit()
        return {"count": count, "message": message, "show_list": show_list}
    
class GetRequestLog(Resource):
  def get(self):
    log_requests = LogRequests.query.all()
    req_list = []
    for each_rec in log_requests:
      req_list.append({"datetime": each_rec.accesstime, "call": each_rec.call})
    return req_list
    
api.add_resource(GetShows, "/diff/<string:month1>/<string:month2>")
api.add_resource(GetRequestLog, "/list")
        
if __name__ == "__main__":
  run_server()
