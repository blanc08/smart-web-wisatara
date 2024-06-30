from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from news.models import News


def index(request):
    page_number = request.GET.get("page")
    news = News.objects.all()
    paginator = Paginator(news, 10)
    print("paginator", paginator)

    page_obj = paginator.get_page(page_number)

    return render(request, "blog/index.html", {"page_obj": page_obj})


def single_blog(request: HttpRequest, id: int):
    data = News.objects.filter(id=id).get()
    return render(request, "blog/single-blog.html", {"data": data})
