import os
import webapp2
import jinja2

from google.appengine.ext import ndb
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from models import MailMessage
from utils import hash_string

JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# Mail Receiver
class ReceiveMailHandler(InboundMailHandler):
	def receive(self, mail):
		if mail.sender:
			bodies = mail.bodies('text/plain')
			body_text = ''
			for content_type, body in bodies:
				body_text += body.decode()

			m = MailMessage(name=hash_string(mail.sender), subject=mail.subject, body=body_text)
			m.put()

# Pages
class MainPage(webapp2.RequestHandler):
	def get(self, name):
		lookup = hash_string(name)
		messages = MailMessage.query_by_name(lookup)

		template = JINJA_ENV.get_template('html/index.html')
		self.response.write(template.render({
			'messages': messages
		}))

app = webapp2.WSGIApplication([('/(.*)', MainPage)], debug=True) 
save = webapp2.WSGIApplication([ReceiveMailHandler.mapping()], debug=True)