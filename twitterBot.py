import urllib
import urllib2
import simplejson as json
import time

user = 'username' # here goes the username
password = 'password' # here goes the password
q = '#search' # the search query
since_id = 0
replied = []
users = []

updateUrl = 'http://api.twitter.com/1/statuses/update.json';

auth_handler = urllib2.HTTPBasicAuthHandler()
auth_handler.add_password("Twitter API",updateUrl,user,password)
opener = urllib2.build_opener(auth_handler)
urllib2.install_opener(opener)

while (True):
	searchUrl = "http://search.twitter.com/search.json?%s" % urllib.urlencode({'q':q,'since_id':since_id})
	results = json.loads(urllib.urlopen(searchUrl).read())['results']
	for t in results:
		# you can play here and change those rules, it is optimized not to reach the daily limit of 1000 posts
		if (t['from_user'] != user and t['from_user'] not in users):
			status = 'RT @%s %s' % (t['from_user'],t['text'])
			params = urllib.urlencode({'status':status,'in_reply_to_status_id':t['id']})
			try:
				urllib2.urlopen(updateUrl, params).read()
				print status
				since_id = t['id']
				replied.append(t['id'])
				users.append(t['from_user'])
			except urllib2.HTTPError:
				print "HTTPError "
			time.sleep(90)
			break
