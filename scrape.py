
#install dependencies with: pip install requests bs4

from bs4 import BeautifulSoup as bs
import requests

URL = 'myURL'
#URL to any playlist with under 100 elements

data = requests.get(URL).text
data_lowered = data.lower() 
#Available title names are in a simpleText attribute and deleted videos are in a text attribute.
#Easiest to just lower the data and search for text so a deleted video or available video title will be found regardless

soup = bs(data, 'html.parser')

playlistTitle = soup.find('title').get_text()

playlistTitle = playlistTitle[0:-10] #remove '- Youtube' from the title of the playlist

sizePhrase = '"stats":[{"runs":[{"text":"'
#the size of the playlist is located after the text attribute
begin = data.find(sizePhrase) + len(sizePhrase)
finish = data.find('videos', begin) - 1
#the text attribute has the phrase 'num videos' so save position before 'videos'

playlistLen = int(data[begin:finish])
print(playlistLen)

startingPoint = '"playlistVideoListRenderer"'
#the list of title names is right after this element

mainPhrase = '"title":'
#the name of the video is close to this attribute

subPhrase = 'text":"'
#the actual video name follows this attribute

titles = []
i = data.find(startingPoint)
for x in range(0, playlistLen):
    i = data.find(mainPhrase, i) #mark start point as position of the mainPhrase
    endPoint = data.find('"index"', i) #look for index attribute, starting at i, since it is after the video name
    start = data_lowered.find(subPhrase, i, endPoint) + len(subPhrase) #save position of video name starting at i and ending at 'endPoint'
    end = (data.find('"}', start))
    i = end
    titles.append(data[start:end]) #add title to array

output = ""
for title in titles:
   output += title + "\n"

dest = "Playlists/" + playlistTitle + ".txt"
#put in Playlists folder with playlistName as its filename
f = open(dest, "w", encoding='utf8')
f.write(output)

