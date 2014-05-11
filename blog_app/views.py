from django.shortcuts import render
from blog_app.models import New


def admin(request):
	dictionary = {}
	if request.method == 'POST':  # If the form has been submitted...
		dictionary.update({
			'pic_url': request.POST['pic_url'],
			'new_type': request.POST['new_type'],
			'name': request.POST['name'],
			'lid': request.POST['lid'],
			'html': request.POST['html'],})
		p = New(
				pic_url = request.POST['pic_url'],
				new_type = request.POST['new_type'],
				name = request.POST['name'],
				lid = request.POST['lid'],
				html = request.POST['html'],)
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