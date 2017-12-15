# 1. Importing all necessary programs in order to run my code
import json
import requests
import webbrowser
import unittest
import csv
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
from your_app_data import APP_ID, APP_SECRET
from collections import Counter

# 2. Facebook request function
# Global facebook_session variable, needed for handling FB access below
facebook_session = False

# Function to make a request to Facebook provided.
# Reference: https://requests-oauthlib.readthedocs.io/en/latest/examples/facebook.html
def makeFacebookRequest(baseURL, params = {}):
    global facebook_session
    if not facebook_session:
        # OAuth endpoints given in the Facebook API documentation
        authorization_base_url = 'https://www.facebook.com/dialog/oauth'
        token_url = 'https://graph.facebook.com/oauth/access_token'
        redirect_uri = 'https://www.programsinformationpeople.org/runestone/oauth'

        scope = ['user_posts','pages_messaging','user_managed_groups','user_status','user_likes']
        facebook = OAuth2Session(APP_ID, redirect_uri=redirect_uri, scope=scope)
        facebook_session = facebook_compliance_fix(facebook)

        authorization_url, state = facebook_session.authorization_url(authorization_base_url)
        print('Opening browser to {} for authorization'.format(authorization_url))
        webbrowser.open(authorization_url)

        redirect_response = input('Paste the full redirect URL here: ')
        facebook_session.fetch_token(token_url, client_secret=APP_SECRET, authorization_response=redirect_response.strip())

    return facebook_session.get(baseURL, params=params)


## this makes the request to the API and turns it into a Python dictionary - tells FB to give access to 'humansofny'
baseurl = 'https://graph.facebook.com/humansofny/feed'
params_50 = {}
params_50['fields'] = 'message'
params_50['limit'] = 50
fb_req = makeFacebookRequest(baseurl, params_50)
fifty_posts_data = json.loads(fb_req.text)

with open("facebook_request.json", 'w', encoding='utf-8') as f:
    dumping = json.dumps(fifty_posts_data, indent=4, sort_keys = True)
    f.write(dumping)
    f.close()

class Post(): #class Post will get the message data from the post
    def __init__(self, fb_dict):
        self.message = fb_dict.get('message')

        def __str__(self):
            return "This is the information for each post in the feed: {}".format(self.message)

# post_list will find all the stopwords in the message data from class Post and remove them and separate them into a different list 
def post_list(list_inst):
    stopwordslist = []
    with open('stopwords.txt', 'r') as f:
        for line in f:
            line = line.strip('\n')
            stopwordslist.append(line)

    total_message = ''
    for each in list_inst:
        total_message = total_message + '' + str(each.message)

    l_message= str(total_message).lower().replace(';', '').replace('"', '').replace('“', '').replace(',', '')
    splitmes = l_message.split()
    final = []
    for each in splitmes:
        if 'http' not in each:
            final.append(each)
    final2 = []
    for each in final:
        if '#' not in each:
            final2.append(each)

    message2 = []

    for each in final2:
        if each not in stopwordslist:
            message2.append(each)


    ### this code finds the most common word 
    from collections import Counter
    words = Counter()
    words.update(message2)

    new = words.most_common(1)
    common = new[0][0]
    return common

# this will create a new list with all of the posts from class Post
post_insts = []
for post in fifty_posts_data['data']:
    obj = Post(post)
    post_insts.append(obj)

most_common = post_list(post_insts)
print(most_common)



# 1. Call on iTunes data from API or cache

CACHE_FILE = 'iTunes_API_cache.json'
CACHE = None
song_dict = {}

def loading_cache_from_file():
	global CACHE 
	try:
		f = open(CACHE_FILE, 'r')
		CACHE = json.loads(f.read())
		f.close()
		print('Loaded cache from', CACHE_FILE)
	except:
		# if cache file does not exist, initialize empty cache
		CACHE = {}
		save_cache_to_file()

def save_cache_to_file():
	if CACHE is not None:
		f = open(CACHE_FILE, 'w')
		f.write(json.dumps(CACHE, indent=4, sort_keys = True))
		f.close()
		print('Saved cache to', CACHE_FILE)

def construct_cache_key(name, mtype):
	return '#'.join(name.split()) + '_' + mtype


#### request to the iTunes API #########

# 2. Search the iTunes cache using the most common word from most_common - this is above with the Facebook code 

def get_from_iTunes(name, mtype='song'):
    request_key = construct_cache_key(name, mtype)
    if request_key in CACHE:
    	final_list = []
    	for item in CACHE[request_key]['results']:
    		temp = {}
    		temp['trackName'] = item['trackName']
    		temp['artistName'] = item['artistName']
    		temp['trackTimeMillis'] = item['trackTimeMillis']
    		temp['collectionName'] = item['collectionName']
    		final_list.append(temp) #this will return the final list from the cache that was read
    	return final_list
    else:
        baseurl = 'https://itunes.apple.com/search' # this happens if the cache file is empty
        parameters = {}
        parameters['term'] = name
        parameters['entity'] = mtype
        print('Making request to the iTunes API')
        response = requests.get(baseurl, params = parameters)
        python_obj = json.loads(response.text)
        final_list = []
        for item in python_obj['results']:
            temp = {}
            temp['trackName'] = item['trackName']
            temp['artistName'] = item['artistName']
            temp['trackTimeMillis'] = item['trackTimeMillis']
            temp['collectionName'] = item['collectionName']
            final_list.append(temp)
        print(len(final_list))
        # Cache this response and save the cache to file
        CACHE[request_key] = python_obj  
        save_cache_to_file()
        return final_list

loading_cache_from_file() #if a cache file exists it will read it into memory
result = get_from_iTunes(most_common)


# 3. Define a class Song():
class Song():
	def __init__(self, song_lst):
		self.title = song_lst['trackName']
		self.length = mil_to_min(song_lst['trackTimeMillis'])  #find tags to add here for the length of the song
		self.artist = song_lst['artistName']
		self.album_name = song_lst['collectionName']

	def __str__(self):
		return '{} by {} in {} is {} minutes long.'.format(self.title, self.artist, self.album_name, self.length) #look at this again, is this the right code?

def mil_to_min(mil):
	Militime = int(mil)
	seconds = (Militime/1000)%60
	seconds = int(seconds)
	minutes = (Militime/(1000*60))%60
	minutes = int(minutes)
	hours = (Militime/(1000*60*60))%24
	hours = int(hours)
	return "{}:{}".format(minutes, seconds)


song_list_instance = []

def song_lst():
	for each in result:
		song = Song(each)
		song_list_instance.append(song)

song_lst()

songz = sorted(song_list_instance, key=lambda song: song.length, reverse=True)

masterlist = []
names = ['Song Title', 'Song Album', 'Song Artist', 'Song Length']
masterlist.append(names)
for songs in songz:
	temp = [songs.title, songs.album_name, songs.artist, songs.length]
	masterlist.append(temp)

with open('iTunesSongs.csv', 'w', newline="") as f:
	writer = csv.writer(f)
	writer.writerows(masterlist)

