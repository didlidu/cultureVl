import os
import json
from django.shortcuts import render
from blog_app.models import New, get_records
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string


def admin(request):
	dictionary = {}
	if request.method == 'POST':  # If the form has been submitted...
		p = New(
				#pic = request.FILES['pic'],
				new_type = request.POST['new_type'],
				name = request.POST['name'],
				lid = request.POST['lid'],
				html = request.POST['html'],)
		p.save()
		print(p.id)
		print(request.FILES)
		for upfile in request.FILES.getlist('pic'):
			path = default_storage.save(str(p.id) + '/' + "pic.jpg", ContentFile(upfile.read()))
			tmp_file = os.path.join(settings.MEDIA_ROOT, path)
		dictionary.update({
			'new_type': request.POST['new_type'],
			'name': request.POST['name'],
			'lid': request.POST['lid'],
			'html': request.POST['html'],
			})
	return render(request, 'admin.html', dictionary)


def admin_post_pic(request):
	if request.method == 'POST':  # If the form has been submitted...
		#print(request.FILES)
		for upfile in request.FILES.getlist('file'):
			path = default_storage.save(str(request.POST['id']) + '/' + upfile.name, ContentFile(upfile.read()))
			tmp_file = os.path.join(settings.MEDIA_ROOT, path)
	response_data = {}
	response_data['status'] = "success"
	response_data['result'] = "Your file has been uploaded:"
	return HttpResponse(json.dumps(response_data), content_type='application/json')


def lenta(request):
	a = get_records(10, 1, 0)
	print(a)
	html_code = ""
	rcds = New.objects.all()[:10]
	for i in rcds:
		record = {
			'id': i.id,
			'date': i.date,
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
	html_code = ""
	u = New.objects.get(id=item_id)
	u.cviews += 1
	u.save()
	record = {
			'id': u.id,
			'date': u.date,
			'type': u.new_type,
			'body': u.html,
			'title': u.name,
			'info': u.lid,
			'lid': u.lid,
			'views': u.cviews,
			'comments': u.ccomments,
	}
	rcds = New.objects.all()[:4]
	j = 1
	for i in rcds:
		if u.id == i.id: continue
		record.update({
			'id_'+str(j): i.id,
			'date_'+str(j): i.date,
			'type_'+str(j): i.new_type,
			'title_'+str(j): i.name,
			'info_'+str(j): i.lid,
			'lid_'+str(j): i.lid,
			'views_'+str(j): i.cviews,
			'comments_'+str(j): i.ccomments,
		})
		j += 1
	html_code += render_to_string('blog_app/header.html', record)
	html_code += render_to_string('pages/item.html', record)
	html_code += render_to_string('blog_app/footer.html', record)
	return HttpResponse(html_code)
	try:
		i = New.objects.get(id=item_id)
	except:
		return render(request, 'pages/item.html')
	i.looks += 1
	ctx = {
		'date': i.date,
		'type': i.new_type,
		'title': i.name,
		'info': i.lid,
		'lid': i.lid,
		'comments': i.ccomments,
	    'views': i.cviews,
	}
	return render(request, 'pages/item.html', ctx)


def search(request):
	return render(request, 'search.html')