import json
import bcrypt
import pytest
from sqlalchemy import create_engine

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
    new_user = {
        'id' : 1,
        'name' : 'pst',
        'email' : 'taekgutv@gmail.com',
        'profile' : 'test profile',
        'hashed_password' : hashed_password
    }

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

def teardown_function():
    database.execute


def test_ping(api):
    resp = api.get('/ping')
    assert b'pong' in resp.data


def test_tweet(api):
    new_user = {
        "name": "pst",
        "email": "taekgutv6@gmail.com",
        "password": "pstpw",
        "profile": "Data Engineer"
    }
    resp = api.post(
        "/sign-up",
        data=json.dumps(new_user),
        content_type="application/json"
    )
    assert resp.status_code == 200

    resp_json = json.loads(resp.data.decode('utf-8'))
    new_user_id = resp_json['id']

    resp = api.post(
        '/login',
        data=json.dumps({'email': 'taekgutv6@gmail.com', 'password': 'pstpw'}),
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
    resp = api.get(f'/timeline/{new_user_id}')
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
