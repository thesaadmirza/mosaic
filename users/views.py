from django.views.generic import ListView, DetailView, FormView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import User, Staff, Customer


# Create your views here.
class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'account/profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        if self.request.user.type:
            if self.request.user.type == "S":
                context['profile'] = Staff.objects.filter(user=self.request.user).first()
            else:
                context['profile'] = Customer.objects.filter(user=self.request.user).first()
        else:
            if self.request.user.is_superuser:
                context = self.request.user
        return context
