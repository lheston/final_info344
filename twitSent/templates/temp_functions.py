from django import template
from textblob import TextBlob
register = template.Library()

#vs = vaderSentiment(sentence)

#register sentiment function
#@register.filter(name='sent')


@register.filter
def sent(tweet):
	y = []
	blob = TextBlob(tweet)
	for sentence in blob.sentences:
		x = sentence.sentiment.polarity
		y.append(x)

	return str(y)