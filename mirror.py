#!/usr/bin/python3

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
fetched = []
abase=''
def isWebPage(path):
    ext=extension = os.path.splitext(path)[1]
    return len(ext)==0 or ext=='.htm' or ext=='.html' or ext=='.php' or ext=='.cgi'
def followLinks(url):
    global fetched
    global abase
    split=urllib.parse.urlparse(url)
    if split.path[-1]=='/':
        if split.query:
            saveTo=split.netloc+split.path+'index.html?'+split.query
        else:
            saveTo=split.netloc+split.path+'index.html'
    else:
        if split.query:
            saveTo=split.netloc+split.path+'?'+split.query
        else:
            saveTo=split.netloc+split.path
    saveTo=urllib.parse.unquote(saveTo,'ascii','ignore')
    if os.path.exists(saveTo):
        pth=''
        if split.path[-1]=='/':
            pth=split.path+'index.html'
        else:
            pth=split.path
        if not isWebPage(pth):
            print('File already exists',saveTo)
            return
    resp = requests.get(url)
    print('Fetched',resp.url,'Save to',saveTo)
    if resp.status_code != 200:
        print('Status code',resp.status_code,'In url',resp.url)
        return
    if not os.path.exists(saveTo):
        if not os.path.exists(os.path.dirname(saveTo)):
            os.makedirs(os.path.dirname(saveTo))
        print('About to write',saveTo)
        with open(saveTo,'wb') as f:
            f.write(resp.content)
        print('Done')
        pth=''
        if split.path[-1]=='/':
            pth=split.path+'index.html'
        else:
            pth=split.path
        if not isWebPage(pth):
            print('Skipping binary file',saveTo)
            return
    else:
        print("The file already exists still following its links",resp.url)
        with open(saveTo,'wb') as f:
            f.write(resp.content)
        print('Done')
    soup = BeautifulSoup(resp.text)
    for link in soup.find_all('a', href=True):
        aburl=urllib.parse.urljoin(resp.url,link['href'])
        print('Before:',link['href'],'After:',aburl)
        if abase not in aburl:
            print('Skipping',aburl)
            continue
        if aburl not in fetched:
            fetched.append(aburl)
            followLinks(aburl)
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import sys
import shutil
import requests
import os
if len(sys.argv)!=2:
    print('Usage '+sys.argv[0]+'Url')
    exit()
abase=sys.argv[1]
split=urllib.parse.urlparse(abase)
print(split.netloc)
if not os.path.exists(split.netloc):
    os.makedirs(split.netloc)
followLinks(abase)
