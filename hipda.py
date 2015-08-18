#coding=utf-8
import urllib2
import urllib
import cookielib
import re
import jieba.analyse
from multiprocessing import Pool
from bs4 import BeautifulSoup

def is_num_by_except(num):
    try:
        int(num)
        return True
    except ValueError:
#        print "%s ValueError" % num
        return False

def hianalyse(num):
	cookie = cookielib.CookieJar()
	handler = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(handler)

	loginURL = 'http://www.hi-pda.com/forum/logging.php?action=login'

	postdata = {
		'formhash' : '7fb05e5b',
		'referer' : 'index.php',
		'loginfield' : 'username',
		'username' : '用户名哦',
		'password' : '密码哦',
		'questionid' : '0',
		'answer' : '',
		'loginsubmit' : 'true',
		'cookietime' : '2592000'}

	postdata = urllib.urlencode(postdata)
	opener.open(loginURL,postdata)


	msg = ''
	for page_num in range(num*100-99, num*100):
		bsURL = 'http://www.hi-pda.com/forum/forumdisplay.php?fid=2&page='+str(page_num)
		response = opener.open(bsURL)
		page = BeautifulSoup(response)
		tag = page.find_all(href = re.compile('viewthread\.php\?tid=\d*'))
	for each_tag in tag:
		if is_num_by_except(each_tag.get_text()) == True:
			continue
		else:
			each_tag = each_tag.get_text().encode('utf-8')
			msg = msg + each_tag
	print 'task '+str(num)+' done!!!' 
	f = open('temp.txt','a+')
	f.write(msg)
	f.close()

if __name__ == '__main__':
	p = Pool()
	for i in range(10):
		p.apply_async(hianalyse,args=(i,))
	p.close()
	p.join()
