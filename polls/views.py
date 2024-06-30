from django.core.paginator import Paginator
from django.shortcuts import render
from polls.models import News


def index(request):
    print("request", request)

    news = News.objects.all().iterator()
    paginator = Paginator(news, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "book_list.html", {"page_obj": page_obj})
