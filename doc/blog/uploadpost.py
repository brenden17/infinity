#! /usr/bin/env python
"""
This script is to upload md formatted file to blog on wordpress.
usage : ./uploadpost -h

Required
 - http://python-wordpress-xmlrpc.readthedocs.org/
 - https://github.com/trentm/python-markdown2
"""

import sys
import argparse as ap
from markdown2 import markdown
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost, EditPost

MAINFILE = '../../../mine.txt'
BIFILE = './blog.ini'
BLOG = 'http://brenden17.wordpress.com/xmlrpc.php'
WPID = 'wordpress-id'
WPPW = 'wordpress-pw'

def get_userinfo():
    with open(MAINFILE) as f:
        doc = f.read().strip()
        sf = lambda line, index:line.split(':')[index].strip()
        userinfo = {sf(line, 0):sf(line, 1) for line in doc.split('\n')}
    return userinfo

def get_postid(filename):
    with open(BIFILE) as f:
        lines = f.readlines()
        for line in lines:
            savedfilename, postid = line.split(',')
            if savedfilename.strip()== filename.strip():
                return postid.strip()
        return None
    return None

def set_postid(filename, postid):
    with open(BIFILE, 'a') as f:
        f.write('{0},{1}\n'.format(filename.strip(), postid))

def readmd(filename):
    with open(filename) as f:
        txt = f.read()
        return txt

def convert_md2html(txt):
    return markdown(txt)

def upload(htmltxt, postid=None, options=None):
    userinfo = get_userinfo()
    username = userinfo.get(WPID, '')
    pw = userinfo.get(WPPW, '')
    doc = htmltxt.split('\n')
    try:
        title = doc[0]
        content = '\n'.join(doc[1:])
        wp = Client(BLOG, username, pw)
        post = WordPressPost()
        post.title = title
        post.content = content
        if options:
            post.terms_names = options
        if not postid:
            postid = wp.call(NewPost(post))
            post.post_status = 'publish'
        wp.call(EditPost(int(postid), post))
        return postid
    except Exception, e:
        print 'Something wrong:' + str(e)

def app(filename, options):
    txt = readmd(filename)
    htmltxt = convert_md2html(txt)
    postid = get_postid(filename)
    newpost = True if not postid else False
    status = 'Creating New Post...' if newpost else 'Updating...{0}'.format(postid)
    print status
    postid = upload(htmltxt, postid, options)
    if newpost:
        set_postid(filename, postid)
    status = 'Created New Post' if newpost else 'Updated {0}'.format(postid)
    print '==== %s  : %s.. ====' % (status, filename)
    print 'http://brenden17.wordpress.com'

def get_args():
    parser = ap.ArgumentParser(description='Uploader for Blog on Wordpress')
    parser.add_argument('filename', action='store',
                        help='uploading file name')
    parser.add_argument('-t', action='store', dest='tags',
                        nargs='+', help='tags')
    parser.add_argument('-c', action='store', dest='cates',
                        nargs='+', help='category')
    args = parser.parse_args()
    return args.filename, {
            'post_tag' : args.tags,
            'category' : args.cates}

if __name__ == '__main__':
    filename, options = get_args()
    app(filename, options)
