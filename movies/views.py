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
            'Pictures': [{'url': request.POST.get('url') or 'http://www.gladessheriff.org/media/images/most%20wanted/No%20image%20available.jpg'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')

        }
        try:
            response = AT.insert(data)

            #notify on adding movie
            messages.success(request,'Movie added: {}'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'Got an error while adding the movie: {}'.format(e))

    return redirect('/')



def edit(request, movie_id):
    if request.method == 'POST' :
        data={
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'http://www.gladessheriff.org/media/images/most%20wanted/No%20image%20available.jpg'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')

        }
        try:
            response=AT.update(movie_id, data)
            #notify on update
            messages.success(request,'Movie updated: {}'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'Got an error while updating the movie: {}'.format(e))

    return redirect('/')

def delete(request, movie_id):
    try:
        movie_deleted = AT.get(movie_id)['fields'].get('Name')
        AT.delete(movie_id)
        messages.warning(request, 'Movie deleted: {}'.format(movie_deleted))  #notify on delete
    except Exception as e:
        messages.warning(request, 'Got an error: {}'.format(e))

    return redirect('/')


AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'), 'Movies', api_key=os.environ.get('AIRTABLE_API_KEY'))
