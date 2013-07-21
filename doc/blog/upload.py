#! /usr/bin/env python
"""
This script is to upload md formatted file to blog on wordpress.

Required
 - http://python-wordpress-xmlrpc.readthedocs.org/
 - https://github.com/trentm/python-markdown2
"""

import sys
from markdown2 import markdown
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost, EditPost

def get_userinfo():
    filename = '../../../mine.txt'
    with open(filename) as f:
        doc = f.read().strip()
        sf = lambda line, index:line.split(':')[index]
        userinfo = {sf(line, 0):sf(line, 1) for line in doc.split('\n')}
    return userinfo

def readmd(filename):
    with open(filename) as f:
        txt = f.read()
        return txt

def convert_md2html(txt):
    return markdown(txt)

def upload(htmltxt):
    blog = 'http://brenden17.wordpress.com/xmlrpc.php'
    userinfo = get_userinfo()
    username = userinfo.get('wordpress-id', '')
    pw = userinfo.get('wordpress-pw', '')
    doc = htmltxt.split('\n')
    try:
        title = doc[0]
        content = '\n'.join(doc[1:])

        wp = Client(blog, username, pw)
        post = WordPressPost()
        post.title = title
        post.content = content
        post.id = wp.call(NewPost(post))
        post.post_status = 'publish'
        wp.call(EditPost(post.id, post))
    except Exception, e:
        print 'Something wrong:' + str(e)

if __name__ == '__main__':
    filename = sys.argv[1]
    txt = readmd(filename)
    htmltxt = convert_md2html(txt)
    upload(htmltxt)
    print '==== Done ===='
