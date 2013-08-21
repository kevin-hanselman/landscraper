#! /usr/bin/python3
'''Bringing you scenic desktop wallpapers courtesy of Reddit and its users.'''

'''
   Copyright 2013 Kevin Hanselman

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
'''

import os
import re
import sys
import json
import argparse
from urllib import request 
import urllib.parse

ver = '1.0'

def main():
	parser = init_argparser()
	args = parser.parse_args()
	#print(args)

	if args.dir:
		if os.path.isfile(args.dir):
			sys.exit('Path exists and is not a directory')
		if not os.path.isdir(args.dir):
			try:
				os.makedirs(args.dir)
			except Exception as ex:
				sys.exit(str(ex));
		os.chdir(args.dir)	
		
	base = 'http://www.reddit.com/r/EarthPorn'
	querystr = ''
	if args.params:
		querystr = '?' + '&'.join(args.params)
	url = os.path.join(base, args.listing + '.json') + querystr
	print('HTTP GET: %r' % url)
	
	urlo = RedditOpener()
	jdict = urlo.get_json(url)
	#print(json.dumps(jdict, sort_keys=True, indent=2, separators=(',', ': ')))
	
	try:
		data = [d['data'] for d in jdict['data']['children']]
	except Exception as ex:
		sys.exit(str(ex))
		
	regex = r'(\d+)\s*x\s*(\d+)'
	for entry in data:
		title = entry['title']
		url = entry['url']
		print('-' * 80)
		print(title)
		m = re.search(regex, title)
		if m:
			res = tuple(int(x) for x in m.group(1, 2))
			ratio = float(res[0]) / res[1]
			print('Alleged resolution: %sx%s\tRatio: %.2f' % (res[0], res[1], ratio))
		else:
			print('No matching resolution. Skipping.')
			continue
		
		if not (res[0] >= args.width and abs(ratio - args.ratio) < args.tol):
			print('Does not meet image specs. Skipping.')
			continue
		else:
			ext = os.path.splitext(url)[1]
			if not ext:
				print('URL %r is not a file. Skipping.' % url)
				continue
			friendly_title = re.sub(r'\W+', '_', title)[:50] + ext
			dlm = DownloadManager(url, urlo, friendly_title)
			dlm.download()
		print('-'*80)

class HTTPError(Exception):
	pass

class RedditOpener(request.FancyURLopener):
	version = 'User-Agent: landscraper/' + ver
	
	def http_error_default(self, url, fp, errorcode, errmsg, headers):
		if errorcode >= 400:
			raise HTTPError(str(errorcode) + ': ' + errmsg)
		else:
			request.FancyURLopener.http_error_default(self, url, fp, errorcode, errmsg, headers)
			
	def get_json(self, url):
		resp = self.open(url)
		encoding = resp.headers.get_content_charset()
		return json.loads(resp.read().decode(encoding))

class DownloadManager:
	def __init__(self, url, urlo, filename=None):
		self.url = url
		self.urlo = urlo
		if filename:
			self.filename = filename
		else:
			self.filename = os.path.basename(url)
		
	def download(self):
		if os.path.exists(self.filename):
			print('File %r exists locally.' % self.filename)
			return
		try:
			print('Downloading: %r' % self.url)
			self.urlo.retrieve(self.url, self.filename, reporthook=self.rhook)
			print()
		except HTTPError as ex:
			request.urlcleanup()
			sys.exit(ex)
		except URLError as ex:
			request.urlcleanup()
			sys.exit(ex)
		request.urlcleanup()
	
	def rhook(self, blocks_read, block_size, total_size):
		amount_read = blocks_read * block_size
		if total_size > 0:
			sys.stdout.write('\r[%2d%% of %s]'
							% (amount_read/total_size*100, sizeof_fmt(total_size)))
		else: # unknown size
			sys.stdout.write('\r[Downloading: %s]' % (sizeof_fmt(amount_read)))
		sys.stdout.flush()       
	
def sizeof_fmt(num):
	for x in [' bytes','KB','MB','GB']:
		if num < 1024.0:
			return "%4.2f%s" % (num, x)
		num /= 1024.0
		
def init_argparser():
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-v','--version', action='version', version='%(prog)s ' + ver)
	parser.add_argument('-d', '--dir', default='images', help='output directory for images')
	parser.add_argument('-a', type=float, default=1.6, metavar='RATIO', dest='ratio', help='aspect ratio as decimal (e.g. 1.6)')
	parser.add_argument('-t', '--tol', type=float, default=0.2, help='aspect ratio absolute tolerance (e.g. 0.2)')
	parser.add_argument('-w', type=int, default=0, metavar='WIDTH', dest='width', help='minimum resolution width as integer (e.g. 1024)')
	parser.add_argument('-l', '--listing', choices=('top','hot','new','random'), default='top', help='listing to get from Reddit')
	parser.add_argument('-p', '--params', nargs='*', help='query parameters for the Reddit API (e.g. limit=10)')
	return parser

if __name__=='__main__':
	main()
