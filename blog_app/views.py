import os
from django.shortcuts import render
from blog_app.models import New
from Svetanyashmyash.settings import ROOT_PATH
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings


def admin(request):
	dictionary = {}
	if request.method == 'POST':  # If the form has been submitted...
		print(request.FILES)
		for upfile in request.FILES.getlist('pic'):
			path = default_storage.save('%Y/%m/%d/somename.jpg', ContentFile(upfile.read()))
			tmp_file = os.path.join(settings.MEDIA_ROOT, path)
			print("1")
			#filename = ROOT_PATH + "/media/" + upfile.name
			#fd = open(filename, 'w')
			#for chunk in upfile.chunks():
			#	fd.write(chunk)
			#fd.close()
		dictionary.update({
			#'pic_url': request.POST['pic_url'],
			'new_type': request.POST['new_type'],
			'name': request.POST['name'],
			'lid': request.POST['lid'],
			'html': request.POST['html'],
			})
		p = New(
				#pic_url = request.POST['pic_url'],
				#pic = request.FILES['pic'],
				new_type = request.POST['new_type'],
				name = request.POST['name'],
				lid = request.POST['lid'],
				html = request.POST['html'],)
		print("debug")
		p.save()
	return render(request, 'admin.html', dictionary)


def lenta(request):
	return render(request, 'pages/lenta.html')


def about(request):
	return render(request, 'pages/about.html')


def redaction(request):
	return render(request, 'pages/redaction.html')


def search(request):
	return render(request, 'search.html')


def premiera(request):
	return render(request, 'pages/premiera.html')


def news(request):
	return render(request, 'pages/news.html')


def personality(request):
	return render(request, 'pages/personality.html')


def afisha(request):
	return render(request, 'pages/afisha.html')