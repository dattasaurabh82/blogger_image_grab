# Alexander Attar - Summer 2013

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
import random
from os.path import expanduser

import urllib2
import urlparse
from urllib import urlretrieve
from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup as bs


def main(url):
    """
    blogger_image_grab.py
        Downloads all the images on the supplied Blogger blog, and saves them to the
        Downloads directory

    Usage:
        python blogger_image_grab.py http://example.com
    """

    # send the request with a random user agent in the header
    request = urllib2.Request(url, None, randomize_user_agent())
    html = urllib2.urlopen(request)
    soup = bs(html)
    parsed = list(urlparse.urlparse(url))
    download_images(soup, parsed)

    older_posts = soup.find(text='Older Posts')
    while older_posts:
        print 'Navigating to the next page: %s' % older_posts.previous['href']
        soup = bs(urlopen(older_posts.previous['href']))
        parsed = list(urlparse.urlparse(url))
        download_images(soup, parsed)
        older_posts = soup.find(text='Older Posts')
        if not older_posts:
            print 'Downloading complete!'


def _usage():
    print 'usage: python blogger_image_grab.py http://example.com'


def randomize_user_agent():

    user_agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',
        'Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))',
        'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.2; SV1; .NET CLR 3.3.69573; WOW64; en-US)'
    ]

    return {'User-Agent': random.choice(user_agents)}


def download_images(soup, parsed):

    home = expanduser("~")  # setup a path to the OSX ~/ directory
    download_directory = home + '/Downloads/'

    for image in soup.findAll('img'):

        try:  # to save the image
            print 'Image: %(src)s' % image
            filename = image['src'].split('/')[-1]
            parsed[2] = image['src']
            file_location = download_directory + filename

            if image['src'].lower().startswith('http'):
                urlretrieve(image['src'], file_location)
            else:
                urlretrieve(urlparse.urlunparse(parsed), file_location)
        except Exception as e:
            print 'Unable to save image: %s' % str(e)

if __name__ == '__main__':
    url = sys.argv[-1]
    if not url.lower().startswith('http'):
            _usage()
            sys.exit(-1)
    main(url)
