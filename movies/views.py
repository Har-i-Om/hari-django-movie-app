from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
import os

# Create your views here.
def home_page(request):
    user_query = str(request.GET.get('query',''))
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({Name}))")
    stuff_for_frontend = {'search_result': search_result}
    #print(user_query)
    return render(request, 'movies/movies_stuff.html', stuff_for_frontend)

def create(request):
    if request.method == 'POST' :
        data={
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url')}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')

        }
    AT.insert(data)
    return redirect('/')

def edit(request, movie_id):
    if request.method == 'POST' :
        data={
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url')}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')

        }

    AT.update(movie_id, data)

    return redirect('/')

AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'), 'Movies', api_key=os.environ.get('AIRTABLE_API_KEY'))
