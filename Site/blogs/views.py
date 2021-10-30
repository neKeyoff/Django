from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.views.generic import UpdateView, DeleteView

from .forms import CreateForm
from .models import Blog


def index(request):
    latest_blog_list = Blog.objects.order_by('-pub_date')[:10]
    template = loader.get_template('blogs/Index.html')
    context = {
        'latest_blog_list': latest_blog_list,
    }
    return render(request, 'blogs/index.html', context)

def detail(request, Blog_id):
    try:
        blog = Blog.objects.get(pk=Blog_id)
    except Blog.DoesNotExist:
        raise Http404("Блога не существует")
    return render(request, 'blogs/detail.html', {'blog': blog})


def create(request):
    error =''
    if request.method == 'POST':
        form = CreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blogs:success_saved'))
        else:
            error = 'Wrong form filling'

    form = CreateForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'blogs/create.html', data)


def success_saved(request):
    return render(request, 'blogs/success_saved.html')


class Update(UpdateView):
    model = Blog
    pk_url_kwarg = "Blog_id"
    template_name = 'blogs/update.html'
    form_class = CreateForm
    success_url = '/blogs/'


class Delete(DeleteView):
    model = Blog
    pk_url_kwarg = "Blog_id"
    success_url = '/blogs/'
    template_name = 'blogs/delete.html'

