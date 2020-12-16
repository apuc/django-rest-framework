from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import FormView
from rest_framework import generics, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import status

from .forms import RegisterForm
from .models import UserProfile
from .serializers import UserSerializer


class HomeView(generic.TemplateView):
    template_name = "html/base.html"


class RegisterAPIView(generics.CreateAPIView):
    """POST /api/register/."""

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, JSONParser]

    def init_from_dict(self, data: dict, photo=None):
        self.username = data.get('username')
        self.email = data.get('email')
        self.password = data.get('password1')
        self.password2 = data.get('password2')
        if photo is not None:
            self.photo = photo
        else:
            self.photo = data.get('photo')

    def post(self, request, *args, **kwargs):
        if len(request.POST) > 1:
            form = RegisterForm(request.POST)
            if form.is_valid():
                photo = request.FILES.get('photo')
                self.init_from_dict(request.POST, photo=photo)
            else:
                return render(request, 'html/register.html', {'form': form})
        else:
            self.init_from_dict(request.data)

        new_user = UserProfile.objects.create(
            username=self.username,
            email=self.email,
            password=self.password,
            photo=self.photo
        )
        return Response({
            'data': UserSerializer(new_user).data,
            'status': status.HTTP_201_CREATED
        })


class RegisterFormView(FormView):
    """GET /register_user/."""

    form_class = RegisterForm
    template_name = 'html/register.html'
    success_url = reverse_lazy('user:home')


class ListUsersAPIView(generics.ListAPIView):
    """GET list_users/."""

    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['username', 'email']


def add_orderings(qs: QuerySet, orderings: str) -> QuerySet:
    orderings = orderings.split(',')
    qs = qs.order_by(*orderings)
    return qs


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list_view(request):
    qs = UserProfile.objects.only(
        'id', 'username', 'email', 'photo'
    )

    if orderings := request.GET.get('ordering'):
        qs = add_orderings(qs, orderings)

    data = []
    for profile in list(qs):
        data.append({
            'id': profile.id,
            'username': profile.username,
            'email': profile.email,
            'photo': profile.photo
        })

    return render(request, 'html/list_users.html', {'data': data})
