import json

import bcrypt
import pytest
from sqlalchemy import create_engine, text

import config
from app import create_app

database = create_engine(config.test_config['DB_URL'], encoding='utf-8', max_overflow=0)


# 가상의 HTTP 요청을 전송하여 TEST
@pytest.fixture
def api():
    app = create_app(config.test_config)
    app.config['TEST'] = True
    api = app.test_client()
    return api


def setup_function():
    hashed_password = bcrypt.hashpw(
        b"test password",
        bcrypt.gensalt()
    )
    new_user = [
        {
            'id': 1,
            'name': 'pst',
            'email': 'taekgutv@gmail.com',
            'profile': 'test profile',
            'hashed_password': hashed_password
        },
        {
            'id': 2,
            'name': 'pst2',
            'email': 'taekgutv2@gmail.com',
            'profile': 'test profile',
            'hashed_password': hashed_password
        }
    ]

    database.execute(text("""
        INSERT INTO users(
            id,
            name,
            email,
            profile,
            hashed_password
        ) VALUES (
            :id,
            :name,
            :email,
            :profile,
            :hashed_password
        )
    """), new_user)

    database.execute(text("""
        INSERT INTO tweets (
            user_id,
            tweet
        ) VALUES (
            2,
            "Hello World!"
        )
    """))


def teardown_function():
    database.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    database.execute(text("TRUNCATE users"))
    database.execute(text("TRUNCATE tweets"))
    database.execute(text("TRUNCATE users_follow_list"))
    database.execute(text("SET FOREIGN_KEY_CHECKS=1"))


def test_ping(api):
    resp = api.get('/ping')
    assert b'pong' in resp.data


def test_login(api):
    # login
    resp = api.post(
        '/login',
        data=json.dumps({'email': 'taekgutv@gmail.com', 'password': 'test password'}),
        content_type='application/json'
    )
    assert b"access_token" in resp.data


def test_unauthorized(api):
    resp = api.post(
        '/tweet',
        data=json.dumps({'tweet': 'Hello World!'}),
        content_type='application/json'
    )
    assert resp.status_code == 401

    resp = api.post(
        '/follow',
        data=json.dumps({'follow': 2}),
        content_type='application/json'
    )
    assert resp.status_code == 401

    resp = api.post(
        '/unfollow',
        data=json.dumps({'unfollow': 2}),
        content_type='application/json'
    )
    assert resp.status_code == 401


def test_tweet(api):
    resp = api.post(
        '/login',
        data=json.dumps({'email': 'taekgutv@gmail.com', 'password': 'test password'}),
        content_type='application/json'
    )
    resp_json = json.loads(resp.data.decode('utf-8'))
    access_token = resp_json['access_token']

    # tweet
    resp = api.post(
        '/tweet',
        data=json.dumps({'tweet': "Hello World!"}),
        content_type='application/json',
        headers={'Authorization': access_token}
    )
    assert resp.status_code == 200

    # tweet 확인
    resp = api.get(f'/timeline/1')
    tweets = json.loads(resp.data.decode('utf-8'))

    assert resp.status_code == 200
    assert tweets == {
        'user_id': 1,
        'timeline': [
            {
                'user_id': 1,
                'tweet': "Hello World!"
            }
        ]
    }


def test_follow(api):
    resp = api.post(
        '/login',
        data=json.dumps({'email': 'taekgutv@gmail.com', 'password': 'test password'}),
        content_type='application/json'
    )
    resp_json = json.loads(resp.data.decode('utf-8'))
    access_token = resp_json['access_token']

    ## 먼저 유저 1의 tweet 확인 해서 tweet 리스트가 비어 있는것을 확인
    resp = api.get(f'/timeline/1')
    tweets = json.loads(resp.data.decode('utf-8'))

    assert resp.status_code == 200
    assert tweets == {
        'user_id': 1,
        'timeline': []
    }

    # follow 유저 아이디 = 2
    resp = api.post(
        '/follow',
        data=json.dumps({'id': 1, 'follow': 2}),
        content_type='application/json',
        headers={'Authorization': access_token}
    )
    assert resp.status_code == 200

    resp = api.get(f'/timeline/1')
    tweets = json.loads(resp.data.decode('utf-8'))

    assert resp.status_code == 200
    assert tweets == {
        'user_id': 1,
        'timeline': [
            {
                'user_id': 2,
                'tweet': "Hello World!"
            }
        ]
    }


def test_unfollow(api):
    # 로그인
    resp = api.post(
        '/login',
        data=json.dumps({'email': 'taekgutv@gmail.com', 'password': 'test password'}),
        content_type='application/json'
    )
    resp_json = json.loads(resp.data.decode('utf-8'))
    access_token = resp_json['access_token']

    # follow 유저 아이디 = 2
    resp = api.post(
        '/follow',
        data         = json.dumps({'id': 1,'follow' : 2}),
        content_type = 'application/json',
        headers = {'Authorization': access_token}
    )

    assert resp.status_code == 200


    resp = api.get(f'/timeline/1')
    tweets = json.loads(resp.data.decode('utf-8'))

    assert resp.status_code == 200
    assert tweets == {
        'user_id': 1,
        'timeline': [
            {
                'user_id': 2,
                'tweet': "Hello World!"
            }
        ]
    }

    # unfollow 유저 아이디 = 2
    resp = api.post(
        '/unfollow',
        data=json.dumps({'id': 1, 'unfollow': 2}),
        content_type='application/json',
        headers={'Authorization': access_token}
    )
    assert resp.status_code == 200

    resp = api.get(f'/timeline/1')
    tweets = json.loads(resp.data.decode('utf-8'))

    assert resp.status_code == 200
    assert tweets == {
        'user_id': 1,
        'timeline': []
    }
