#from django.shortcuts import render
# Create your views here.
import tweepy
from django.http import *
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.template import RequestContext
from twitSent.utils import *
from textblob import TextBlob
import pandas as pd
import json
from afinn import Afinn
from .models import Post, blacklist
from .forms import PostForm
from django.db import transaction
from ratelimit.decorators import ratelimit
from rest_framework.decorators import api_view
from twitSent.serializers import UrlsSerializer
from rest_framework.response import Response



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

	test = pd.DataFrame
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(request.session.get('key'), request.session.get('secret'))
	api = tweepy.API(auth)

	tweets = tweepy.API(auth)
	user_data = api.user_timeline()
	#get page data
	timeline_list = api.home_timeline()
	#get username
	username = api.me().name
	#form = PostForm()
	#if form.is_valid():
	#	post = form.save(commit=False)
	list1 = blacklist.objects.values_list('tweetContent', flat=True).distinct
	for tweet in user_data:
		p, post = Post.objects.get_or_create(tweetContent=tweet.text, name= username, sent=tweet.text)
		#p = p.objects.exclude(blacklist=blacklist.tweetContent)
		#p.objects.filter(time__gte=datetime.now()).exclude(id__in=list1)
		p.save()

	#list1 = blacklist.objects.values_list('tweetContent')
	url = Post.objects.all()
	return render(request, 'twitSent/info.html', {'user': list1, 'userSpecs': username,'userData': url})

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

def delete(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post = Post.objects.filter(pk=pk).update(bad=2)
	#post.save();
	#post = post.delete()
	return HttpResponseRedirect(reverse('info'))

def post_new(request):
	if request.method == "POST":
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(request.session.get('key'), request.session.get('secret'))
		api = tweepy.API(auth)

		tweets = tweepy.API(auth)
		#get username
		username = api.me().name
		
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.tweetContent = request.POST['tweetContent']
			post.name = username
			post.sent = sent(request.POST['tweetContent'])
			post.save()
			return redirect('info')
	else:
		form = PostForm()
	return render(request, 'twitSent/post_new.html', {'form': form})

def sent(tweet):
	y = []
	afinn = Afinn(emoticons=True)
	#for sentence in tweet:
	y = afinn.score(tweet)
	#	y.append(x)

	return str(y)


@ratelimit(key='ip', rate='10/m', block=True)
@api_view(['GET', 'POST'])
def url_list(request, format=None):
	"""
	Lists all urls, or create a url.
	"""
	if request.method =='GET':
		urlsdata = Post.objects.all()
		serializer = UrlsSerializer(urlsdata, many=True)
		return Response(serializer.data)
	elif request.method == 'POST':
		serializer = UrlsSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 




@ratelimit(key='ip', rate='10/m', block=True)
@api_view(['GET', 'PUT', 'DELETE'])
def url_detail(request, pk, format=None):
	"""
	Retrive, update or delete a book
	"""
	try:
		 users = Post.objects.get(pk=pk)
	except Post.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = UrlsSerializer(users)
		return Response(serializer.data)
	elif request.method == 'PUT':
		serializer = UrlsSerializer(user, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.tatus.HTTP_400_BAD_REQUEST)
	elif request.method == 'DELETE':
		user.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
