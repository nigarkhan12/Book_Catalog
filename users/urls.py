from django.urls import path
from django.conf.urls import url
from . import views
from django.views.generic import TemplateView
from .views import SignUpView, ActivateAccount, ProfileView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    url(r'^book/(\d+)', views.book_reviews, name='book_reviews'),

]
