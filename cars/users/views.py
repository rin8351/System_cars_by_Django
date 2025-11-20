from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth.views import LoginView, PasswordChangeView
from users.forms import LoginUserForm, ProfileUserForm, UserPasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse('index')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'users/profile.html'
    form_class = ProfileUserForm
    extra_context = {'title': 'Profile'}
    success_url = reverse_lazy('profile')

    def get_success_url(self):
        return reverse_lazy('users:profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    

class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'
