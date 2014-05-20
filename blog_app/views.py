import os
import json
from django.shortcuts import render, render_to_response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from blog_app.models import New, get_records
from blog_app.forms import UserForm, UserProfileForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime

@login_required
def new(request):
	dictionary = {}
	if request.method == 'POST':  # If the form has been submitted...
		if not request.POST['id']:
			p = New(
					new_type = request.POST['new_type'],
					name = request.POST['name'],
					lid = request.POST['lid'],
					html = request.POST['html'],
					authors = request.POST['authors'],
					is_enabled = 'is_enabled' in request.POST,
					)
		else:
			p = New.objects.get(id=request.POST['id'])
			p.new_type = request.POST['new_type']
			p.name = request.POST['name']
			p.lid = request.POST['lid']
			p.html = request.POST['html']
			p.authors = request.POST['authors']
			p.is_enabled = 'is_enabled' in request.POST
		p.save()
		for upfile in request.FILES.getlist('pic'):
			path = default_storage.save(str(p.id) + '/' + "pic.jpg", ContentFile(upfile.read()))
			tmp_file = os.path.join(settings.MEDIA_ROOT, path)
			p.pic_url = settings.MEDIA_URL + str(p.id) + '/' + "pic.jpg"
		p.save()
		dictionary.update({
			'new_type': request.POST['new_type'],
			'name': request.POST['name'],
			'lid': request.POST['lid'],
			'html': request.POST['html'],
			'authors': request.POST['authors'],
			'is_enabled': 'is_enabled' in request.POST,
			'pic_url': p.pic_url,
			'id': p.id,
			})
		print(request.POST['name'])
	return render(request, 'new.html', dictionary)

@login_required
def edit(request, id):
	try:
		if id:
			a = New.objects.get(id=id)
			dictionary = {
				'new_type': a.new_type,
				'name': a.name,
				'lid': a.lid,
				'html': a.html,
				'pic_url': a.pic_url,
				'id': a.id,
				'authors': a.authors,
				'is_enabled': a.authors,
			}
			return render(request, 'new.html', dictionary)
	except:
		pass
	return render(request, 'blog_app/404.html')


def get_new_id():
	last = New.objects.last()
	if last != None:
		id = last.id
	else:
		id = 0
	return id + 1


@login_required
def admin_post_pic(request):
	if request.method == 'POST':
		id = int(request.POST['id'])
		for upfile in request.FILES.getlist('file'):
			if id == -1:
				path = default_storage.save(str(get_new_id()) + '/' + upfile.name, ContentFile(upfile.read()))
			else:
				path = default_storage.save(str(id) + '/' + upfile.name, ContentFile(upfile.read()))
			tmp_file = os.path.join(settings.MEDIA_ROOT, path)
	response_data = {}
	response_data['status'] = "success"
	response_data['result'] = "Your file has been uploaded:"
	return HttpResponse(json.dumps(response_data), content_type='application/json')


@login_required
def admin_get_pic(request):
	list_dir = {}
	try:
		if request.method == 'GET':
			id = int(request.GET.get("id"))
			if id == -1:
				id = get_new_id()
			list_dir = os.listdir(settings.MEDIA_ROOT + '/' + str(id))
			for i in range(0, len(list_dir)):
				list_dir[i] = str(id) + '/' + list_dir[i]
	except: 
		pass
	return HttpResponse(json.dumps(list_dir), content_type='application/json')


def get_more(request):
	if request.is_ajax():
		a = get_records(10, 1, 0)
		html_code = ""
		for i in a:
			ctx = {
			'id': i.id,
			'date': i.date,
			'type': i.new_type,
			'title': i.name,
			'info': i.lid,
			'lid': i.lid,
			'views': i.cviews,
			'comments': i.ccomments,
		}
		html_code += render_to_string('pages/item_li.html', ctx)
	return HttpResponse(html_code)

def lenta(request):
	print(get_records(10,"",0))
	print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
	rcds = New.objects.all().order_by('-id')[:5]
	html_code = ""
	for i in rcds:
		record = {
			'id': i.id,
			'date': i.date,
			'pic_url': settings.MEDIA_URL + i.pic_url,
			'type': i.new_type,
			'title': i.name,
			'info': i.lid,
			'lid': i.lid,
			'views': i.cviews,
			'comments': i.ccomments,
		}
		html_code += render_to_string('pages/item_li.html', record)
	dictionary = {'stuff': html_code}
	return render(request, 'pages/lenta.html', dictionary)


def lenta_get(request):
	data = {'something': 'useful'}
	return HttpResponse(json.dumps(data), content_type="application/json")


def item(request, item_id):
	context = RequestContext(request)
	html_code = ""
	q = ""
	try:
		u = New.objects.get(id=item_id)
	except:
		return render(request, 'blog_app/404.html', )
	u.cviews += 1
	u.save()
	count_news = 3
	j = 0
	rcds = New.objects.all()[:count_news+1]
	for i in rcds:
		if u.id == i.id: continue
		j += 1
		record = {
			'id': i.id,
			'date': i.date,
			'pic_url': settings.MEDIA_URL + i.pic_url,
			'type': i.new_type,
			'title': i.name,
			'views': i.cviews,
		}
		q += render_to_string('pages/parts/little_div.html', record)
		if j == count_news: break

	record = {
		'id': u.id,
		'main_pic': settings.MEDIA_URL + u.pic_url,
		'date': u.date,
		'type': u.new_type,
		'body': u.html,
		'title': u.name,
		'info': u.lid,
		'lid': u.lid,
		'views': u.cviews,
		'comments': u.ccomments,
		'other_news': q,
	}
	
	html_code += render_to_string('blog_app/header.html', record, context)
	html_code += render_to_string('pages/item.html', record, context)
	html_code += render_to_string('blog_app/footer.html', record)
	return HttpResponse(html_code)


def preview(request):
	if request.method == "POST":
		record = {
			'id': request.POST['id'],
			'main_pic': request.POST['pic_url'],
			'date': datetime.date.today(),
			'type': request.POST['new_type'],
			'body': request.POST['html'],
			'title': request.POST['name'],
			'info': request.POST['lid'],
			'lid': request.POST['lid'],
			'views': 0,
			'comments': 0,
		}
	html_code = ""
	html_code += render_to_string('blog_app/header.html', record)
	html_code += render_to_string('pages/item.html', record)
	html_code += render_to_string('blog_app/footer.html', record)
	return HttpResponse(html_code)



def search(request):
	return render(request, 'search.html')


def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    ctx = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
    return render_to_response(
            'blog_app/registration.html', ctx, context)


def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/staff/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Culture account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('blog_app/login.html', {}, context)


def culture(request):
	context = RequestContext(request)
	return render_to_response('blog_app/staff_only.html', {},context)

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')
