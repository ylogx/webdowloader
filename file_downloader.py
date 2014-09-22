#!/usr/bin/env python3
#
#  file_downloader.py - download the file passed as the first argument, can be easily used as a module for your program
#
#  Copyright (c) 2014 Shubham Chaudhary <me@shubhamchaudhary.in>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import ( division, absolute_import, print_function, unicode_literals )
import sys, os, time, tempfile, logging

if sys.version_info >= (3,):
    import urllib.request as urllib2
    import urllib.parse as urlparse
else:
    import urllib2
    import urlparse


def download(url,destination='./',desc=None):
    ''' download the file passed and
    show detailed description while downloading'''
    try:
        u = urllib2.urlopen(url)
    except ValueError:
        print(url);
        print('Url value error');
        return
    except:
        raise

    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    filename = os.path.basename(path)
    if not filename:
        filename = 'downloaded.file'
    if desc:
        filename = os.path.join(desc, filename)
    if os.path.isdir(destination):
        filename = os.path.join(destination, filename);
    if os.path.exists(filename):
        #FIXME: adding suffix if file exists
#         filename += time.strftime("%y%m%d-%H%M%S.txt");
        print('File {0} exists'.format(filename));

    with open(filename, 'wb') as f:
        meta = u.info()
        meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
        meta_length = meta_func("Content-Length")
        file_size = None
        if meta_length:
            file_size = int(meta_length[0])
        print("Downloading: {0} Bytes: {1}".format(url, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)

            status = "{0:16}".format(file_size_dl)
            if file_size:
                status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
            status += chr(13)
            print(status,)
        print()
    print('Saved: ',filename);
    # return filename

def download_2(url):
    ''' 2nd implementation '''
    urllib.urlretrieve(url,url.split('/')[-1]);
    file_name = url.split('/')[-1]
    response = urllib.urlopen(url);
    file_read = response.read();

def download_3(url):
    ''' 3rd implementation '''
    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print("Downloading: %s Bytes: %s" % (file_name, file_size))

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print(status,)

    f.close()

def download_list(url_list,destination='./',desc=None):
    count = len(url_list)
    for url in url_list:
        print("{0} files left".format(count));
        download(url,destination,desc);
        count -= 1

def main(argv):
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-r", "--rename", dest="rename",
                     help="Name the downloaded file RENAME", metavar="RENAME")
    (options, args) = parser.parse_args()
    if args:
        if len(args) == 1 and options.rename:
            #TODO: Rename interface?
            download(args[0])
        else:
            download_list(args);

if __name__ == '__main__':
    try:
        main(sys.argv);
    except KeyboardInterrupt:
        print('\nGracefully exiting, but that is not fair. ',
              'I was trying to get it for you :(');
    except:
        raise
