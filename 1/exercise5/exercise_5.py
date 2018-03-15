from twython import Twython, TwythonError
import gmplot

APP_KEY = '7slYxZOiz6SCnLudupuvF6d4g'
APP_SECRET = 'esGzNewoflwJex8sXZcPYfQJJPmTqJuoZ3QpHDOqPUH92TY7vm'

twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)

ACCESS_TOKEN = twitter.obtain_access_token()


twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

results = twitter.search(geocode ='41.9027835,12.496365500000024,7mi')

all_tweets = results['statuses']

all_data = []
for tweet in all_tweets:
    data = []
    if tweet['geo']:
        print(tweet)
        data.append(tweet['text'])
        data.append(tweet['user']['screen_name'])
        data.append(tweet['geo']['coordinates'])
        all_data.append(data)

text = []
ltd = []
lgs = []

for data in all_data:
    ltd.append(data[2][0])
    lgs.append(data[2][1])
    if len(all_data) == 1:
        text.append('@'+str(data[1])+': '+str(data[0]))
        text.append('@'+str(data[1])+': '+str(data[0]))
    else:
        text.append('@'+str(data[1])+': '+str(data[0]))

print(ltd)
print(lgs)

ltd = [41.9,41.7909300]
lgs = [12.5,12.2366200]
text = ['@SAIDdal1923: Il  pranzetto  di oggi martedì 10 Ottobre. lunch at said roma SAID dal 1923 rome head house and… https://t.co/dvD70Vm1wt', '@SAIDdal1923: I\'m at Gate C4 in Fiumicino, Lazio w/ @lachlanj @japh @pwcc https://t.co/h1mv4sCQN3']

gmap = gmplot.GoogleMapPlotter(41.9027835,12.496365500000024,11)
gmap.scatter(ltd, lgs, '#3B0B39', size=40, marker=True)
gmap.scatter(ltd, lgs, 'k', marker=True)
gmap.draw("mymap.html", text)