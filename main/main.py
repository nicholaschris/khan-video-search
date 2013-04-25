import sys
sys.path.insert(0, 'lib.zip')

from google.appengine.api import mail
import flask
from flaskext import wtf
import config

app = flask.Flask(__name__)
app.config.from_object(config)
app.jinja_env.line_statement_prefix = '#'

import auth
import util
import model
import admin

# Copypaste from Dropbox/perceptum/sample-video-search 
import pprint
import json
import urllib
import csv
import webapp2
import jinja2
import cgi
import os

from apiclient.discovery import build
from optparse import OptionParser
from google.appengine.api import users

# Set DEVELOPER_KEY to the "API key" value from the "Access" tab of the
# Google APIs Console http://code.google.com/apis/console#access
# Please ensure that you have enabled the YouTube Data API for your project.

DEVELOPER_KEY = "AIzaSyCpl5TM4HFVXIfAdy1PeLByqAWrlaHEqdk"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
FREEBASE_SEARCH_URL = "https://www.googleapis.com/freebase/v1/search?%s"

# JINJA_ENVIRONMENT = jinja2.Environment(
#    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

################################################################################
# YouTube API stuff
################################################################################

def get_topic_id(top,options):
  freebase_params = dict(query=top, key=DEVELOPER_KEY, lang='nl')
  freebase_url = FREEBASE_SEARCH_URL % urllib.urlencode(freebase_params)
  freebase_response = json.loads(urllib.urlopen(freebase_url).read())

  if len(freebase_response["result"]) == 0:
    exit("No matching terms were found in Freebase.")

  mids = []
  index = 1
  for result in freebase_response["result"]:
    mids.append(result["mid"])
    return result.get("name", "unknown")
 #   with open('/Users/Vaidas/Dropbox/python/some.csv', 'wb') as fil:
 #       writer = csv.writer(fil)
 #       for row in writer:
 #           writer.writerows(result.get("name", "unknown"))

#    print "  %2d. %s (%s)" % (index, result.get("name", "Unknown"),
#      result.get("notable", {}).get("name", "Unknown"))
    index += 1
#  pprint.pprint(freebase_response)
  mid = None
#  while mid is None:
#    index = raw_input("Enter a topic number to find related YouTube %ss: " %
#      options.type)
#    try:
#      mid = mids[int(index) - 1]
#    except ValueError:
#      pass
#  return mid

def get_category_name(cat):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
  search_response = youtube.videoCategories().list(
    id=cat,
    part="snippet"
  ).execute()
  name = []
  for search_result in search_response.get("items", []):
      name = search_result["snippet"]["title"]
  return name

def stat_search(vid):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
  search_response = youtube.videos().list(
  id=vid,
    part="statistics,snippet,contentDetails"
  ).execute()

  stats = []
  for search_result in search_response.get("items", []):
      stats.append("%s %s %s %s %s %s %s %s %s %s " % (search_result["statistics"]["viewCount"],
                                 search_result["statistics"]["likeCount"],
                                 search_result["statistics"]["dislikeCount"],
                                 search_result["statistics"]["favoriteCount"],
                                 search_result["statistics"]["commentCount"],
                                 search_result["snippet"]["publishedAt"],
                                 search_result["snippet"]["title"],
                                 search_result["snippet"]["channelTitle"],
                                 get_category_name(search_result["snippet"]["categoryId"]),
                                 search_result["contentDetails"]["duration"].replace("PT","").replace("M",":").replace("S","")
                                ))
  #~ print "\n".join(stats)
  
def topic_search(vid):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
  search_response = youtube.videos().list(
  id=vid,
    part="topicDetails"
  ).execute()

  topic = []
  for search_result in search_response.get("items", []):
      topic = search_result["topicDetails"]["topicIds"]
  return topic
  
def get_video_id(options):

  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, 
    developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
    q=options.q,
#    q=key,
    part="id,snippet",
    maxResults=options.maxResults,
    videoCategoryId=options.videoCategoryId,
    safeSearch=options.safeSearch,
    type=options.type
  ).execute()

  #~ print search_response["items"]

  video_id_list = []
  title_list = []
  for search_result in search_response.get("items", []):
    video_id_list.append(search_result["id"]["videoId"])
    title_list.append(search_result["snippet"]["title"])
#    print search_result["id"]["videoId"]
  return video_id_list, title_list

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
    q=options.q,
#    q=key,
    part="id,snippet",
    maxResults=options.maxResults,
    videoCategoryId=options.videoCategoryId,
    safeSearch=options.safeSearch,
    type=options.type
  ).execute()
  
  videos = []
  topic_list = []
  playlists = []
#  pprint.pprint(search_response)
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))
      vid = search_result["id"]["videoId"]
      #~ print "\n", search_result["id"]["videoId"]
      #~ pprint.pprint(search_result["snippet"]["title"])
      try:
        stat_search(search_result["id"]["videoId"])
      except:
        pass
        #~ print "oh well"

      try:
        top = topic_search(vid)
        for topic in top:
          row = get_topic_id(topic,options)
          #~ print row
#          keyW.append(row)
      except:
        pass
        #~ print "no topics found"

#    with open('/Users/Vaidas/Dropbox/python/some.csv', 'wb') as f:
#        writer = csv.writer(f,delimiter=',')
#        writer.writerow(topic_list)

    if search_result["id"]["kind"] == "youtube#channel":
      videos.append("%s (%s)" % (search_result["snippet"]["channelTitle"],
                                 search_result["id"]["channelId"]))
    if search_result["id"]["kind"] == "youtube#playlist":
      videos.append("%s (%s)" % (search_result["snippet"]["playlistTitle"],
                                 search_result["id"]["playlistId"]))
  return search_response
  
################################################################################
# Results Stuff
################################################################################
@app.route('/results', methods=['POST', 'GET'])
def results():
  if flask.request.method == 'GET':
    search_term = flask.request.args.get('search_query', '')
    parser = OptionParser()
    parser.add_option("--q", dest="q", help="Search term",
           default=search_term)
    parser.add_option("--max-results", dest="maxResults",
          help="Max results", default=5)
    parser.add_option("--query", dest="query", help="Freebase search term",
          default="/m/057mq")
    parser.add_option("--type", dest="type", help="video/channel/playlist",
          default="video")
    parser.add_option("--videoCategoryId", dest="videoCategoryId", help="education-17?",
          default="27")
    parser.add_option("--safeSearch", dest="safeSearch", help="none/moderate/strict",
          default="moderate")
    (options, args) = parser.parse_args()
 #   video_id_list = get_video_id(options)
    search_response = youtube_search(options)
    url_for_video = flask.url_for('video', videoId=search_response['items'][0]['id']['videoId'])
    print url_for_video
 #   video_ids=[]
 #   title_list=[]
 #   video_ids_title=[]
 #   for item in xrange(0, len(video_id_list[0])):
 #       video_ids_title.append((video_id_list[0][item], video_id_list[1][item]))
#        video_ids.append(item_ids)
#        title_list.append(item_title)
  if False:
    return flask.redirect(flask.url_for('welcome'))
  return flask.render_template(
      'video-div.html',
      html_class='results',
      search_response = search_response,
      url_for_video = url_for_video
      #~ search_term=search_term,
      #~ video_ids=video_ids,
      #~ title_list=title_list,
      #~ video_ids_title = video_ids_title,
    )
    
################################################################################
# Generate URL
###############################################################################
@app.route('/video/<videoId>')
def video(videoId):
  pass

################################################################################
# Welcome Page
###############################################################################
@app.route('/')
def welcome():
  return flask.render_template(
      'welcome.html',
      html_class='welcome',
    )


################################################################################
# Profile stuff
################################################################################
class ProfileUpdateForm(wtf.Form):
  name = wtf.TextField('Name', [wtf.validators.required()])
  email = wtf.TextField('Email', [
      wtf.validators.optional(),
      wtf.validators.email('That does not look like an email'),
    ])


@app.route('/_s/profile/', endpoint='profile_service')
@app.route('/profile/', methods=['GET', 'POST'], endpoint='profile')
@auth.login_required
def profile():
  form = ProfileUpdateForm()
  user_db = auth.current_user_db()
  if form.validate_on_submit():
    user_db.name = form.name.data
    user_db.email = form.email.data.lower()
    user_db.put()
    return flask.redirect(flask.url_for('welcome'))
  if not form.errors:
    form.name.data = user_db.name
    form.email.data = user_db.email or ''

  if flask.request.path.startswith('/_s/'):
    return util.jsonify_model_db(user_db)

  return flask.render_template(
      'profile.html',
      title='Profile',
      html_class='profile',
      form=form,
      user_db=user_db,
    )


################################################################################
# Feedback
################################################################################
class FeedbackForm(wtf.Form):
  subject = wtf.TextField('Subject', [wtf.validators.required()])
  message = wtf.TextAreaField('Message', [wtf.validators.required()])
  email = wtf.TextField('Email (optional)', [
      wtf.validators.optional(),
      wtf.validators.email('That does not look like an email'),
    ])


@app.route('/feedback/', methods=['GET', 'POST'])
def feedback():
  form = FeedbackForm()
  if form.validate_on_submit():
    mail.send_mail(
        sender=config.CONFIG_DB.feedback_email,
        to=config.CONFIG_DB.feedback_email,
        subject='[%s] %s' % (
            config.CONFIG_DB.brand_name,
            form.subject.data,
          ),
        reply_to=form.email.data or config.CONFIG_DB.feedback_email,
        body='%s\n\n%s' % (form.message.data, form.email.data)
      )
    flask.flash('Thank you for your feedback!', category='success')
    return flask.redirect(flask.url_for('welcome'))
  if not form.errors and auth.current_user_id() > 0:
    form.email.data = auth.current_user_db().email

  return flask.render_template(
      'feedback.html',
      title='Feedback',
      html_class='feedback',
      form=form,
    )


################################################################################
# User Stuff
################################################################################
@app.route('/_s/user/', endpoint='user_list_service')
@app.route('/user/', endpoint='user_list')
@auth.admin_required
def user_list():
  user_dbs, more_cursor = util.retrieve_dbs(
      model.User.query(),
      limit=util.param('limit', int),
      cursor=util.param('cursor'),
      order=util.param('order') or '-created',
      name=util.param('name'),
      admin=util.param('admin', bool),
    )

  if flask.request.path.startswith('/_s/'):
    return util.jsonify_model_dbs(user_dbs, more_cursor)

  return flask.render_template(
      'user_list.html',
      html_class='user',
      title='User List',
      user_dbs=user_dbs,
      more_url=util.generate_more_url(more_cursor),
    )


################################################################################
# Error Handling
################################################################################
@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(410)
@app.errorhandler(418)
@app.errorhandler(500)
def error_handler(e):
  try:
    e.code
  except:
    class e(object):
      code = 500
      name = 'Internal Server Error'

  if flask.request.path.startswith('/_s/'):
    return flask.jsonify({
        'status': 'error',
        'error_code': e.code,
        'error_name': e.name.lower().replace(' ', '_'),
        'error_message': e.name,
      }), e.code

  return flask.render_template(
      'error.html',
      title='Error %d (%s)!!1' % (e.code, e.name),
      html_class='error-page',
      error=e,
    ), e.code
