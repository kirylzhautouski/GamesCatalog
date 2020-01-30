from django.conf import settings
from django.contrib.auth import mixins
from django.core.mail import send_mail
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.db.utils import IntegrityError
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import generic


from requests import HTTPError


from .forms import SignUpForm
from .helpers import igdb_api, twitter_api
from .models import User, GameID
from .tokens import account_activation_token_generator


class IndexView(generic.ListView):
    template_name = 'gamecatalog/home.html'
    context_object_name = 'games'

    def __init__(self):
        super().__init__()

        self.current_page = 1

        self.search_query = ''

        self.rating_from = None
        self.rating_to = None

        self.platforms = igdb_api.IGDB_API.get_all_resources_at_url(
            igdb_api.IGDB_API.PLATFORMS_URL,
            igdb_api.IGDB_API.PLATFORMS_SLUG_COLUMN_NAME)

        self.checked_platforms_ids = None

        self.genres = igdb_api.IGDB_API.get_all_resources_at_url(
            igdb_api.IGDB_API.GENRES_URL,
            igdb_api.IGDB_API.GENRES_COLUMN_NAME)

        self.checked_genres_ids = None

        self.filter_params = ''

    def dispatch(self, request, *args, **kwargs):

        try:
            if 'page' in self.request.GET:
                self.current_page = int(self.request.GET['page'])
        except ValueError:
            raise Http404()

        if not (1 <= self.current_page <= 3):
            raise Http404()

        if 'search' in self.request.GET:
            self.search_query = self.request.GET['search']

            self.filter_params += f'&search={self.search_query}'

        if 'rating_from' in self.request.GET:
            self.rating_from = int(self.request.GET['rating_from'])

            self.filter_params += f'&rating_from={self.rating_from}'

        if 'rating_to' in self.request.GET:
            self.rating_to = int(self.request.GET['rating_to'])

            self.filter_params += f'&rating_to={self.rating_to}'

        self.checked_platforms_ids = self.__handle_get_filter_params(
            self.platforms, igdb_api.IGDB_API.PLATFORMS_SLUG_COLUMN_NAME)

        self.checked_genres_ids = self.__handle_get_filter_params(
            self.genres, igdb_api.IGDB_API.GENRES_COLUMN_NAME)

        return super().dispatch(request, *args, **kwargs)

    def __handle_get_filter_params(self, possible_params, name_key):
        params = set()
        for get_param in self.request.GET:
            for possible_param in possible_params:
                if possible_param[name_key] == get_param:
                    params.add(possible_param['id'])

                    self.filter_params += f'&{get_param}=on'

        return params

    def get_queryset(self):
        games = igdb_api.IGDB_API.get_all_games(
            games_count=18,
            search_query=(self.search_query
                          if self.search_query != '' else None),
            user_rating_range=(self.rating_from, self.rating_to),
            platform_ids=self.checked_platforms_ids,
            genre_ids=self.checked_genres_ids)

        return games[(self.current_page - 1) * 6:
                     (self.current_page - 1) * 6 + 6]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context['current_page'] = self.current_page

        context['search_query'] = self.search_query

        if self.rating_from is not None:
            context['rating_from'] = self.rating_from

        if self.rating_to is not None:
            context['rating_to'] = self.rating_to

        context['platforms'] = self.platforms
        context['checked_platforms_ids'] = self.checked_platforms_ids

        context['genres'] = self.genres
        context['checked_genres_ids'] = self.checked_genres_ids

        context['filter_params'] = self.filter_params

        return context


class DetailsView(generic.TemplateView):
    template_name = 'gamecatalog/details.html'

    def __init__(self):
        super().__init__()

        self.game = {}
        self.is_fav = False
        self.tweets = []

    def dispatch(self, request, *args, **kwargs):
        try:
            self.game = igdb_api.IGDB_API.get_game(kwargs['game_id'])

        except igdb_api.InvalidGameIDError:
            raise Http404()

        user = self.request.user
        if user.is_authenticated and user.gameid_set.filter(game_id=self.game['id']).first():
            self.is_fav = True

        try:
            self.tweets = twitter_api.TWITTER_API.get_tweets_for_game(
                self.game['name'])
        except HTTPError:
            pass

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            self.request.user.gameid_set.create(game_id=self.game['id'])
            self.is_fav = True
        except IntegrityError:
            pass

        return super().get(request, *args, *kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['game'] = self.game
        context['is_fav'] = self.is_fav
        context['tweets'] = self.tweets

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
    context_object_name = 'games'

    def dispatch(self, request, *args, **kwargs):
        try:
            if 'page' in self.request.GET:
                self.current_page = int(self.request.GET['page'])
            else:
                self.current_page = 1
        except ValueError:
            raise Http404()

        if not (1 <= self.current_page <= 3):
            raise Http404()

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        games = igdb_api.IGDB_API.get_games_by_ids(list(self.request.user.gameid_set.values_list('game_id',
                                                                                                 flat=True)))
        if games:
            for game in games:
                game['users_added'] = len(GameID.objects.all().filter(game_id=game['id']))

        return games[(self.current_page - 1) * 12:
                     (self.current_page - 1) * 12 + 12]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = self.current_page
        return context


class SoftDeleteFromFavsView(generic.View):

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'success': True, 'message': 'Game was deleted from favs'})


class RestoreToFavsView(generic.View):

    def post(self, request, *args, **kwargs):
        return JsonResponse({'success': True, 'message': 'Game was restored'})
