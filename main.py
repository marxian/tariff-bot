#!/usr/bin/env python
#

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
#from google.appengine.dist import use_library
#use_library('django', '1.3')
import urllib
import logging
#import csv, StringIO
import json
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
#from django import template
from django.utils.safestring import SafeString
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch
from gviz_api import DataTable
from datetime import date
import urllib

class Welcome(webapp.RequestHandler):
  def get(self):
    question = self.request.get("q")
    if question != '':
      form = { "q": question }
      form_data = urllib.urlencode(form)
      resp = urlfetch.fetch("http://localhost:8080/ask", payload=form_data, method="POST", follow_redirects=False)
      if resp.status_code == 200:
        logging.debug("OK")
        logging.debug(result.content)
      else:
        logging.debug("FAILED ON QUESTION")
        pass
      country = 'US'
      indicator = 'TM.TAX.MRCH.SM.AR.ZS'
      pass
    else:
      country = self.request.get("country")
      indicator = self.request.get("indicator")
      pass
    start = self.request.get("start")
    if start == '':
      start = '2000'
    end = self.request.get("end")
    if end == '':
      end = '2012'
    country = self.request.get("country")
    indicator = self.request.get("indicator")
    if indicator == '':
      indicator = 'TM.TAX.MRCH.SM.AR.ZS'
      pass
    data = {}

    country_code = country.lower()
    indicator = indicator.upper()
    url = "http://api.worldbank.org/countries/" + country_code + "/indicators/" + indicator + "?" + \
    "date=" + start + ":" + end + "&" + "format=" + "json"
               
    resp = urlfetch.fetch(url, method="GET", follow_redirects=True)
    if resp.status_code == 200:
      logging.debug(resp.status_code)
      try:
        data = json.loads(resp.content)
      except:
        logging.info(resp.content)
        pass
    else:
       logging.debug(resp.status_code)
       logging.debug(resp.content)
       pass
    rows={}
    old_viz_data=[]
    viz_data=[]
    countries={}
    if True:
      for row in data[1]:
        key = row['country']['id']
        countries[key]=row['country']['value']
        try:
          rows[row['date']][key]=row['value']
        except:
          rows[row['date']]={}
          rows[row['date']][key]=row['value']
        pass
      
      for yr in rows.keys():
        viz_row = {"date": date(int(yr),1,1)}
        for k in rows[yr].keys():
          try:
            viz_row[k] = float(rows[yr][k])
          except:
            viz_row[k] = None
            pass
          pass
        viz_data.append( viz_row )


      chart_data={}    
      chart_data['cols'] = [{'id':'date' , 'label':'Date', 'type':'number'},
                            {'id':'value', 'label':'Value', 'type':'number'}]
      chart_data['rows'] = rows
      pass

    indicator_value = data[1][0]['indicator']['value']  

    viz_desc = {"date": ("date", "Date")}
    order=["date"]
    for k in countries.keys():
      viz_desc[k] = ("number", countries[k])
      order.append(k)

    data_table = DataTable( viz_desc )
    data_table.LoadData( viz_data )
    template_values = {
            'start' : start,
            'end' : end,
            'country' : country,
            'indicator': indicator,
            'data' : data_table.ToJSon(columns_order=order, order_by="date"),
            'title' : SafeString( indicator_value )
            }

    if self.request.path == '/':
         path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
    else:
        path = os.path.join(os.path.dirname(__file__), 'templates' + self.request.path)
        pass

    self.response.out.write(template.render(path, template_values))
    return
  pass

application = webapp.WSGIApplication([
    ('.+',Welcome)], debug=False)

def main():
  run_wsgi_app(application)
if __name__ == '__main__':
  main()
