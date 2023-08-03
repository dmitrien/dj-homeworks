from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'

    phones = Phone.objects.all()
    context = {'phones': phones}
    return render(request, template, context)

def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.filter(slug=slug)
    for c in phone:
        result_phone = {'name': c.name, 'image': c.image, 'price': c.price, 'release_date': c.release_date, 'lte_exist': c.lte_exists }

    context = {'phone': result_phone}
    return render(request, template, context)
