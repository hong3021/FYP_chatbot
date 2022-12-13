from flask import Blueprint, render_template, request, jsonify
from website.chatbot import response_message
from flask_login import login_required, current_user
from .model import User
from .model import Chatlog
import re
from . import db

import website.Osintgram as osint
import json

views = Blueprint('views', __name__)

file = True
json = True
output = 'website/output'
cookies = True
command = False


@views.route('/')
# @login_required
def home():
    return render_template('home.html', user=current_user)


@views.route('/osint')
@login_required
def osint_search():
    return render_template('osint.html', user=current_user)


@views.route('/chatBox')
@login_required
def chat_box():
    return render_template('chatInterface.html', user=current_user)


@views.post("/predict")
def predict():
    answer = ''
    text = request.get_json().get("message")
    # TODO: check if text is valid

    if re.search("search", text):
        username = str(text).split()[1]
        api = osint.Osintgram(username, file, json, command, output, cookies)
        info = api.get_user_info()
        message = {"answer": info}
        answer = ','.join(map(str, info))
    else:
        answer = response_message(text)
        message = {"answer": answer}

    if current_user.id:
        new_chatlog = Chatlog(message=text, answer=answer, user_id=current_user.id)
        db.session.add(new_chatlog)
        db.session.commit()
    return jsonify(message)


@views.post('/search')
def search_data():
    username = request.get_json().get("username")
    add = request.get_json().get("find_address")
    # search_address = request.get_json().get("find_address")
    # api = osint.Osintgram(username, file, json, command, output, cookies)
    # api.get_user_propic()
    # info = api.get_user_info()
    info = {"id": 478948082, "full_name": "\u76ae\u76ae\u266117Baby", "biography": "\u4e00\u500b\u61f6\u60f0\u7684\u4eba\u8207\u4e00\u96bb\u770b\u4f3c\u53ad\u4e16\u537b\u611b\u6492\u5b0c\u7684\u8c93\ud83d\ude3d\n\ud83d\udc47\ud83c\udffb\u7c89\u5c08\u6709\u6bcf\u9031\u884c\u7a0b\u53ca\u66f4\u591a\u7167\u7247\u5466\ud83d\udc47\ud83c\udffb", "edge_followed_by": 84109, "edge_follow": 664, "is_business_account": True, "is_verified": False, "profile_pic_url_hd": "https://instagram.fkul4-3.fna.fbcdn.net/v/t51.2885-19/278798311_714848619698431_7271821634817120572_n.jpg?_nc_ht=instagram.fkul4-3.fna.fbcdn.net&_nc_cat=107&_nc_ohc=2QL-8t4Z9DIAX_t-RXX&edm=AIRHW0ABAAAA&ccb=7-5&oh=00_AfCsEbUQ9LXzftH-zQ91qQJ0qskGjBiyYKfYY2vBXtJoJA&oe=639AEFAD&_nc_sid=e3b034", "email": "mayday830328@yahoo.com.tw"}

    if add:
        # address = api.get_addrs()
        address = {"address": [{"address": "TREC, Pudu, Kuala Lumpur, 55100, Malaysia", "time": "2022-12-04 21:13:01"}, {"address": "Troy University, University Avenue, Ridgewood, Troy, Pike County, Alabama, 36082, United States", "time": "2022-11-25 14:26:40"}, {"address": "\u4eac\u738b\u30d7\u30ec\u30c3\u30bd\u30a4\u30f3, \u7532\u5dde\u8857\u9053, \u897f\u65b0\u5bbf\u4e09\u4e01\u76ee, \u65b0\u5bbf\u533a, \u6771\u4eac\u90fd, 163-8001, \u65e5\u672c", "time": "2022-11-21 21:18:34"}, {"address": "\u4e2d\u5c71\u5317\u8def\u4e94\u6bb5, \u798f\u6797\u91cc, \u58eb\u6797\u5340, \u77f3\u89d2, \u81fa\u5317\u5e02, 11111, \u81fa\u7063", "time": "2022-11-18 22:06:36"}, {"address": "\u53f0\u5317101\u8cfc\u7269\u4e2d\u5fc3, 45, \u5e02\u5e9c\u8def, \u897f\u6751\u91cc, \u4fe1\u7fa9\u5340, \u4fe1\u7fa9\u5546\u5708, \u81fa\u5317\u5e02, 11001, \u81fa\u7063", "time": "2022-11-17 20:30:57"}, {"address": "\u4ee3\u5929\u5e9c, \u745e\u91d1\u516c\u8def, \u57fa\u5c71\u91cc, \u745e\u82b3\u5340, \u4e5d\u4efd, \u65b0\u5317\u5e02, 22448, \u81fa\u7063", "time": "2022-11-16 20:07:41"}, {"address": "Building \u2116 4, Jesus Street, Paco, Fifth District, Manila, Capital District, Metro Manila, 1007, Philippines", "time": "2022-11-15 21:20:56"}, {"address": "\u9280\u5ea7, \u6674\u6d77\u901a\u308a, \u6709\u697d\u753a\u4e00\u4e01\u76ee, \u6709\u697d\u753a, \u5343\u4ee3\u7530\u533a, \u6771\u4eac\u90fd, 104-0061, \u65e5\u672c", "time": "2022-11-11 22:20:08"}, {"address": "\u6771\u4eac\u30bf\u30ef\u30fc, \u6771\u4eac\u30bf\u30ef\u30fc\u901a\u308a, \u829d\u516c\u5712\u4e09\u4e01\u76ee, \u6e2f\u533a, \u6771\u4eac\u90fd, 106-0041, \u65e5\u672c", "time": "2022-11-10 21:16:16"}]}
        info.update(address)

    return jsonify(info)





