from django.conf import settings
from django.contrib.auth import mixins
from django.core.mail import send_mail
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import generic


import logging
import functools
import operator

from urllib.parse import urlencode


from .forms import SignUpForm
from .helpers import twitter_api
from .models import User, Favourite, Platform, Genre, Game
from .tokens import account_activation_token_generator


logger = logging.getLogger(__file__)


class IndexView(generic.ListView):
    template_name = 'gamecatalog/home.html'
    context_object_name = 'games'
    model = Game
    paginate_by = 6  # TODO: make pagination

    def __handle_get_filter_params(self, possible_params, qs):
        checked_ids = list()
        for get_param in self.request.GET:
            for possible_param in possible_params:
                if possible_param.slug == get_param:
                    checked_ids.append(possible_param.id)
                    qs[possible_param.slug] = 'on'
        return checked_ids

    def get_queryset(self):

        self.qs = {
            'search': self.request.GET.get('search', ''),
            'rating_from': int(self.request.GET.get('rating_from', 0)),
            'rating_to': int(self.request.GET.get('rating_to', 10)),
        }

        self.platforms = Platform.objects.all()[:20]
        self.checked_platforms_ids = self.__handle_get_filter_params(self.platforms, self.qs)

        self.genres = Genre.objects.all()[:20]
        self.checked_genres_ids = self.__handle_get_filter_params(self.genres, self.qs)

        conditions = list()

        if self.qs.get('search'):
            conditions.append(Q(name__icontains=self.qs.get('search')))

        if self.qs.get('rating_from') and self.qs.get('rating_to'):
            conditions.append(Q(rating__range=(self.qs.get('rating_from'), self.qs.get('rating_to'))))

        if self.checked_platforms_ids:
            conditions.append(Q(platforms__in=self.checked_platforms_ids))

        if self.checked_genres_ids:
            conditions.append(Q(genres__in=self.checked_genres_ids))

        return Game.objects.filter(functools.reduce(operator.and_, conditions)).distinct() if conditions \
            else Game.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context['qs'] = self.qs
        context['filter_params'] = urlencode(self.qs)
        context['platforms'] = self.platforms
        context['checked_platforms_ids'] = self.checked_platforms_ids
        context['genres'] = self.genres
        context['checked_genres_ids'] = self.checked_genres_ids

        return context


class DetailsView(generic.DetailView):
    template_name = 'gamecatalog/details.html'
    context_object_name = 'game'
    model = Game

    def post(self, request, *args, **kwargs):
        try:
            fav_game = self.request.user.favourites(manager='objects').filter(game=self.get_object()).first()
            if fav_game:
                fav_game.is_deleted = False
                fav_game.save()
            else:
                self.request.user.favourites.create(game=self.get_object())
        except IntegrityError as ex:
            return JsonResponse({'success': False, 'message': str(ex)})

        return JsonResponse({'success': True, 'message': "Game was successfully added to favs"})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tweets'] = twitter_api.TWITTER_API.get_tweets_for_game(self.get_object().name)
        return context


class SignUpView(generic.edit.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('gamecatalog:login')
    template_name = 'gamecatalog/sign_up.html'

    def __send_confirmation_mail(self):
        message = render_to_string('gamecatalog/confirmation_email.html', {
            'user': self.object,
            'domain': get_current_site(self.request).domain,
            'upkb64': urlsafe_base64_encode(force_bytes(self.object.pk)),
            'token': account_activation_token_generator.make_token(self.object),
        })

        send_mail('GameMuster account registration', message, settings.EMAIL_HOST_USER, [self.object.email],
                  fail_silently=False)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()
        self.__send_confirmation_mail()

        return HttpResponse('Confirm your email address to activate your acccount.')


class ActivateView(generic.TemplateView):
    template_name = 'gamecatalog/activate.html'

    def post(self, request, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(kwargs['upkb64']))
        except Exception:
            return HttpResponse('Invalid activation link')

        user = User.objects.filter(pk=uid).first()
        token = kwargs['token']

        if user and account_activation_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)

            return redirect('gamecatalog:profile')
        else:
            return HttpResponse('Invalid activation link')


class ProfileView(mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'gamecatalog/profile.html'


class FavouritesView(mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'gamecatalog/favs.html'
    context_object_name = 'favourites'
    model = Favourite
    paginate_by = 1  # TODO: 12

    def get_queryset(self):
        return Favourite.not_deleted_objects.filter(user=self.request.user)


class DeleteRestoreFavsView(generic.View):

    DELETE_SUCCESS_MESSAGE = 'Game was deleted from favs'
    RESTORE_SUCCESS_MESSAGE = 'Game was restored'

    def __action_fav(self, request, game_id, manager, is_deleted_flag, message):
        try:
            fav = request.user.favourites(manager=manager).filter(game__id=game_id).first()
            fav.is_deleted = is_deleted_flag
            fav.save()
        except Exception as ex:
            return JsonResponse({'success': False, 'message': str(ex)})

        return JsonResponse({'success': True, 'message': message})

    def delete(self, request, *args, **kwargs):
        return self.__action_fav(request, kwargs['game_id'], 'not_deleted_objects', True, self.DELETE_SUCCESS_MESSAGE)

    def post(self, request, *args, **kwargs):
        return self.__action_fav(request, kwargs['game_id'], 'objects', False, self.RESTORE_SUCCESS_MESSAGE)
