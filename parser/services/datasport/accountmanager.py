from pyquery import PyQuery
import HttpUtils
from Auth import is_logged_in,incorrect_login
import pickle
import urllib,urllib2
import json
import os
import logging,logging.config
logging.config.fileConfig('logger.conf')
logger = logging.getLogger(__name__)

def get_user_data(session,args):
        session_id = HttpUtils.get_user_session_id()
        user_id = pickle.load(open( HttpUtils.session_dir+'.id.'+session_id, "rb" ))
        url_datasport = 'https://online.datasport.pl/zapisy/portal/hid/edytuj.php'
        url_post_data = {'id': session['user'], 'los': 42311 }
        post_data_encoded = urllib.urlencode(url_post_data)
        request_object = urllib2.Request(url_datasport+"?"+post_data_encoded)
        request_object.add_header("Cookie", session['cookie'])
        response = urllib2.urlopen(request_object)
        query = PyQuery(response.read())
        user_info = {}
        user_info['email'] = query("#email").val()
        user_info['name_surname'] = query("#nazwisko").val() + " " + query("#imie").val()
        user_info['birth_date'] = query("#dzienur option:selected").text()+'-'+query("#miesur option:selected").text()+'-'+query("#rokur option:selected").text()
        user_info['sex'] = query("#plec option:selected").text()
        user_info['address'] = query("#adres").val()
        user_info['post_code'] = query("#kodp").val()
        user_info['city'] = query("#miasto").val()
        user_info['country'] = query("#kraj option:selected").text()
        user_info['nationality'] = query("#obywatel option:selected").text()
        user_info['state'] = query("#wojew option:selected").text()
        user_info['phone'] = query("#sms1").val()
        user_info['club'] = query("#klub").val()
        user_info['hide_results'] = query("#zastrzezone").val()
        return user_info

