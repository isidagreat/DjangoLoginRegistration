from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User
import bcrypt

def index(request):
	return render(request, "login_registration/index.html")

def process(request):
	if request.method == "POST":
		errors = User.objects.basic_validator(request.POST)
		# check if there are any errors
		if len(errors):
			# if there are errors loop through key value pairs
			for key, value in errors.items():
				messages.error(request,value)
				# redirect to new user form
			return redirect(index)
		else:
			hash1= bcrypt.hashpw(request.POST['pword'].encode(), bcrypt.gensalt())
			newuser = User(first_name = request.POST['fname'], last_name= request.POST['lname'], email = request.POST['email'], password = hash1)
			newuser.save()
			request.session['id'] = newuser.id
			request.session['name'] = newuser.first_name
			print(request.session['id'])
			print(request.session['name'])
			messages.success(request, "Successfully registered")
			return redirect(success)
	else:
		return redirect(index)

def verify(request):
	if request.method == "POST":
		errors = User.objects.login_validator(request.POST)
		# check if there are any errors
		if len(errors):
			# if there are errors loop through key value pairs
			for key, value in errors.items():
				messages.error(request,value)
				# redirect to new user form
			return redirect(index)
		try:
			user = User.objects.get(email = request.POST['email'])
			print(user.first_name)
		except:
			messages.error(request, "Could not log in")
			return redirect(index)
		if bcrypt.checkpw(request.POST['pword'].encode(), user.password.encode()):
			request.session['id'] = user.id
			request.session['name'] =   user.first_name
			messages.success(request, "Successfully logged In")
			print("passwords match")
			return redirect(success)
		else:
			messages.error(request, "Could not log in")
			return redirect(index)
	else:
		return redirect(index)

def success(request):
	if 'id' in request.session:
		return render(request,"login_registration/success.html")
	else:
		messages.error(request, "You're not Logged in")
		return redirect(index)

