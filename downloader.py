from requests import get, head, post, packages
from bs4 import BeautifulSoup as soup
packages.urllib3.disable_warnings()



def get_size(content):
	size_in_bytes = len(content)
	size_in_mb = round( size_in_bytes / 1024 / 1024, 2 )
	return size_in_mb

def get_name_from_headers(headers):
        return headers['Content-Disposition'].split(';')[1].replace('filename=', '').replace('"','')

class File:
	def __init__(self, name='',  url='', res=''):
		self.headers = res.headers
		self.name = name.replace(':', '')
		self.url = url
		self.content = res.content
		self.size = get_size(res.content)

		self.info = f'Name: {self.name}\nUrl: {self.url}\nSize: {self.size}'

	def save(self, path=''):
		open( path+self.name, 'wb' ).write(self.content)

	def save_as(self, name, path=''):
		open( name, 'wb' ).write(self.content)



class GoogleDrive:

	def available(vid_id):
		url = f'https://drive.google.com/uc?export=download&id={vid_id}'
		res = get(url).text
		res = soup(res, 'html.parser')
		if res.find( id='uc-download-link' ):
			return True
		else:
			return False
	def download(vid_id):
		url = f'https://drive.google.com/uc?export=download&id={vid_id}'
		res = get(url)

		# Get Cookies (download_warning & NID)
		cookies = res.cookies.get_dict()

		if cookies == {}:
			return File(url = url, name = get_name_from_headers(res.headers), res = res)

		# Get Confirm code from the cookies
		cookies_names = cookies.keys()
		for cookie_name in cookies_names:
			if 'download' in cookie_name:# name ex. download_warning_e456346345
				code = cookies[cookie_name]
				break

		url+= f'&confirm={code}'

		# Download The File 
		#direct_url = head(url, cookies=cookies).headers['Location'] because python does it automaticly ig

		res = get(url, cookies=cookies)
		file_name = get_name_from_headers(res.headers)
		return File(url = url, name = file_name, res = res)


class Mp4upload:

    def get_name_from_url(url):
        return url.split('/')[-1].replace('%20', ' ')
                
    def download(vid_id):
    	url = f'https://www.mp4upload.com/{vid_id}'

    	headers = {'referer':'https://mp4upload.com'}
    	data = {
    		'op': 'download2',
			'id': vid_id,
			'rand': '',
			'referer': 'https://www.mp4upload.com/',
			'method_free':  '',
			'method_premium':''
		}
    	
    	res = post(url, headers=headers, data=data, verify=False)
    	return File(url = url, name= Mp4upload.get_name_from_url(res.url), res = res)


class _4shared:

        def get_name_from_vid_id(vid_id):
                url = 'https://www.4shared.com/video/'+vid_id
                return soup( get(url).text, 'html.parser' ).find('div', {'class':'file-name'}).text\

        def get_vid_url(vid_id):
                url = 'https://www.4shared.com/web/embed/file/'+vid_id
                vid_url = soup( get(url).text, 'html.parser' ).find('source')['src']
                return vid_url

        def download(vid_id):
                url = 'https://www.4shared.com/web/embed/file/'+vid_id
                file_name = _4shared.get_name_from_vid_id(vid_id)
                res = get( _4shared.get_vid_url(vid_id) ) 

                return File(url=url, name=file_name, res=res)

        def available(vid_id):
        	url = 'https://www.4shared.com/video/'+vid_id
        	res = get(url).text
        	if 'The file link that you requested is not valid' in res:
        		return False
        	else:
        		return True

class Mediafire:
        def download(vid_id):
                url = 'https://www.mediafire.com/file/'+vid_id
                direct_url = soup(get(url), 'html.parser').find(id='downloadButton')['href']
                res = get(direct_url)
                file_name = get_name_from_headers(res.headers)

                return File(url = url, name= file_name, res = res)
                
                
        
class blkom:
	def download(url):
		useless_headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-GB,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Host': 'cdn2.vid4up.xyz', 'Pragma': 'no-cache', 'Referer': 'https://www.animeblkom.net/', 'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34'}
		res = get(url, headers=useless_headers)
		file_name = get_name_from_headers(res.headers)

		return File(url = url, name= file_name, res = res)
