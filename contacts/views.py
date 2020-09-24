from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from .models import Contact
from .forms import ContactForm, ContactCreateForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import ModelFormMixin, DeleteView, DeletionMixin, BaseDetailView, View
from django.http import Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from taggit.models import Tag


class ListContactView(ListView):
    model = Contact
    template_name = 'contacts/common_list.html'
    context_object_name = 'objects'

    def get_queryset(self, *args, **kwargs):
        queryset = super(ListContactView, self).get_queryset(
            *args, **kwargs)
        queryset = queryset.filter(status='share')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(profession__icontains=query) | Q(author__username=query) | Q(search_tags__name=query))
            queryset = queryset.order_by(
                '-created').filter(status='share').distinct()
        page = self.request.GET.get('page', 1)
        paginator = Paginator(queryset, 4)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(ListContactView, self).get_context_data(
            *args, **kwargs)
        context['featured'] = Contact.objects.all().order_by('-views')[:6]
        print(Tag.objects.all(), 'bmksmakdfmklwsmkl')
        tag = []
        for obj_tag in Tag.objects.all().order_by('name'):
            tag.append(str(obj_tag.name))
        tag = set(tag)  # eliminates duplicates
        tag = list(tag)  # back to list
        tag = sorted(tag)
        # sorting
        context['tags'] = tag

        context['page_obj'] = context['objects']
        return context


class UserDetailListContactView(DetailView):
    model = Contact
    template_name = "contacts/user_list.html"
    context_object_name = 'objects'
    pk_url_kwarg = 'author_id'

    pk_url_kwarg = 'author_id'
    slug_url_kwarg = 'author'

    def get_queryset(self, *args, **kwargs):
        queryset = super(UserDetailListContactView, self).get_queryset(
            *args, **kwargs)

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(profession__icontains=query) | Q(author__username=query) | Q(
                    status=query)).distinct()
            queryset = queryset.order_by('-created')

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='share')
            queryset = queryset.order_by('-created').distinct()
            print(queryset)

        return queryset

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)  # author_id
        slug = self.kwargs.get(self.slug_url_kwarg)  # author_username
        if pk is not None and slug is not None:
            queryset = queryset.filter(author__id=pk).filter(
                author__username=slug)
            print(queryset, 'bibek')

        try:

            page = self.request.GET.get('page', 1)
            paginator = Paginator(queryset, 4)
            try:
                queryset = paginator.page(page)
            except PageNotAnInteger:
                queryset = paginator.page(1)
            except EmptyPage:
                queryset = paginator.page(paginator.num_pages)
            obj = queryset
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailListContactView,
                        self).get_context_data(*args, **kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg)
        user = get_object_or_404(User, pk=pk)
        context['user'] = user
        print(self.queryset)
        context['page_obj'] = self.get_object()
        user_posts_count = user.blog_posts.all()
        if self.request.user.username == user.username:
            context['counts'] = user_posts_count.count()
        else:
            context['counts'] = user_posts_count.filter(
                status='published').count()
        return context


class DetailContactView(DetailView):
    model = Contact
    # form_class = PostCreateForm
    context_object_name = 'objects'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'author_id'
    author_url_kwarg = 'author'
    template_name = "contacts/detail.html"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)  # author_id
        slug = self.kwargs.get(self.slug_url_kwarg)
        author = self.kwargs.get(self.author_url_kwarg)  # author_username
        if pk is not None and slug is not None and author is not None:
            queryset = queryset.filter(author__id=pk).filter(
                author__username=author).filter(slug=slug)
            print(queryset, 'bibek')

        if pk is None and slug is None and author is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        try:
            obj = queryset.get()
            obj.views = obj.views + 1
            obj.save()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class CreateContactView(SuccessMessageMixin, CreateView):
    template_name = 'contacts/create.html'
    form_class = ContactCreateForm
    success_message = 'Contact was created SuccessFully'

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.author = self.request.user
        form.save()
        form.save_m2m()
        return super(CreateContactView, self).form_valid(form)


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class UpdateContactView(SuccessMessageMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'author_id'
    author_url_kwarg = 'author'
    template_name = 'contacts/update.html'
    success_message = 'Contact was Updated successfully'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)  # author_id
        slug = self.kwargs.get(self.slug_url_kwarg)
        author = self.kwargs.get(self.author_url_kwarg)  # author_username
        if pk is not None and slug is not None and author is not None:
            queryset = queryset.filter(author__id=pk).filter(
                author__username=author).filter(slug=slug)
            print(queryset, 'bibek')

        if pk is None and slug is None and author is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.author = self.request.user
        form.save()
        form.save_m2m()
        return super(UpdateContactView, self).form_valid(form)


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class DeleteContactView(View):
    def get(self, request, author_id, slug):
        obj = get_object_or_404(Contact, author__id=author_id, slug=slug)
        obj.delete()
        messages.success(request, 'Contact Successfully Deleted')
        return redirect('contacts:user_post_list', request.user.username, request.user.id)
