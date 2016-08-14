#from django.shortcuts import render
# Create your views here.
import tweepy
from django.http import *
from django.shortcuts import render_to_response, render
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.template import RequestContext
from twitSent.utils import *


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
	username = auth.get_username()

	# Get timeline
	timeline_list = api.home_timeline()

	
	return render(request, 'twitSent/info.html', {'user': username})

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
