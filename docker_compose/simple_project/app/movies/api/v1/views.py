from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from django.http import JsonResponse
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import F, Value
from django.db.models.functions import Coalesce

from movies.models import FilmWork


def annotate_filmwork(queryset):
    """
    Аннотирует QuerySet полями actors, directors, writers и genres.
    """
    return queryset.annotate(
        annotated_genres=ArrayAgg('genres__name', distinct=True),
        actors=ArrayAgg(
            Coalesce(F('personfilmwork__person__full_name'), Value('')),
            filter=F('personfilmwork__role') == 'actor',
            distinct=True,
        ),
        directors=ArrayAgg(
            Coalesce(F('personfilmwork__person__full_name'), Value('')),
            filter=F('personfilmwork__role') == 'director',
            distinct=True,
        ),
        writers=ArrayAgg(
            Coalesce(F('personfilmwork__person__full_name'), Value('')),
            filter=F('personfilmwork__role') == 'writer',
            distinct=True,
        ),
    )


class MoviesListApi(BaseListView):
    model = FilmWork
    paginate_by = 50

    def get_page_number(self) -> int:
        """
        Определяет номер страницы (учитывая 'last' и некорректные значения).
        """
        page = self.request.GET.get('page', 1)

        if page == 'last':
            total_count = self.model.objects.count()
            total_pages = (total_count + self.paginate_by - 1) // self.paginate_by
            return total_pages

        try:
            return int(page)
        except ValueError:
            return 1

    def get_queryset(self):
        """
        Возвращает аннотированный QuerySet с учётом пагинации.
        """
        page_number = self.get_page_number()
        start = (page_number - 1) * self.paginate_by
        end = start + self.paginate_by

        base_qs = self.model.objects.all()
        return annotate_filmwork(base_qs)[start:end]

    def get_context_data(self, *, object_list=None, **kwargs):
        total_count = self.model.objects.count()
        total_pages = (total_count + self.paginate_by - 1) // self.paginate_by

        page_number = self.get_page_number()
        queryset = self.get_queryset()

        results = [
            {
                'id': film.id,
                'title': film.title,
                'description': film.description,
                'creation_date': film.creation_date,
                'rating': film.rating,
                'type': film.type,
                'genres': film.annotated_genres or [],
                'actors': film.actors or [],
                'directors': film.directors or [],
                'writers': film.writers or [],
            }
            for film in queryset
        ]

        context = {
            'count': total_count,
            'total_pages': total_pages,
            'prev': (page_number - 1) if page_number > 1 else None,
            'next': (page_number + 1) if page_number < total_pages else None,
            'results': results,
        }
        return context

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context, safe=False)


class MovieDetailApi(BaseDetailView):
    model = FilmWork

    def get_queryset(self):
        """
        Возвращает аннотированный QuerySet для конкретного фильма.
        """
        base_qs = self.model.objects.filter(pk=self.kwargs['pk'])
        return annotate_filmwork(base_qs)

    def get_context_data(self, **kwargs):
        film = self.get_object()
        context = {
            'id': film.id,
            'title': film.title,
            'description': film.description,
            'creation_date': film.creation_date,
            'rating': film.rating,
            'type': film.type,
            'genres': film.annotated_genres or [],
            'actors': film.actors or [],
            'directors': film.directors or [],
            'writers': film.writers or [],
        }
        return context

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context, safe=False)
