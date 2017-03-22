from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from .models import User, Secret


# Create your views here.
def index(request):
	return render(request, "dojosecrets/index.html")

def secrets(request):
	# now = pytz.utc.localize(datetime.datetime.now())
	secrets = Secret.objects.all().order_by('-created_at')
	context = {
		'user': User.objects.get(id=request.session['user']),
		'secrets': secrets,
	}
	return render(request, "dojosecrets/secrets.html", context)

def popular(request):
	context = {
		"secrets": Secret.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')
	}
	return render(request, "dojosecrets/popular.html", context)


# processing login and registration
def process(request):
	if request.POST['action'] == 'register':
		postData = {
			'first_name': request.POST['first_name'],
			'last_name': request.POST['last_name'],
			'email': request.POST['email'],
			'password': request.POST['password'],
			'confirm_pw': request.POST['confirm_pw']
		}
		user = User.objects.register(postData)
		if 'error' in user:
			for message in user['error']:
				messages.error(request, message)
			return redirect('/')
		if 'theuser' in user:
			messages.success(request, 'Successfully registered, you may now log in.')
			return redirect('/')
	elif request.POST['action'] == 'login':
		postData = {
			'email': request.POST['email'],
			'password': request.POST['password']
		}
		user = User.objects.login(postData)
		if 'error' in user:
			for message in user['error']:
				messages.error(request, message)
			return redirect('/')
		if 'theuser' in user:
			request.session['user'] = user['theuser'].id
			return redirect('/secrets')


# process posting a secret to the wall
def post(request):
	user = User.objects.get(id=request.session['user'])
	secret = Secret.objects.create(content=request.POST['secret-text'], user=user) #user_id=request.session['user']
	return redirect('/secrets')

# create a like link between users and secrets
def like_post(request, id):
	user = User.objects.get(id=request.session['user'])
	secret = Secret.objects.get(id=id)
	if secret.likes.filter(id=request.session['user']).count() ==1:
		secret.likes.remove(user)
	else:
		secret.likes.add(user)
	return redirect('/secrets')

# delete a post
def delete(request, id):
	Secret.objects.get(id=id).delete()
	return redirect('/secrets')

# logout
def logout(request):
	request.session.clear()
	return redirect('/')












