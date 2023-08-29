from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView# импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from .models import News
from datetime import datetime
from django.shortcuts import render
from django.core.paginator import Paginator # импортируем класс, позволяющий удобно осуществлять постраничный вывод
from .filters import NewsFilter # импортируем недавно написанный фильтр
from django.urls import reverse_lazy
 
 
class NewsList(ListView):
    model = News  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = News.objects.order_by('-id')
    paginate_by = 1

    # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон. В возвращаемом словаре context будут храниться все переменные. Ключи этого словари и есть переменные, к которым мы сможем потом обратиться через шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow() # добавим переменную текущей даты time_now
        context['value1'] = None # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        return context
    
 
class NewsDetail(DetailView):
    model = News # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'detail.html' # название шаблона будет product.html
    context_object_name = 'detail' # название объекта  

class News(View):
    
    def get(self, request):
        news = News.objects.order_by('-id')
        p = Paginator(news, 1) # создаём объект класса пагинатор, передаём ему список наших товаров и их количество для одной страницы
 
        news = p.get_page(request.GET.get('page', 1)) # берём номер страницы из get-запроса. Если ничего не передали, будем показывать первую страницу.
        # теперь вместо всех объектов в списке товаров хранится только нужная нам страница с товарами
        
        data = {
            'news': news,
        }
        return render(request, 'news.html', data)
    
class PostCreateView(CreateView):
    model = News
    context_object_name = 'new_post_form'
    template_name = 'MyApp/post_create.html'
    fields = ('author', 'header', 'body', 'news_date')
    success_url = reverse_lazy('news_list')
   
class PostUpdateView(UpdateView):
    model = News
    context_object_name = 'edit_news_form'
    template_name = 'MyApp/news_edit.html'
    fields = ('header', 'body')
    success_url = reverse_lazy('viewname=news_list')
    
class PostDeleteView(DeleteView):
    model = News
    context_object_name = 'delete_news_form'
    template_name = 'MyApp/news_delete.html'
    fields = ('header', 'news_date')
    success_url = reverse_lazy('news_list')

class PostDetailedView(DetailView):
    model = News
    template_name = 'MyApp/post_details.html'
    queryset = News.objects.all()
    