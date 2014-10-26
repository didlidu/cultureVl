import os
import json
import datetime
import random
import re
from django.shortcuts import render, render_to_response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from blog_app.models import New, get_records
from blog_app.forms import UserForm, UserProfileForm
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


import os, sys
from PIL import Image

size = 320, 189

def thumbnail(infile):
    outfile = infile + ".thumbnail"
    if infile != outfile:
        try:
            im = Image.open(infile)
            im.thumbnail(size)
            im.save(outfile, "JPEG")
        except IOError:
            print ("cannot create thumbnail")


@login_required
def new(request):
    dictionary = {}
    if request.method == 'POST':  # If the form has been submitted...
        if not request.POST['id']:
            p = New(
                new_type=request.POST['new_type'],
                date=str(datetime.date.today()),
                name=request.POST['name'],
                lid=request.POST['lid'],
                info=request.POST['info'],
                html=request.POST['html'],
                authors=request.POST['authors'],
                is_enabled='is_enabled' in request.POST,
            )
        else:
            p = New.objects.get(id=request.POST['id'])
            p.new_type = request.POST['new_type']
            p.name = request.POST['name']
            p.lid = request.POST['lid']
            p.info = request.POST['info']
            p.html = request.POST['html']
            p.authors = request.POST['authors']
            p.is_enabled = 'is_enabled' in request.POST
            if request.POST['date']:
                new_date = request.POST['date'].split('.')
                date = p.date.isoformat().split('-')
                print(date)
                print(new_date)
                j = 2
                for i in new_date:
                    date[j] = i
                    j -= 1
                print(date)
                p.date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
        p.save()
        for upfile in request.FILES.getlist('pic'):
            if default_storage.exists(str(p.id) + '/' + "pic.jpg"):
                default_storage.delete(str(p.id) + '/' + "pic.jpg")
            if default_storage.exists(str(p.id) + '/' + "pic.jpg.thumbnail"):
                default_storage.delete(str(p.id) + '/' + "pic.jpg.thumbnail")
            path = default_storage.save(str(p.id) + '/' + "pic.jpg", ContentFile(upfile.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            thumbnail(tmp_file)
            p.pic_url = settings.MEDIA_URL + str(p.id) + '/' + "pic.jpg"
        p.save()
        red = '/restricted/edit/' + str(p.id)
        return HttpResponseRedirect(red)
    return render(request, 'new.html', {})


def about(request):
    return render(request, 'pages/static/about.html', {})


def redaction(request):
    return HttpResponseRedirect('/about/')
    # Till now
    return render(request, 'pages/static/redaction.html', {})


@login_required
def edit(request, id):
    try:
        if id:
            a = New.objects.get(id=id)
            dictionary = {
                'new_type': a.new_type,
                'name': a.name,
                'lid': a.lid,
                'info': a.info,
                'html': a.html,
                'pic_url': a.pic_url,
                'authors': a.authors,
                'is_enabled': a.is_enabled,
                'date': a.date,
                'id': a.id,
                'last_change': a.last_change,
            }
            return render(request, 'new.html', dictionary)
    except:
        pass
    return render(request, 'blog_app/404.html')


@login_required
def admin_del_pic(request):
    response_data = {}
    if request.method == 'POST':
        id = request.POST['id']
        name = request.POST['name']
        if default_storage.exists(id + '/' + name):
            default_storage.delete(id + '/' + name)
        response_data['status'] = "success"
        response_data['result'] = "Your file " + id + '/' + name + " has been deleted:"
    return HttpResponse(json.dumps(response_data), content_type='application/json')


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
                if default_storage.exists(str(get_new_id()) + '/' + upfile.name):
                    default_storage.delete(str(get_new_id()) + '/' + upfile.name)
                path = default_storage.save(str(get_new_id()) + '/' + upfile.name, ContentFile(upfile.read()))
            else:
                if default_storage.exists(str(id) + '/' + upfile.name):
                    default_storage.delete(str(id) + '/' + upfile.name)
                path = default_storage.save(str(id) + '/' + upfile.name, ContentFile(upfile.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
    response_data = {'status': "success", 'result': "Your file has been uploaded:"}
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
    next = 0
    try:
        next = request.COOKIES["next"]
    except:
        next = 0
    html_code = ""
    a = get_records(5, request.POST['type_of_page'], next)
    for i in a:
        ctx = {
            'id': i.id,
            'pic_url': i.pic_url,
            'date': i.date,
            'type': i.new_type,
            'title': i.name,
            'info': i.info,
            'lid': i.lid,
            'views': i.cviews,
            'comments': i.ccomments,
        }
        html_code += render_to_string('pages/parts/item_li.html', ctx)
        next = int(ctx['id'])
    response = HttpResponse(html_code)
    response.set_cookie("next", next)
    return response


def lenta_mask(request, mask):
    request.META["CSRF_COOKIE_USED"] = True
    rcds = get_records(5, mask, 0)
    html_code = ""
    next = 0
    for i in rcds:
        record = {
            'id': i.id,
            'date': i.date,
            'pic_url': i.pic_url,
            'type': i.new_type,
            'title': i.name,
            'info': i.info,
            'lid': i.lid,
            'views': i.cviews,
            'comments': i.ccomments,
        }
        next = record['id']
        html_code += render_to_string('pages/parts/item_li.html', record)
    dictionary = {'stuff': html_code, 'type_of_page': mask}
    response = render(request, 'pages/lenta.html', dictionary)
    response.set_cookie(key="next", value=next)
    return response


def lenta_get(request):
    data = {'something': 'useful'}
    return HttpResponse(json.dumps(data), content_type="application/json")


def item(request, item_id):
    context = RequestContext(request)
    html_code = ""
    q = ""
    try:
        u = New.objects.get(id=item_id)
        if not u.is_enabled:
            raise NameError('NewIsNotEnabledExeption')
    except:
        return render(request, 'blog_app/404.html', )
    u.cviews += 1
    u.save()
    count_news = 3

    rcds = New.objects.all().filter(is_enabled=True, date__gt=(datetime.date.today() - datetime.timedelta(days=30))).exclude(date__gt=datetime.date.today(), id=u.id).order_by('-cviews')
    if len(rcds) < 3:
        rcds = New.objects.all().filter(is_enabled=True, date__gt=(datetime.date.today() - datetime.timedelta(days=90))).exclude(date__gt=datetime.date.today(), id=u.id).order_by('-cviews')
    if len(rcds) >= 3:
        z = [rcds.first()]
        rcds = rcds.exclude(id=z[0].id)
        j = random.sample(range(len(rcds)), 2)
        for i in j:
            z.append(rcds[i])
        j = 0
        random.shuffle(z)
        for i in z:
            j += 1
            record = {
                'id': i.id,
                'date': i.date,
                'pic_url': i.pic_url,
                'type': i.new_type,
                'lid': i.lid,
                'title': i.name,
                'views': i.cviews,
            }
            q += render_to_string('pages/parts/little_div.html', record)
            if j == count_news: break

    record = {
        'id': u.id,
        'main_pic': u.pic_url,
        'date': u.date,
        'type': u.new_type,
        'body': u.html,
        'title': u.name,
        'authors': u.authors,
        'info': u.info,
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
            'authors': request.POST['authors'],
            'date': str(datetime.datetime.now()),
            'type': request.POST['new_type'],
            'body': request.POST['html'],
            'title': request.POST['name'],
            'info': request.POST['info'],
            'lid': request.POST['lid'],
            'views': 0,
        }
    html_code = ""
    html_code += render_to_string('blog_app/header.html', record)
    html_code += render_to_string('pages/preview.html', record)
    html_code += render_to_string('blog_app/footer.html', record)
    return HttpResponse(html_code)


def search(request):
    return render(request, 'pages/search.html')


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
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('blog_app/login.html', {}, context)


@login_required
def restricted(request):
    context = RequestContext(request)
    return render_to_response('restricted/restricted.html', {}, context)


@login_required
def profile(request):
    context = RequestContext(request)
    return render_to_response('restricted/profile.html', {}, context)


@login_required
def archive(request):
    context = RequestContext(request)
    rrr = New.objects.all()
    html_code = ""
    for i in reversed(rrr):
        record = {
            'id': i.id,
            'date': i.date,
            'type': i.new_type,
            'title': i.name,
            'is_active': i.is_enabled,
            'authors': i.authors,
            'views': i.cviews,
        }
        html_code += render_to_string('pages/parts/archive_td.html', record)
    return render_to_response('restricted/archive.html', {'info': html_code}, context)


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')
