import os
import webapp2
import urllib2
from xml.dom import minidom
import jinja2
from google.appengine.ext import db
from google.appengine.api import memcache
import logging

jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

def top_arts(update = False):
	key = "top"
	arts = memcache.get(key)
	if arts is None or update:
		logging.error("DB QUERY")
		# get art from db
		arts = db.GqlQuery("SELECT * FROM Art " " ORDER BY created DESC " "LIMIT 10")
		arts = list(arts)
		memcache.set(key,arts)
	return arts


class Handler(webapp2.RequestHandler):
	def write(self,*a,**kw):
		self.response.out.write(*a,**kw)

	def render_str(self, template, **params):
		t = jinja_environment.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainPage(Handler):
	def render_front(self,title="",art="",error=""):
		arts = top_arts()

		self.render(title=title, art=art,error=error,arts=arts)

	def get(self):
		self.write(repr(self.request.remote_addr))
		self.render_front()

	def post(self):
		title = self.request.get('title')
		art = self.request.get('art')

		if title and art:
			a = Art(title=title, art=art)

			a.put()
			memcache.flush_all()

			self.redirect('/')

		else:
			error = "We need both a title and some artwork!"
			self.render_front(title,art,error)


application = webapp2.WSGIApplication([('/',MainPage)],debug=True)








