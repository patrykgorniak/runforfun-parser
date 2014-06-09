from pyquery import PyQuery
import re

def get_id(data):
    query = PyQuery(data)
    user_id = re.search("id=([0-9]*)",query('script').eq(2).text())
    if len(user_id.groups()) > 0:
        return user_id.groups()[0]
    else:
        return -1

def get_user_data(data):
    query = PyQuery(data)
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

def get_user_events(data):
    user_events = {}
    query = PyQuery(data)("#platnosci")("table")("tr")
    print(query.eq(0))

    for iter, row in enumerate(query):
        row_data = {}
        row_data["title"]  = str(query.eq(iter)("td").eq(0)("a").html()).replace(r"<br />", ";")
        row_data["sign_in_url"] = query.eq(iter)("td").eq(0)("a").attr("href")
        row_data["edit_url"] = query.eq(iter)("td").eq(2)("a").attr("href")
        row_data["state"] = query.eq(iter)("td").eq(1).text()
        user_events[iter] = row_data

    return user_events
