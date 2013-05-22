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
  query.max_results = 1
  query.lr = 'nl'
  query.category = 'Education'
  query.safeSearch = 'strict'
  print query
  feed = yt_service.YouTubeQuery(query)
  PrintVideoFeed(feed)

SearchAndPrint('napoleon')
