from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')


def ckeditor(request):
	return render(request, 'editor.html')