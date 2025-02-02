# test_db.py

import unittest
from peewee import *

from app import TimelinePost
from playhouse.shortcuts import model_to_dict

MODELS = [TimelinePost]


test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):

        test_db.drop_tables(MODELS)
        test_db.close()

    def test_create_timeline_post(self):
        first_post = TimelinePost.create(name='John Doe', email='john@example.com', content="Hello world, I\'m John Doe")
        assert first_post.id == 1
        first_post = TimelinePost.create(name='Jane Doe', email='jane@example.com', content="Hello world, I\'m Jane Doe")
        assert first_post.id == 2
    
        get_first = model_to_dict(TimelinePost.get_by_id(1))
        assert get_first['name'] == 'John Doe'
        get_second = model_to_dict(TimelinePost.get_by_id(2))
        assert get_second['name'] == 'Jane Doe'

    