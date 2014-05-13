import os
import json
from django.shortcuts import render
from blog_app.models import New
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from datetime import date
from django.http import HttpResponse
from django.template.loader import render_to_string


def admin(request):
	dictionary = {}
	if request.method == 'POST':  # If the form has been submitted...
		#print(request.FILES)
		for upfile in request.FILES.getlist('pic'):
			today = date.today()
			path = default_storage.save(str(today.year) + '/' + str(today.month) + '/' + str(today.day) + '/' + upfile.name, ContentFile(upfile.read()))
			tmp_file = os.path.join(settings.MEDIA_ROOT, path)
		dictionary.update({
			'new_type': request.POST['new_type'],
			'name': request.POST['name'],
			'lid': request.POST['lid'],
			'html': request.POST['html'],
			})
		p = New(
				#pic = request.FILES['pic'],
				new_type = request.POST['new_type'],
				name = request.POST['name'],
				lid = request.POST['lid'],
				html = request.POST['html'],)
		print("debug")
		p.save()
	return render(request, 'admin.html', dictionary)


def admin_post_pic(request):
	if request.method == 'POST':  # If the form has been submitted...
		print(request.FILES)
		for upfile in request.FILES.getlist('file'):
			today = date.today()
			path = default_storage.save(str(today.year) + '/' + str(today.month) + '/' + str(today.day) + '/' + upfile.name, ContentFile(upfile.read()))
			tmp_file = os.path.join(settings.MEDIA_ROOT, path)
	response_data = {}
	response_data['status'] = "success"
	response_data['result'] = "Your file has been uploaded:"
	return HttpResponse(json.dumps(response_data), content_type='application/json')


def lenta(request):
	html_code = ""
	rcds = New.objects.all()[10:]
	for i in rcds:
		record = {
			'date': i.date,
			'type': i.new_type,
			'title': i.name,
			'info': i.lid,
			'lid': i.lid,
			'comments': i.looks,
		}
		html_code += render_to_string('pages/item_li.html', record)
	dictionary = {'stuff': html_code}
	return render(request, 'pages/lenta.html', dictionary)


def lenta_get(request):
	data = {'something': 'useful'}
	return HttpResponse(json.dumps(data), content_type="application/json")


def item(request, item_id):
	try:
		i = New.objects.get(id=item_id)
	except:
		return render(request, 'blog_app/404.html')
	i.looks += 1
	ctx = {
		'date': i.date,
		'type': i.new_type,
		'title': i.name,
		'info': i.lid,
		'lid': i.lid,
		'comments': i.looks,
	    'body': i.html,
	}
	return render(request, 'pages/item.html', ctx)


def search(request):
	return render(request, 'search.html')