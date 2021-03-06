from flask import Flask
from flask import render_template, redirect, url_for
from flask import request
from flask import jsonify

import json
import logging

import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

"""
デフォルトルート
"""
@app.route('/')
def home():
    return render_template('index.html')


"""
予約カレンダー
"""
@app.route('/login/reservation', methods=['GET'])
def reserve():
    pass


"""
ログインメニューテーブル
"""
@app.route('/login', methods=['POST'])
def logIn():
    if request.method == 'POST':
        requestId = request.values['number']
        requestPassword = request.values['password']
        logger.info({
            'action': 'login',
            'id': type(requestId),
            'pswd': type(requestPassword)
        })

        authId = '09019429814'
        authPassword = 'etsudatsujicho'

        if requestId == authId and requestPassword == authPassword:
            logger.info({
                'action': 'if run'
            })
            return render_template('login_menu.html')
        else:
            return None



"""
予約カレンダー
"""
@app.route('/calendar', methods=['GET', 'POST'])
def get_calendar():
    logger.info({
        'action': 'calendar',
        'status': 'run',
    })
    return render_template('login_calendar.html')


"""
予約フォーム
"""
@app.route('/reservation', methods=['POST'])
def reservation():
    logger.info({
        'action': 'reservation',
        'status': 'run',
    })
    name = request.values['name']
    address = request.values['address']
    time = request.values['time']
    number = request.values['number']
    course = request.values['course']
    description = request.values['description']

    data = {
        'name': name,
        'address': address,
        'time': time,
        'number': number,
        'course': course,
        'description': description
    }

    logger.info({
        'action': 'reservation',
        'data': data,
        'data type': type(data)
    })

    res = db.Db.post_reservation(data)

    responseData = {
        'data': res
    }
    logger.info({
        'action': 'reservation',
        'response': responseData,
        'response type': type(responseData)
    })

    return responseData







@app.route('/post_db', methods=['POST'])
def post_request():
    logger.info({
        'action': 'post_request',
        'status': 'run',
    })

    data = request.get_json()

    logger.info({
        'action': 'post_request',
        'request': data,
        'request type': type(data)
    })

    #seatModalを呼び出す処理
    if(data['section'] == 1):
        language = data['languageId']
        seats = []
        for seatId in data['seatsIds']:
            seats.append(seatId['type'])

        logger.info({
            'action': 'jsonify',
            'language': language,
            'seats': seats,
            'data': type(data)
        })
        res = db.Db.post_seat(language, seats)

    # menuModalを呼び出す処理
    elif data['section'] == 2:
        language = data['languageId']
        category = data['category']
        types = data['type']

        logger.info({
            'action': 'jsonify',
            'language': language,
            'category': category,
            'type': types
        })
        res = db.Db.post_menu(language, category, types)


    responseData = {
        'data': res
    }

    logger.info({
        'action': 'get_db',
        'response': responseData,
        'response type': type(responseData)
    })

    return responseData



"""
メニューデータを取得する処理
"""
@app.route('/get_db', methods=['GET', 'POST'])
def get_request():

    logger.info({
        'action': '/get_db',
        'status': 'run',
    })

    #androidからのリクエストに対する処理
    if request.method == 'POST':
        #jsonデータを受け取り中のデータを取得する処理
        json_data = request.get_json()  #typeはdict型
        json_value_data = json_data['data']
        table = json_value_data['table']
        id = json_value_data['languageId']
        logger.info({
            'action': '/get_db, android',
            'table': table,
            'id': id
        })
        res = db.Db.get_all_menu(table, id)
        responseData = {
            'data': res
        }
        logger.info({
            'action': '/get_db, response',
            'response': responseData,
            'response type': type(responseData)
        })
        return jsonify(responseData)

    #webブラウザからのリクエストに対する処理
    else:
        table = request.values['table']
        logger.info({
            'action': '/get_db browser',
            'table': table
        })
        res = db.Db.get_all_menu(table)
        responseData = {
            'data': res
        }
        logger.info({
            'action': '/get_db, response',
            'response': responseData,
            'response type': type(responseData)
        })

        return responseData


"""
編集ウィンドウの保存ボタンを押した際の処理
"""
@app.route('/save_menu', methods=['PUT', 'POST'])
def save_menu_data():
    logger.info({
        'action': 'put_menu_data',
        'status': 'run',
    })
    data = request.get_json()
    logger.info({
        'action': 'put_menu_data',
        'request': data,
        'request type': type(data)
    })

    if request.method == 'PUT':
        res = db.Db.put_menu_data(data)

    elif request.method == 'POST':
        res = db.Db.post_menu_data(data)

    responseData = {
        'data': res
    }

    logger.info({
        'action': 'put_menu_data responseData',
        'responseData': responseData,
        'response type': type(responseData)
    })

    return responseData


"""
編集ウィンドウの削除ボタンを押した際の処理
"""
@app.route('/delete_menu', methods=['DELETE'])
def delete_menu_data():
    logger.info({
        'action': 'delete_menu_data',
        'status': 'run',
    })
    data = request.values['id']
    logger.info({
        'action': 'delete_menu_data',
        'request': data,
        'request type': type(data)
    })

    res = db.Db.delete_menu_data(data)

    responseData = {
        'data': res
    }

    logger.info({
        'action': 'delete_menu_data responseData',
        'responseData': responseData,
        'response type': type(responseData)
    })

    return responseData


if __name__ == '__main__':
    app.debug = True
    app.run()