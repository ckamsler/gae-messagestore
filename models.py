from google.appengine.ext import ndb

class MailMessage(ndb.Model):
	name = ndb.StringProperty()
	body = ndb.StringProperty()
	subject = ndb.StringProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def query_by_name(self, name):
		if name:
			query = self.query(MailMessage.name==name).order(-self.date)
		else:
			query = self.query()

		return query.order(-self.date)