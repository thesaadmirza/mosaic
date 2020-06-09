from django.shortcuts import render

# Create your views here.

# Create your views here.
class BlackListView(ListView, LoginRequiredMixin):
    model = User
    queryset = User.objects.all()
    template_name = 'lenderer/blacklist.html'