from __future__ import unicode_literals
import datetime
from django.db import models
from django.db.models import Count
import re
import bcrypt
from IPython import embed
import datetime
import pytz


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	def register(self, postData):
		errors = []
		if len(postData['first_name']) < 2:
			errors.append('First name must at least 2 letters')
		if not postData['first_name'].isalpha():
			errors.append('First name cannot contain numbers')
		if len(postData['last_name']) < 2:
			errors.append('Last name must at least 2 letters')
		if not postData['last_name'].isalpha():
			errors.append('Last name cannot contain numbers')
		if not EMAIL_REGEX.match(postData['email']):
			errors.append('Invalid Email')
		if len(postData['password']) < 8:
			errors.append('Password must be at least 8 charcters')
		if postData['password'] != postData['confirm_pw']:
			errors.append('Passwords do not match!')


		if not errors:
			password = postData['password'].encode()
			hashed = bcrypt.hashpw(password, bcrypt.gensalt())
			user = self.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], hash_pw = hashed)
			return { 'theuser': user }
		else:
			return { 'error': errors }

	def login(self, postData):
		errors = []
		if self.filter(email=postData['email']).exists():
			password = postData['password'].encode('utf-8')
			stored_hashed = User.objects.get(email=postData['email']).hash_pw
			if bcrypt.hashpw(password.encode('utf-8'), stored_hashed.encode()) != stored_hashed:
				print "INCORRECT PASSWORD"
				errors.append('Incorrect password')
			else:
				print "CORRECT PASSWORD"
				user = self.get(email=postData['email'])
		else:
			errors.append('Email is not registered')
	
		if not errors:
			return { 'theuser': user }
		else:
			return { 'error': errors }

# Create your models here.
class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	hash_pw = models.CharField(max_length=255)
	objects = UserManager()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "first name: " + self.first_name

class Secret(models.Model):
	content = models.TextField()
	user = models.ForeignKey(User)
	likes = models.ManyToManyField(User, related_name="likes")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

	def __unicode__(self):
		return "Secret content: " + self.content








