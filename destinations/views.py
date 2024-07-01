from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import render
from destinations.models import Destination
from news.models import News


def index(request):
    page_number = request.GET.get("page")
    city = request.GET.get("city")
    news = Destination.objects.filter(city=city).all()
    paginator = Paginator(news, 10)

    page_obj = paginator.get_page(page_number)

    if city != None:
        return render(request, f"destination/{city}.html", {"page_obj": page_obj})

    return render(request, "destination/index.html", {"page_obj": page_obj})


def detail(request: HttpRequest, id: int):
    data = News.objects.filter(id=id).get()
    return render(request, "destination/detail.html", {"data": data})
