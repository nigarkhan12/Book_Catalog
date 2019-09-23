from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from users.forms import SignUpForm, ProfileForm, ReviewForm
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth.views import LoginView


from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from users.tokens import account_activation_token

from .models import Review
from binder.models import Book
import logging
log = logging.getLogger(__name__)



# Sign Up View
class SignUpView(View):
    form_class = SignUpForm
    template_name = 'commons/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('emails/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, ('Please Confirm your email to complete registration. By copy paste the url from console to browser.'))
            return redirect('login')
        return render(request, self.template_name, {'form': form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('home')
        else:
            messages.warning(request, ('Something went wrong!!!. Please try with Social Authentication'))
            return redirect('login')


# Edit Profile View
class ProfileView(UpdateView):
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('home')
    template_name = 'commons/profile.html'


# Book Review View
def book_reviews(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    context = {
        'book': book,
    }
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ReviewForm(request.POST)
            if form.is_valid():
                new_review = Review.objects.create(
                    user=request.user,
                    book=context['book'],
                    text=form.cleaned_data.get('text')
                )
                new_review.save()
        else:
            if Review.objects.filter(user=request.user, book=context['book']).count() == 0:
                form = ReviewForm()
                context['form'] = form
        context['reviews'] = book.review_set.all()
    return render(request, 'reviews.html', context)


