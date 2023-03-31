from django.contrib.postgres.aggregates import ArrayAgg
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from django.contrib.postgres.expressions import ArraySubquery
from django.db.models import OuterRef, Subquery

from movies.models import Filmwork, PersonFilmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']
    paginate_by = 50

    def get_queryset(self, pk=None):

        actors = Subquery(
            PersonFilmwork.objects.select_related(
            'person'
            ).filter(
                film_work=OuterRef('pk'),
                role=PersonFilmwork.RoleInFilm.ACTOR
            ).values('person__full_name')
        )

        directors = Subquery(
            PersonFilmwork.objects.select_related(
            'person'
            ).filter(
                film_work=OuterRef('pk'),
                role=PersonFilmwork.RoleInFilm.DIRECTOR
            ).values('person__full_name')
        )

        writers = Subquery(
            PersonFilmwork.objects.select_related(
            'person'
            ).filter(
                film_work=OuterRef('pk'),
                role=PersonFilmwork.RoleInFilm.WRITER
            ).values('person__full_name')
        )

        queryset = Filmwork.objects.prefetch_related(
            'genres', 'persons'
        ).values(
            'id', 'title', 'description', 'creation_date',
            'rating', 'film_type'
        ).annotate(
            genres=ArrayAgg('genres__name', distinct=True)
        ).annotate(
            actors=ArraySubquery(queryset=actors)
        ).annotate(
            directors=ArraySubquery(queryset=directors)
        ).annotate(
            writers=ArraySubquery(queryset=writers)
        )

        if pk:
            queryset = Filmwork.objects.prefetch_related(
                'genres', 'persons'
            ).values(
                'id', 'title', 'description', 'creation_date',
                'rating', 'film_type'
            ).annotate(
                genres=ArrayAgg('genres__name', distinct=True)
            ).annotate(
                actors=ArraySubquery(queryset=actors)
            ).annotate(
                directors=ArraySubquery(queryset=directors)
            ).annotate(
                writers=ArraySubquery(queryset=writers)
            ).get(id=pk)

        return queryset

    def render_to_response(self, *args, **kwargs):
        return JsonResponse(self.get_context_data())


class MoviesListApi(MoviesApiMixin, BaseListView):
    def get_context_data(self, *args, object_list=None, **kwargs):
        queryset = list(self.get_queryset())
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by,
        )
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': page.object_list,
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, **kwargs):
        return self.get_queryset(self.kwargs['pk'])
