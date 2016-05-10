""" 
Matt Levan

Patent analysis on patents related to prediction, data analysis, big data,
artificial intelligence, and machine learning.

Uses Google Search API to collect patents from google.com/patents according
to specific keywords. Returns patents in JSON format.

The format for all all url requests is below: 

#"https://www.googleapis.com/customsearch/v1?
	#	q={searchTerms}
	#	&num={count?}
	#	&start={startIndex?}
	#	&lr={language?}
	#	&safe={safe?}
	#	&cx={cx?}
	#	&cref={cref?}
	#	&sort={sort?}
	#	&filter={filter?}
	#	&gl={gl?}
	#	&cr={cr?}
	#	&googlehost={googleHost?}
	#	&c2coff={disableCnTwTranslation?}
	#	&hq={hq?}
	#	&hl={hl?}
	#	&siteSearch={siteSearch?}
	#	&siteSearchFilter={siteSearchFilter?}
	#	&exactTerms={exactTerms?}
	#	&excludeTerms={excludeTerms?}
	#	&linkSite={linkSite?}&orTerms={orTerms?}&relatedSite={relatedSite?}
	#	&dateRestrict={dateRestrict?}&lowRange={lowRange?}&highRange={highRange?}&searchType={searchType}&fileType={fileType?}&rights={rights?}&imgSize={imgSize?}&imgType={imgType?}&imgColorType={imgColorType?}&imgDominantColor={imgDominantColor?}&alt=json"

"""

import requests
import urllib
import time
import json
import sys

exact_search = ""
date_search = ""
strt = 1

# Check for user args.  If args present, use them all in a search string.
# Format for the command line entry
#	python patent_analysis_multi.py -de y3 "exact_name" rest of search text

# Search command line for special search parameters -d and -e
if(len(sys.argv)>1):
	search_text = ""
	for i in range(0,len(sys.argv)):
		if(not(isinstance(sys.argv[i], (int)))):
			if(sys.argv[i][0] == '-'):
				# Increment the argument start position
				# 1   2    3      4
				# -de date "term" start
				# 1  2  3    4      5
				# -d -e date "term" start
				strt += 1
				for j in range(0,len(sys.argv[i])):
					if(sys.argv[i][j] == 'd'):
						date_search = "&dateRestrict=" + sys.argv[i+j]
						strt += 1
					if(sys.argv[i][j] == 'e'):
						exact_search = "&exactTerms=" + sys.argv[i+j]
						strt += 1
	# Generate the standard query text string
	print("start=" + str(strt))
	for arg in sys.argv[strt+1:len(sys.argv)]:
		if(search_text == ""):
			search_text = str(arg)
		else:
			search_text = str(search_text+"+"+arg)
	end = int(sys.argv[strt])
else:
	print("Enter command line args in the format\n<numberOfPatentMatches tag1 tag2 tag3 etc...>")
	sys.exit()

	
# Get your own access token and custom search engine id (cse_id) from Google.
access_token = "Your Key" 
cse_id = "Your CSE ID"

# Build URL.
# Search parameters.
rf = open("result_files.txt", "a")
num = "10"
num = "10"
for i in range(1, end, 10):
	file_name = str(search_text + str(int(time.time())) + ".txt")
	f = open(file_name, "w")
	start = str(i)
	
	url = "https://www.googleapis.com/customsearch/v1?" + \
		  "key=" + access_token + \
		  "&cx=" + cse_id + \
		  "&hl=en" + \
		  "&start=" + start + \
		  "&filter=1" + \
		  "&num=" + num + \
		  "&tbm=pts" + \
		  "&q=" + search_text + \
		  date_search  + \
		  exact_search
	print(url)
	print(search_text)
	response = requests.get(url)
	response.json()
	# Write the response to a file.
	f.write(json.dumps(response.json(), indent = 4))
	rf.write(str(file_name + '\n'))
	f.close()
