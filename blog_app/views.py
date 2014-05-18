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
		if not request.POST['id']:
			p = New(
					new_type = request.POST['new_type'],
					name = request.POST['name'],
					lid = request.POST['lid'],
					html = request.POST['html'],)
		else:
			p = New.objects.get(id=request.POST['id'])
			p.new_type = request.POST['new_type']
			p.name = request.POST['name']
			p.lid = request.POST['lid']
			p.html = request.POST['html']
		p.save()
		for upfile in request.FILES.getlist('pic'):
			path = default_storage.save(str(p.id) + '/' + "pic.jpg", ContentFile(upfile.read()))
			tmp_file = os.path.join(settings.MEDIA_ROOT, path)
			p.pic_url = str(p.id) + '/' + "pic.jpg"
		p.save()
		dictionary.update({
			'new_type': request.POST['new_type'],
			'name': request.POST['name'],
			'lid': request.POST['lid'],
			'html': request.POST['html'],
			'pic_url': p.pic_url,
			'id': p.id,
			})
		print(request.POST['name'])
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


def admin_get_pic(request):
	list_dir = {}
	if request.method == 'POST':
		id = int(request.POST['id'])
		list_dir = os.listdir(settings.MEDIA_ROOT + str(id))
	return HttpResponse(json.dumps(list_dir), content_type='application/json')


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
			'type': i.new_type,
			'title': i.name,
			'views': i.cviews,
		}
		q += render_to_string('pages/parts/little_div.html', record)
		if j == count_news: break

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
		'other_news': q,
	}
	
	html_code += render_to_string('blog_app/header.html', record)
	html_code += render_to_string('pages/item.html', record)
	html_code += render_to_string('blog_app/footer.html', record)
	return HttpResponse(html_code)


def search(request):
	return render(request, 'search.html')