from django.shortcuts import get_object_or_404, render
from django.http import Http404

# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader

from Utilities import Utilities


utilities = Utilities()

def index(request):
    context = {}
    return render(request, 'index.html', context)


def detail(request, id):
    artists = utilities.getUser(id)
    context = {'artists': artists, 'id': id}
    return render(request, 'detail.html', context)

def detailByGrade(request, id, grade):
    artists = utilities.getUser(id)
    filtred = []
    for _name, _grade, _tag in artists:
        if int(_grade) == int(grade):
            filtred += [(_name, _grade, _tag)]
    context = {'artists': filtred, 'id': id, 'selectedGrade': grade}
    return render(request, 'detail.html', context)


def randomUser(request):
    artists, id = utilities.getRandomUser()
    context = {'artists': artists, 'id': id}
    return render(request, 'detail.html', context)



def predict(request, id):
    context = {'artists': utilities.predictRBM(id, 100), 'id': id, 'predicted': True}
    return render(request, 'detail.html', context)
