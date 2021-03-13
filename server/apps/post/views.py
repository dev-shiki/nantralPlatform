from django.views.generic import FormView, View, TemplateView, UpdateView
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import PostForm, PostFormSet
from .models import Post

from apps.group.models import Group
from apps.utils.accessMixins import UserIsAdmin, LoginRequiredAccessMixin


class PostDetailView(LoginRequiredAccessMixin, TemplateView):
    template_name = 'event/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = Post.get_post_by_slug(self.kwargs['post_slug'])
        context['object'] = self.object
        context['group'] = self.object.get_group
        return context


class PostUpdateView(UserIsAdmin, UpdateView):
    template_name = 'event/update.html'
    fields = ['title', 'description',
              'publication_date', 'publicity', 'color', 'image']

    def test_func(self) -> bool:
        self.kwargs['group_slug'] = self.object.get_group.slug
        return super().test_func()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.object.get_group
        context['post'] = self.object
        return context

    def get_object(self, **kwargs):
        return Post.get_post_by_slug(self.kwargs['post_slug'])

    def dispatch(self, request, *args, **kwargs):
        self.object = Post.get_post_by_slug(self.kwargs['post_slug'])
        self.kwargs['group_slug'] = self.object.get_group.slug
        return super().dispatch(request, *args, **kwargs)


class UpdateGroupCreatePostView(UserIsAdmin, FormView):
    """In the context of a group, create a post view."""
    template_name = 'group/event/create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Group.get_group_by_slug(self.kwargs['group_slug'])
        return context

    def form_valid(self, form, **kwargs):
        event = form.save(commit=False)
        event.group = Group.get_group_by_slug(
            slug=self.kwargs['group_slug']).slug
        event.save()
        return redirect('group:create-event', self.kwargs['group_slug'])


class UpdateGroupPostsView(UserIsAdmin, View):
    """In the context of a group, list and update the posts."""
    template_name = 'group/event/planned_edit.html'

    def get_context_data(self, **kwargs):
        context = {}
        context['object'] = Group.get_group_by_slug(kwargs['group_slug'])
        context['posts'] = Post.objects.filter(
            group=kwargs['group_slug'])
        context['form'] = PostFormSet(queryset=context['posts'])
        return context

    def get(self, request, group_slug):
        return render(request, self.template_name, context=self.get_context_data(group_slug=group_slug))

    def post(self, request,  group_slug):
        return edit_posts(request, group_slug)


@login_required
def edit_posts(request, group_slug):
    group = Group.get_group_by_slug(group_slug)
    form = PostFormSet(request.POST)
    if form.is_valid():
        posts = form.save(commit=False)
        # Link each event to the group
        for post in posts:
            post.group = group.slug
            post.save()
        # Delete  missing events
        for event in form.deleted_objects:
            post.delete()
        messages.success(request, 'Annonces  modifies')
        return redirect('group:update-posts', group_slug)
    else:
        messages.warning(request, form.errors)
        return redirect('group:update-posts', group_slug)
