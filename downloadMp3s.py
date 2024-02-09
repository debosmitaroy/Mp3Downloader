from pathlib import Path
import youtube_dl
import pandas
import os
import re
import urllib.request
import urllib.parse

def DownloadVideosFromTitles(los):
	ids = []
	for index, item in enumerate(los):
		vid_id = ScrapeVidId(item[0])
		ids += [vid_id]
	print("Downloading songs")
	DownloadVideosFromIds(ids)


def DownloadVideosFromIds(lov):
	SAVE_PATH = str(os.path.join(Path.home(), "Downloads/songs"))
	try:
		os.mkdir(SAVE_PATH)
	except:
		print("download folder exists")
	ydl_opts = {
    	'format': 'bestaudio/best',
   		'postprocessors': [{
        		'key': 'FFmpegExtractAudio',
        		'preferredcodec': 'mp3',
        		'preferredquality': '192',
    		}],
		'outtmpl': SAVE_PATH + '/%(title)s.%(ext)s',
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	    ydl.download(lov)

def ScrapeVidId(query):
	print ("Getting video id for: ", query)
	BASIC="http://www.youtube.com/results?search_query="
	URL = (BASIC + query)
	url= URL.replace(" ", "+")
	html = urllib.request.urlopen(url)
	video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
	return video_ids[0]

def DownloadMp3():
	data = pandas.read_csv('songs.csv')
	data = data.values.tolist()
	print("Found ", len(data), " songs!")
	DownloadVideosFromTitles(data)
	print("---Song Download Finished---")

def __main__():

	data = pandas.read_csv('songs.csv')
	data = data.values.tolist()
	DownloadVideosFromTitles(data)
__main__()