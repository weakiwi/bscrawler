#coding=utf-8
import urllib2
import urllib
import cookielib
import re
import glob
from bs4 import BeautifulSoup

def is_num_by_except(num):
    try:
        int(num)
        return True
    except ValueError:
#        print "%s ValueError" % num
        return False

cookie = cookielib.CookieJar()

handler = urllib2.HTTPCookieProcessor(cookie)

opener = urllib2.build_opener(handler)

loginURL = 'http://www.hi-pda.com/forum/logging.php?action=login'

postdata = {
	'formhash' : '7fb05e5b',
	'referer' : 'index.php',
	'loginfield' : 'username',
	'username' : '你的用户名',
	'password' : '',
	'questionid' : '0',
	'answer' : '',
	'loginsubmit' : 'true',
	'cookietime' : '2592000'}

postdata = urllib.urlencode(postdata)
opener.open(loginURL,postdata)

bsURL = 'http://www.hi-pda.com/forum/forumdisplay.php?fid=6'
response = opener.open(bsURL)
page = BeautifulSoup(response)
tag = page.find_all(href = re.compile('viewthread\.php\?tid=\d*'))
for each_tag in tag:
	if is_num_by_except(each_tag.get_text()) == True:
		continue
	else:
		print each_tag.get_text() 


