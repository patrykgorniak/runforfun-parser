from pyquery import PyQuery
from parser.services.datasport.authorization import los

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
