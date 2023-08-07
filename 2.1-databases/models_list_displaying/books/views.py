from django.core.paginator import Paginator
from django.shortcuts import render
from books.models import Book
from django.template.defaultfilters import slugify
from datetime import datetime
def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    context = {'books': books}
    return render(request, template, context)


def book_view(request, slug):
    template = 'books/book.html'
    book = Book.objects.filter(pub_date=slug)
    all_date = Book.objects.values_list('pub_date')
    date_dict = []
    for date in all_date:
        date = "{:%Y %m %d}".format(date[0])
        date = slugify(date)
        # if date == slug:
        #     continue
        date_dict.append(date)
    page = date_dict.index(slug)
    if len(date_dict) == page + 1:
        next_page = date_dict[0]
    else:
        next_page = date_dict[page + 1]

    if page == 0:
        previous_page = date_dict[-1]
    else:
        previous_page = date_dict[page - 1]


    #
    # pagi = Paginator(date, 1)
    # page = pagi.get_page(slug)

    context = {'book': book,
               'page': {'next_page': next_page,
                        'previous_page': previous_page
                        }
               }
    return render(request, template, context)