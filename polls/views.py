from django.core.paginator import Paginator
from django.shortcuts import render
from polls.models import News


def index(request):
    page_number = request.GET.get("page")
    news = News.objects.all()
    paginator = Paginator(news, 10)
    print("paginator", paginator)

    page_obj = paginator.get_page(page_number)

    return render(request, "news.html", {"page_obj": page_obj})
