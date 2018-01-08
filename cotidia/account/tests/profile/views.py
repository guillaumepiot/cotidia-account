from django.urls import reverse

from cotidia.account.models import User
from cotidia.admin.views import (
    AdminCreateView,
    AdminUpdateView,
    AdminDeleteView,
)

from .models import Profile
from .forms import (
    ProfileAddForm,
    ProfileUpdateForm,
)


class ProfileCreate(AdminCreateView):
    model = Profile
    form_class = ProfileAddForm

    def build_success_url(self):
        url_name = "account-admin:user-detail"
        return reverse(url_name, args=[self.user.id])

    def dispatch(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        self.user = User.objects.get(id=user_id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        return context


class ProfileUpdate(AdminUpdateView):
    model = Profile
    form_class = ProfileUpdateForm

    def build_detail_url(self):
        url_name = "account-admin:user-detail"
        return reverse(url_name, args=[self.get_object().user.id])

    def build_success_url(self):
        url_name = "account-admin:user-detail"
        return reverse(url_name, args=[self.get_object().user.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.get_object().user
        return context


class ProfileDelete(AdminDeleteView):
    model = Profile

    def build_success_url(self):
        return reverse("account-admin:user-list")
