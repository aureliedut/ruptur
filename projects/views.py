from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView
from django.views.generic.edit import DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView
from .forms import ProjectForm
from .models import Project
from users.models import User
from users.forms import ContributorForm
from users.views import ContributorUpdate

__all__ = [
    'ProjectUpdate'
]


def contribute(request):
    return render(request, 'projects/contribute.html')


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('contribute')


class ProjectUpdate(UpdateView):
    form_class = ProjectForm
    contrib_form_class = ContributorForm
    queryset = Project.objects
    template_name = 'projects/project_form.html'

    def get_object(self, queryset=None):
        try:
            return super(ProjectUpdate, self).get_object(queryset)
        except AttributeError:
            return None

    def get_success_url(self, **kwargs):
        return reverse_lazy('contribute')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(initial=self.object)
        if 'contribform' not in context:
            city = None
            if (
                self.request.user.id and
                hasattr(self.request.user, 'contributor') and
                self.request.user.contributor.city
            ):
                city = self.request.user.contributor.city

            context['contribform'] = self.contrib_form_class(initial={
                'city': city
            })
        return context

    @staticmethod
    def update_project(project, request):
        for fkattr in [
            'nature',
            'maturity'
        ]:
            if request.POST.get(fkattr):
                setattr(project, fkattr + '_id', request.POST.get(fkattr))

        for attr in [
            'title',
            'description',
        ]:
            if request.POST.get(attr):
                setattr(project, attr, request.POST.get(attr))

        for attr in [
            'tags'
        ]:
            if request.POST.getlist(attr):
                setattr(project, attr, ','.join(request.POST.getlist(attr)))

        project.save()

    def create_project(self, request):
        return Project.objects.create(
            creator=request.user.contributor,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            maturity_id=request.POST.get('maturity'),
            nature_id=request.POST.get('nature'),
            tags=','.join(request.POST.getlist('tags')),
        )

    def post(self, request, **kwargs):
        pk = None

        # Not logged in
        if not request.user.id:
            try:
                # Loggin and redirect
                ContributorUpdate.login(request)
                return HttpResponseRedirect(reverse_lazy('project-form'))

            except User.DoesNotExist:

                # Or create user
                ContributorUpdate.create_user_contributor(request)

        elif hasattr(request.user, 'contributor'):
            # Update user and contributor
            ContributorUpdate.update_contributor(request)
            ContributorUpdate.update_user(request)

        # Create project
        if kwargs.get('pk'):
            pk = kwargs.get('pk')
            self.update_project(self.get_object(), self.request)
        else:
            project = self.create_project(self.request)
            pk = project.pk

        return HttpResponseRedirect(self.get_success_url(pk=pk))


class ProjectDetailView(DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
