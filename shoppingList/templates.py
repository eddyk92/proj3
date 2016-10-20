import os

import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)


class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class Shopping(Handler):
	def get(self):
		items = self.request.get_all("food")
		self.render("shopping_list_html", items = items)
		# if items:
		# 	output_items = ""
		# 	for item in items:
		# 		output_hidden += hidden_html % item
		# 		output_items += hidden_html % item

		# 	output_shopping = shopping_list_html % item
		# 	outout += output_shopping

		# output = output % output_hidden

		# self.write(output)

class FizzBuzz(Handler):
	def get(self):
		n = self.request.get("n")
		if n.isdigit():
			n = int(n)
		self.render('fizzbuzz.html', n = n)

app = webapp2.WSGIApplication([
	('/shopping_list', Shopping), 
		'/fizzbuzz', FizzBuzz)
], debug=True)












