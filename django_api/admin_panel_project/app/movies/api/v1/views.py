from django.contrib.postgres.aggregates import ArrayAgg, JSONBAgg
from django.db.models import Q, Prefetch, F
from django.http import JsonResponse, HttpResponse
from django.views.generic.list import BaseListView
from django.views.generic import ListView
from django.views.generic.detail import BaseDetailView
from django.contrib.postgres.expressions import ArraySubquery
from django.db.models import OuterRef
from django.db.models.functions import JSONObject

from movies.models import Filmwork, Genre, Person, GenreFilmwork, PersonFilmwork


class MoviesListApi(BaseListView):
    model = Filmwork
    http_method_names = ['get']  # Список методов, которые реализует обработчик
    
    def get_queryset(self):
        actors = PersonFilmwork.objects.filter(
            film_work_id=OuterRef('pk')
        ).filter(role='actor').values('person__full_name')

        directors = PersonFilmwork.objects.filter(
            film_work_id=OuterRef('pk')
        ).filter(role='director').values('person__full_name')

        writers = PersonFilmwork.objects.filter(
            film_work_id=OuterRef('pk')
        ).filter(role='writer').values('person__full_name')


        queryset = Filmwork.objects.values().annotate(
            genre=ArrayAgg('genres__name', distinct=True)
        ).annotate(
            actors=ArraySubquery(queryset=actors)
        ).annotate(
            directors=ArraySubquery(queryset=directors)
        ).annotate(
            writers=ArraySubquery(queryset=writers)
        )
        
        print(queryset.query)

        return queryset # Сформированный QuerySet

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = {
            'results': list(self.get_queryset()),
        }

        return context

    def render_to_response(self, context, **response_kwargs):
        context = self.get_context_data()
        return JsonResponse(context)



# class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

#     def get_context_data(self, **kwargs):
#         return  # Словарь с данными объекта
