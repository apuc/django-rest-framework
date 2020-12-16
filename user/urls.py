from django.urls import path
import user.views as userviews

app_name = 'user'

urlpatterns = [
    path('', userviews.HomeView.as_view(), name='home'),
    path(
        'api/register/',
        userviews.RegisterAPIView.as_view(),
        name='api-register'
    ),
    path(
        'register_user/',
        userviews.RegisterFormView.as_view(),
        name='form-register'
    ),
    path(
        'api/list_users/',
        userviews.ListUsersAPIView.as_view(),
        name='list-users-api'
    ),
    path('list_users/', userviews.user_list_view, name='list-users'),
]
