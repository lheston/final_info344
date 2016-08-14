#from django.shortcuts import render
# Create your views here.
import tweepy
from django.http import *
from django.shortcuts import render_to_response, render
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.template import RequestContext
from twitSent.utils import *
from textblob import TextBlob
import pandas as pd
import json

DataSet = pd.DataFrame

def get_api(request):
	# set up and return a twitter api object
	oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	access_key = request.session['access_key_tw']
	access_secret = request.session['access_secret_tw']
	oauth.set_access_token(access_key, access_secret)
	api = tweepy.API(oauth)
	return api

def main(request):
	"""
	main view of app, either login page or info page
	"""
	# if we haven't authorised yet, direct to login page
	if check_key(request):
		return HttpResponseRedirect(reverse('info'))
	else:
		return render_to_response('twitSent/login.html')
 
def unauth(request):
	"""
	logout and remove all session data
	"""
	if check_key(request):
		api = get_api(request)
		request.session.clear()
		logout(request)
	return HttpResponseRedirect(reverse('main'))

def info(request):
	"""
	Redirect page of after authenticate
	"""


	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(request.session.get('key'), request.session.get('secret'))
	api = tweepy.API(auth)

	# Get username
	
	tweets = tweepy.API(auth)
	user_data = api.user_timeline()
	#for result in user_data:
	#	formated = toDataFrame(result)
	#print(formated)
	# Get timeline
	timeline_list = api.home_timeline()
	username = api.me().name


	

	
	return render(request, 'twitSent/info.html', {'user': user_data, 'userSpecs': username})

def auth(request):

	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	try:
		auth_url = auth.get_authorization_url()
	except tweepy.TweepError:
		raise Exception('Error! Failed to get request token.')
	request.session['request_token'] = auth.request_token
	return HttpResponseRedirect(auth_url)

def callback(request):
	"""
	Callback
	"""
	# Example using callback (web app)
	verifier = request.GET.get('oauth_verifier')

	# Let's say this is a web app, so we need to re-build the auth handler first...
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	token = request.session.get('request_token')
	del request.session['request_token']
	auth.request_token = token

	try:
		auth.get_access_token(verifier)
	except tweepy.TweepError:
		raise Exception('Error! Failed to get access token.')

	request.session['key'] = auth.access_token
	request.session['secret'] = auth.access_token_secret
	return HttpResponseRedirect(reverse('info'))

def check_key(request):
	"""
	Check to see if we already have an access_key stored, if we do then we have already gone through 
	OAuth. If not then we haven't and we probably need to.
	"""
	try:
		access_key = request.session.get('access_key_tw', None)
		if not access_key:
			return False
	except KeyError:
		return False
	return True


def toDataFrame(tweets):

    DataSet = pd.DataFrame()

    
    DataSet['tweetText'] = [tweet.text for tweet in tweets]
    DataSet['tweetID'] = [tweet.id for tweet in tweets]
    DataSet['tweetRetweetCt'] = [tweet.retweet_count for tweet in tweets]
    DataSet['tweetFavoriteCt'] = [tweet.favorite_count for tweet in tweets]
    DataSet['tweetSource'] = [tweet.source for tweet in tweets]
    DataSet['tweetCreated'] = [tweet.created_at for tweet in tweets]
    DataSet['userID'] = [tweet.user.id for tweet in tweets]
    DataSet['userScreen'] = [tweet.user.screen_name for tweet in tweets]
    DataSet['userName'] = [tweet.user.name for tweet in tweets]
    DataSet['userCreateDt'] = [tweet.user.created_at for tweet in tweets]
    DataSet['userDesc'] = [tweet.user.description for tweet in tweets]
    DataSet['userFollowerCt'] = [tweet.user.followers_count for tweet in tweets]
    DataSet['userFriendsCt'] = [tweet.user.friends_count for tweet in tweets]
    DataSet['userLocation'] = [tweet.user.location for tweet in tweets]
    DataSet['userTimezone'] = [tweet.user.time_zone for tweet in tweets]
    #DataSet['lat'] = [tweet.geo.lat for tweet in tweets]

    return DataSet
