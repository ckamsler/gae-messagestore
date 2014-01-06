import hashlib

def hash_string(value):
	if not value:
		return None
		
	return hashlib.sha1(value).hexdigest()


def format_date(value, format='%Y'):
	return value.strftime(format)