import sys
#sys.path.append('gdata-2.0.17/src/')
import gdata.youtube
import gdata.youtube.service
import json
import pprint

def PrintEntryDetails(entry):
  print entry.media.title.text
  print entry.media.description.text
  print entry.media.thumbnail[0].url
  print entry.media.thumbnail[0].url[24:33]

def PrintVideoFeed(feed):
  for entry in feed.entry:
    PrintEntryDetails(entry)

def SearchAndPrint(search_terms):
  yt_service = gdata.youtube.service.YouTubeService()
  query = gdata.youtube.service.YouTubeVideoQuery()
  query.vq = search_terms
  query.orderby = 'relevance'
  query.max_results = 5 
  query.lr = 'nl'
  query.category = 'Education'
  query.safeSearch = 'strict'
  print query
  feed = yt_service.YouTubeQuery(query)
  PrintVideoFeed(feed)

SearchAndPrint('oppervlakte driehoek')

def search_youtube(search_term):
  yt_service = gdata.youtube.service.YouTubeService()
  query = gdata.youtube.service.YouTubeVideoQuery()
  query.vq = search_term.encode('UTF-8') 
  query.orderby = 'relevance'
  query.max_results = 5
  query.lr = 'nl'
  query.category = 'Education'
  query.categories.append('Education')
  query.safeSearch = 'strict'
  feed = yt_service.YouTubeQuery(query)
  return feed

feed = search_youtube('napoleon')
