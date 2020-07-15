from django import template
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User, auth
import json
import random
import requests
from bs4 import BeautifulSoup
from Musica.models import Song, Playlist

register = template.Library()


@register.filter(name='Test')
def Test(query):
    base_url = f"https://www.saavn.com/api.php?__call=autocomplete.get&_marker=0&query={query}&ctx=android&_format=json&_marker=0"
    response = requests.get(base_url)
    print(response.json()['albums']['data'][0]['image'])
    return response.json()['albums']['data'][0]['image']