from django import template
from textblob import TextBlob
from django.template.defaultfilters import stringfilter
register = template.Library()
from afinn import Afinn
import numpy as np



@register.filter
def sent(tweet):
	y = []
	afinn = Afinn(emoticons=True)
	#for sentence in tweet:
	y = afinn.score(tweet)
	#	y.append(x)

	return str(y)

@register.filter
def all(tweet):
	z = []
	afinn = Afinn(emoticons=True)
	for sentence in tweet:
		m = afinn.score(sentence.text)
		z.append(m)
	y = sum(z) / float(len(z))
	return str(y)