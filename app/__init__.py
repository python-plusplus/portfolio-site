import os
from typing import Any

import requests
from flask import Flask, make_response, render_template, request, redirect, url_for
from dotenv import load_dotenv
from peewee import *
import datetime

from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__, static_folder='static')

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)

else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306 )

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost])
# Base content all pages need
# used by the "profile" section of the template
base_content = {
    'name': 'Sunny Kim',
    'position': 'Software Engineer',
    'url': os.getenv("URL"),
    'socials': [{
        'name': 'Github',
        'url': 'https://github.com/python-plusplus',
        'icon': './static/img/social/github.svg'
    }, {
        'name': 'LinkedIn',
        'url': 'https://www.linkedin.com/in/sunghyoun-kim-583648217/',
        'icon': './static/img/social/linkedin.svg'
    }]
}


@app.route('/api/timeline_post', methods=["POST"])
def post_timeline_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']

    name = request.form['name']
    content = request.form['content']
    email = request.form['email']
    if name == "":
        return "Invalid name", 400
    elif not "@" in email:
        return "Invalid email", 400
    elif content == "":
        return "Invalid content", 400
    else: 
        timeline_post = TimelinePost.create(name=name, email=email, content=content)
        return model_to_dict(timeline_post)


@app.route('/api/timeline_post')
def get_timeline_post():
        return {
            'timeline_posts': [
                model_to_dict(p) for p in
                TimelinePost.select().order_by(TimelinePost.created_at.desc())
            ]
        }


@app.route('/api/timeline_post', methods=['DELETE'])
def delete_timeline_post():
    try:
        to_del = TimelinePost.get(TimelinePost.id == request.form['id'])
        to_del.delete_instance()
        return {'success': 'true'}

    except:
        return {'success': 'false'}


@app.route('/')
def index():
    # no extra content needed
    # title and active_tab handled by `handle_route`
    return handle_route('Home', 'index', base_content)


@app.route('/about')
def about():
    content = {
        **base_content,
        'quote': 'Only one who devotes himself to a cause with his whole strength and soul can be a true master. For this reason mastery demands all of a person.',
        'author': 'Albert Einstein',
    }
    return handle_route('About', 'about', content)


@app.route('/work')
def work():
    content = {
        **base_content,
        'jobs': [{
            'name': 'Computer programmer',
            'location': 'Memory Lane',
            'contact': '127.255.255.255',
            'description': 'Today I walked down a street where many computer programmers live. The houses were numbered 64k, 128k, 256k, 512k and 1MB. For some reason it felt like a trip down memory lane.'
        }]
    }
    return handle_route('Work Experiences', 'work', content)


@app.route('/education')
def education():
    content = {
        **base_content,
        'educations': [{
            'school': 'University of Toronto',
            'degree': 'Bachelor of Science',
            'major': 'Computer Science',
            'years': '2022 - 2025'
        }]
    }
    return handle_route('Education', 'education', content)


@app.route('/hobbies')
def hobbies():
    content = {
        'title': 'Hobbies - Portfolio',
        'active_tab': 'hobbies',
        'hobbies': [
            {
                'name': 'Chess',
                'img': 'https://images.ctfassets.net/3s5io6mnxfqz/wfAz3zUBbrcf1eSMLZi8u'
                       '/c03ac28c778813bd72373644ee8b8b02/AdobeStock_364059453.jpeg?fm=jpg&w=900'
                       '&fl=progressive',
                'desc': "I've been playing chess since I was a little kid. I've played at all "
                        "collegiate levels and have multiple competitive accomplishments in the "
                        "sport."
            },
            {
                'name': 'Bouldering',
                'img': 'https://a2cf4fa39d1096849525-c9e74d9e365a688b9dfb3e01b6ac4867.ssl.cf5'
                       '.rackcdn.com/cloud_images/Climber-at-bouldering-gym.jpg',
                'desc': "One of my favorite pastimes is bouldering. It's a great way to exercise "
                        "while solving problems with other people. I plan on bouldering even more "
                        "next year. "
            },
            {
                'name': 'Cycling',
                'img': 'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/mff-roka'
                       '-0618-1-preview-maxwidth-3000-maxheight-3000-ppi-300-quality-90'
                       '-1620433208.jpg?crop=1.00xw:0.750xh;0,0.190xh&resize=1200:*',
                'desc': "I'm an amateur cyclist and part of my local cycling club. I enjoy "
                        "exploring new routes every weekend and getting new PRs on my Strava. "
            }

        ],
        **base_content
    }
    return handle_route('Hobbies', 'hobbies', content)


@app.route('/where_am_i')
def where_am_i():
    content = {
        **base_content,
        'places': [{
            'name': 'San Francisco',
            'description': 'I am currently living in San Francisco, California (lie)',
            'coords': [37.75, -122.4]
        }, {
            'name': 'Edmonton',
            'description': 'Capital of the texas of Canada',
            'coords': [53, -113]
        }, {
            'name': 'Seattle',
            'description': 'The seat of King County, Washington',
            'coords': [47, -120]
        }, {
            'name': 'San Juan',
            'description': 'Unincorporated territory of the United States',
            'coords': [18, -66]
        }],
        **base_content
    }
    return handle_route('Where am I', 'where_am_i', content)


@app.route('/timeline')
def timeline():
    posts = TimelinePost.select() 
    
    if  len(posts) == 0:
        content = {
            **base_content,
        }    
    else:
        content = {
            **base_content,
            **requests.get('http://localhost:5000/api/timeline_post').json()
        }
    
    return handle_route('Timeline', 'timeline', content)


def handle_route(name: str, id: str, content):
    '''
    Handles routing logic for each page

    Args:
        name: Page name (Shows in the navbar)
        id: unique id for the page
        content: extra content to pass to the template
    '''
    content = {
        **content,
        'title': f'{name} - Portfolio',
        'active_tab': id,
    }
    # check prev_page cookie to see what animations we have to do
    prev_page = request.cookies.get('prev_page', None, type=str)
    print(f'prev_page for {id}: {prev_page}')
    if prev_page is None or prev_page == id:
        # This is an initial page load (user first navigates, or refreshes)
        # `initial` is used by the template to know to play the fadein animations
        content = {
            **content,
            'initial': True,
        }
    else:
        # This is not an initial page load, so set a slide animation for the content
        content = {
            **content,
            'initial': False,
            'content_slide_animation': get_animation(prev_page, id)
        }
    # set the prev_page cookie to the `id`, 
    # so the next link will know what page transition to do
    resp = make_response(render_template(f'{id}.html', **content))
    resp.set_cookie('prev_page', id)
    return resp


# from the two pages, gets the animate.css animation to play
# either a `animate__slideInLeft` or `animate__slideInRight`
def get_animation(prev_page: str, curr_page: str) -> str:
    pages = {'index': 0, 'about': 1, 'work': 2, 'education': 3, 'hobbies': 4, 'where_am_i': 5,
             'timeline': 6}
    anim = 'slideInRight' if pages[prev_page] < pages[curr_page] else 'slideInLeft'
    return f'animate__{anim}'


@app.route("/set")
@app.route("/set/<theme>")
def set_theme(theme='light'):
    res = make_response(redirect(url_for(request.cookies.get('prev_page'))))
    res.set_cookie("theme", theme)
    return res


if __name__ == '__main__':
    app.run(debug=True)
