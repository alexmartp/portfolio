from django.shortcuts import render

def index(context):
    return render(
        context,
        "index.html"
    )