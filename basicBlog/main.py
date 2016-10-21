import os
import re

import jinja2
import webapp2
import hmac
import hashlib
import random
import string

from google.appengine.ext import db

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               autoescape=False)

class Handler(webapp2.RequestHandler):
    """ Renders html templates with Jinja2 variables """
    def write(self, *a, **kw):
        """ Writes HTML """
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """ Finds specified template in '/template' of current dir """
        template = JINJA_ENV.get_template(template)
        return template.render(params)

    def render(self, template, **kw):
        """ Render a specific template (param0)
        with any number of vars (params1+) """
        self.write(self.render_str(template, **kw))


class Post(db.Model):
	""" Database entry for a blog post """
	subject = db.StringProperty(required=True)
	content = db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)

# class User(db.Model):
# 	""" Database entry for a user """
# 	username = db.StringProperty(required=True)
# 	password = db.StringProperty(required=True)
# 	email = db.StringProperty()
# 	created = db.DateTimeProperty(auto_now_add=True)

class Blog(Handler):
	""" Defualt HTTP Request Handler """

	def display_posts(self):
		""" Display 10 most recent blog posts """
		posts = db.GqlQuery("SELECT * FROM Post"
							"ORDER BY created DESC")
		self.render("blog.html", posts=posts)

	def get(self):
		""" Handle GET request """
		self.display_posts()

class NewPost(Handler):
	""" Handler for creating new blog posts """
	def blog_creation(self,subject="", content="", error=""):
		""" Renders blog post creation screen, preserving user input """

		self.render("newpost.html", subject=subject,
					content=content, error=error)

	def post(self):
		""" Gathers blog post data and, if valid, writes to database """
		subject = self.request.get("subject")
		content = self.request.get("content")

		if subject and content:
			new_post = Post(subject=subject, content=content)
			new_post.put()

			self.redirect("/post/%s" % new_post.key().id())
		else:
			error = "Error: Subject and content are both required"
			self.blog_creation(subject, content, error)

	def get(self):
		self.blog_creation()

class BlogPost(Handler):
	""" Displays a single post at a permenant URL """

	def get(self, post_id):
		""" Queries database for post id and renders it """
		post_id = int(post_id)
		post = Post.get_by_id(post_id)

		self.render("post.html", post=post)

class Welcome(Handler):
	""" Render welcome screen """
	def get(self):
		message = ""

		message = "Welcome!"
		self.render('welcome.html', message=message)

		return

	self.redirect('/signup')


app = webapp2.WSGIApplication([('/', Blog),
                               ('/newpost', NewPost),
                               (r'/post/(\d+)', BlogPost),
                               ('/welcome', Welcome),
                              ],
                              debug=True
                             )




















