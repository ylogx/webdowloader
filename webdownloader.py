#!/usr/bin/env python3
#
#  Copyright (c) 2014 Shubham Chaudhary <me@shubhamchaudhary.in>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

''' webdownloader.py - download all data with specific extensions linked
    in any html page, useful for course websites like ocw.mit.org etc. '''

import sys
#import os
#import re

if sys.version_info >= (3,):
    import urllib.request as urllib2
    import urllib.parse as urlparse
else:
    import urllib2
    import urlparse

try:
    from bs4 import BeautifulSoup
except ImportError:
    print('Please install dependency:')
    if sys.version_info >= (3,):
        print('sudo apt-get install python3-bs4')
    else:
        print('sudo apt-get install python-beautifulsoup')
    sys.exit(1)

DEFAULT_DOWNLOAD_TYPE = 'jpg'
DEFAULT_DESTINATION_FOLDER = './'
IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif']
DOCUMENT_EXTENSIONS = ['pdf', 'doc', 'docx']
AUDIO_EXTENSIONS = ['mp3']
VIDEO_EXTENSIONS = ['mp4', 'webm', '3gp', 'mov', 'mkv']

try:
    from filedownloader.file_downloader import download, download_list
except ImportError:
    print('Dependency Problem:')
    print('Download file_downloader.py in the same folder')
    print('Type: `wget https://raw.githubusercontent.com/shubhamchaudhary/filedownloader/master/file_downloader.py`')
    sys.exit(1)

def get_href(url):
    ''' return urllist of all href tags '''
    urllist = []
    html_page = urllib2.urlopen(url)
    soup = BeautifulSoup(html_page)
    for link in soup.findAll('a'):
        address = link.get('href')
        urllist.append(address)
    return urllist

def parse(url, extension=None, destination=None):
    ''' Parse the given url for extension and store them at destination '''
    assert isinstance(url, str)
    if extension == None:
        extension = DEFAULT_DOWNLOAD_TYPE
    if destination == None:
        destination = DEFAULT_DESTINATION_FOLDER

    urllist = []
    href_list = get_href(url)
    for address in href_list:
        if not address:
            continue      #If address in NoneType
        if (address[-len(extension):] == extension
                or address[-4:] == 'jpeg'
                or address[-3:] == 'png'):
            print('Found ', extension, ': ', address)
            urllist.append(urlparse.urljoin(url, address))
    print('Total', len(urllist), 'files found with extension:', extension)
    download_list(urllist, destination)

def parse_filetype(url, filetype, destination):
    ''' Parse files with specific filetype
    e.g webdownloader -t image -d new_folder http://url.com/page '''
    filetype = filetype.lower()
    if (filetype == 'i'
            or filetype == 'image'
            or filetype == 'images'
            or filetype == 'img'):
        EXTENSIONS = IMAGE_EXTENSIONS
    elif (filetype == 'd'
            or filetype == 'doc'
            or filetype == 'pdf'):
        EXTENSIONS = DOCUMENT_EXTENSIONS
    elif (filetype == 'v'
            or filetype == 'video'
            or filetype == 'videos'
            or filetype == 'movie'
            or filetype == 'movies'):
        EXTENSIONS = VIDEO_EXTENSIONS
    elif (filetype == 'a'
            or filetype == 'audio'
            or filetype == 'sound'):
        EXTENSIONS = AUDIO_EXTENSIONS
    for extension in EXTENSIONS:
        print('Downloading {0} filetype:'.format(extension))
        parse(url, extension, destination)

def main(argv):
    ''' The main function '''
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-e", "--extension", dest="extension",
                     help="Download files with this extension .EXT",
                     metavar="EXT")
    parser.add_option("-d", "--destination", dest="destination",
                     help="destination FOLDER where files will be saved",
                     metavar="FOLDER")
    parser.add_option("-f", "--file", dest="filename",
                     help="parse a downloaded html FILE", metavar="FILE")
    parser.add_option("-t", "--type", dest="filetype",
                     help="Download files of this filetype: e.g image, videos,\
                             doc")
    parser.add_option("-q", "--quiet",
                     action="store_false", dest="verbose", default=True,
                     help="don't print status messages to stdout")

    (options, args) = parser.parse_args()

    if args:    #args[0] is the url
        if options.filetype:
            parse_filetype(args[0], options.filetype, options.destination)
        else:
            for anurl in args:
                print('Parsing: ', anurl)
                try:
                    parse(anurl, options.extension, options.destination)
                except:
                    #print('Error encountered with this page.  Details:',
                            #file=sys.stderr)
                    #print(sys.exc_info()[1], file=sys.stderr)
                    continue
    else:
        parser.print_help()

    return  #end main


if __name__ == '__main__':
    try:
        main(sys.argv)
    except ValueError:
        print(sys.exc_info()[1])
    except KeyboardInterrupt:
        print('\nGracefully exiting, but that is not fair. \
                I was trying to get it for you :(')
