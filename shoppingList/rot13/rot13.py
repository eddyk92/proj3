import webapp2
import os
import jinja2

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

def rot13(text):
    alphab = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

    rot = ""
    for i in text:
    	if i.isalph():
    		try:
    			rot += aplhab[(alphab.index(i)+13)%len(alphab)]
    			pass
    		except:
    			rot += alpha[(alpha.index(i)+13)%len(alpha)]

    	else:
    		rot += i
    return rot

class MainPage(Handler):
	def get(self):
		text = self.request.get('text')
		self.render("rot13.html", text = text)

	def post(self):
		self.request.get('text')
		text = self.request.get('text')
		self.render("rot13.html", text = rot13(text)) 

app = webapp2.WSGIApplication([
	('/rot13.html', MainPage)
	], debug=True)









