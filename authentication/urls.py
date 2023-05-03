from django.urls import path

from authentication import views
def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('signup/', views.UserSignupView.as_view(), name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('sentry-debug/', trigger_error),
]