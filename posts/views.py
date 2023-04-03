from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic.edit import CreateView
from .models import MobilePrice, Post, Category, Author, User
from marketing.models import SubscribedEmail
from django.views.generic import View, DetailView
from django.db.models import Q
from django.contrib import messages
from .forms import CommentForm, ContactForm, CreateUserForm, PostForm, AuthorForm
from django.contrib.auth import get_user_model


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


class HomeView(View):
    def get(self, request):
        featured_post = Post.get_featured_post()
        latest_post = Post.get_latest_post()[0:3]
        galleries = Post.get_all_post()[:4]
        context = {'featured_posts': featured_post,
                   'latest_posts': latest_post, 'galleries': galleries}
        return render(request, 'index.html', context)

    def post(self, request):
        featured_post = Post.get_featured_post()
        latest_post = Post.get_latest_post()[0:3]
        email = request.POST.get('email')
        if email:
            if SubscribedEmail.objects.filter(email=email).exists():
                msg = f"This '{email}' email has already Subscribed. No need to Subscribe again."
                context = {'msg': msg, 'featured_posts': featured_post,
                           'latest_posts': latest_post}
                return render(request, 'index.html', context)
            else:
                SubscribedEmail.save_email(email)
                msg = "Thank's for your Subscription. Every updates will be now Notify."
                context = {'msg': msg, 'featured_posts': featured_post,
                           'latest_posts': latest_post}
                return render(request, 'index.html', context)
        return redirect('home')


class BlogView(View):
    def get(self, request):
        article = Post.get_all_post()
        category = Category.get_all_categories()
        category_count = Post.get_category_count()
        latest_post = Post.get_latest_post()[0:3]

        context = {'articles': article, 'categories': category,
                   'category_count': category_count, 'latest_posts': latest_post}
        return render(request, 'blog.html', context)

    def post(self, request):
        article = Post.get_all_post()
        category = Category.get_all_categories()
        category_count = Post.get_category_count()
        latest_post = Post.get_latest_post()[0:3]
        search_query = request.POST.get('search')
        if search_query:
            search_query = article.filter(
                Q(title__icontains=search_query) |
                Q(overview__icontains=search_query)
            ).distinct()
        context = {'articles': article, 'categories': category,
                   'category_count': category_count, 'latest_posts': latest_post, 'search_results': search_query}
        return render(request, 'blog.html', context)


class PostDetailView(DetailView):

    def get(self, request, id):
        post_detail = Post.get_specific_post(id)
        category = Category.get_all_categories()
        latest_post = Post.get_latest_post()[0:3]
        form = CommentForm()
        category_count = Post.get_category_count()
        context = {'form': form, 'post_details': post_detail,
                   'latest_posts': latest_post, 'category_count': category_count, 'categories': category}
        return render(request, 'postdetail.html', context)

    def post(self, request, id):
        article = Post.get_all_post()
        post_detail = Post.get_specific_post(id)
        latest_post = Post.get_latest_post()[0:3]
        category_count = Post.get_category_count()
        search_query = request.POST.get('search')
        form = CommentForm(request.POST)
        post = get_object_or_404(Post, id=id)
        if search_query:
            search_query = article.filter(
                Q(title__icontains=search_query) |
                Q(overview__icontains=search_query)
            ).distinct()

        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': post.pk
            }))

        context = {'form': form, 'articles': article, 'category_count': category_count,
                   'latest_posts': latest_post, 'search_results': search_query, 'post_details': post_detail, }
        return render(request, 'blog.html', context)


class ContactView(View):
    def get(self, request):
        latest_post = Post.get_latest_post()[0:3]
        form = ContactForm()
        context = {'latest_posts': latest_post, 'form': form}
        return render(request, 'contact.html', context)

    def post(self, request):
        footer_post = Post.get_latest_post()[0:3]
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            form.save()
            message = f"Your Messages has sent successfully. Thank You! {name}. We will contact you later."
            form = ContactForm()
            context = {'footer_posts': footer_post,
                       'form': form, 'message': message}
            return render(request, 'contact.html', context)
        context = {'footer_posts': footer_post}
        return render(request, 'contact.html', context)


class RegisterView(View):
    def get(self, request):
        footer_post = Post.get_latest_post()[0:3]
        form = CreateUserForm()
        context = {'form': form, 'footer_posts': footer_post}
        return render(request, 'register.html', context)

    def post(self, request):
        footer_post = Post.get_latest_post()[0:3]
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Hi "{username}" Your account was created Sucessfully.')
            return redirect('login')
        context = {'form': form, 'footer_posts': footer_post}
        return render(request, 'register.html', context)


class MyProfileView(View):
    User = get_user_model()

    def get(self, request, id):
        userdata = get_object_or_404(self.User, id=id)
        form = CreateUserForm(instance=userdata)
        context = {'form': form}
        return render(request, 'myprofile.html', context)

    def post(self, request, id):
        userdata = get_object_or_404(self.User, id=id)
        author = get_author(request.user)
        form = CreateUserForm(request.POST, instance=userdata)

        if form.is_valid():
            form.instance.author = author
            form.save()
            form = CreateUserForm()
            messages.success(
                request, "Your Profile has been Updated Successfully.")
            context = {'form': form}
            return render(request, 'myprofile.html', context)
        context = {'form': form}
        return render(request, 'myprofile.html', context)


class ProfilePictureView(View):
    User = get_user_model()
    model = Author
    template_name = 'myprofilepic.html'
    form_class = AuthorForm

    def get(self, request, id):
        author = get_object_or_404(Author, id=id)
        form = AuthorForm(instance=author)
        context = {'form': form}
        return render(request, 'myprofilepic.html', context)

    def post(self, request, id):
        userdata = get_object_or_404(self.User, id=id)
        author = get_object_or_404(Author, id=id)
        author = get_author(request.user)
        form = AuthorForm(request.POST or None,
                          request.FILES or None, instance=author)
        if form.is_valid():
            form.instance.author = author
            form.save()
            messages.success(
                request, "Your Profile Picture has been Updated Successfully.")
            form = CreateUserForm(instance=userdata)
            context = {'form': form}
            return render(request, 'myprofile.html', context)
        context = {'form': form}
        return render(request, 'myprofile.html', context)


class MyPostView(View):
    def get(self, request, id):
        latest_post = Post.get_latest_post()[0:3]
        article = Post.get_authors_post(author=id)
        context = {'articles': article, 'latest_posts': latest_post}
        return render(request, 'mypost.html', context)


class PostCreateView(CreateView):
    model = Post
    title = 'Upload'
    template_name = 'post_create.html'
    form_class = PostForm

    def get(self, request):
        form = self.form_class
        context = {'title': self.title, 'form': form}
        return render(request, 'post_create.html', context)

    def post(self, request):
        author = get_author(request.user)
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            print('valid')
            form.instance.author = author
            form.save()
            form = self.form_class
            context = {'form': form}
            messages.success(
                request, "Your Post has been uploaded Successfully.")
            return render(request, 'post_create.html', context)
        context = {'title': self.title, 'form': form}
        return render(request, 'post_create.html', context)


class PostUpdateView(View):
    model = Post
    title = 'Update'
    template_name = 'post_create.html'
    form_class = PostForm

    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        form = self.form_class(instance=post)
        context = {'title': self.title, 'form': form}
        return render(request, 'post_create.html', context)

    def post(self, request, id):
        post = get_object_or_404(Post, id=id)
        author = get_author(request.user)
        form = PostForm(request.POST or None,
                        request.FILES or None, instance=post)
        if form.is_valid():
            form.instance.author = author
            form.save()
            form = self.form_class
            form = PostForm()
            messages.success(
                request, "Your Post has been Updated Successfully.")
            context = {'form': form}
            return render(request, 'post_create.html', context)
        context = {'title': self.title, 'form': form}
        return render(request, 'post_create.html', context)


class PostDeleteView(View):
    model = Post
    template_name = 'post_delete.html'

    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        context = {'post': post}
        return render(request, 'post_delete.html', context)

    @staticmethod
    def post(request, id):
        post = get_object_or_404(Post, id=id)
        post.delete()
        return redirect('blog')


class MobilePriceView(View):
    def get(self, request):
        latest_post = Post.get_latest_post()[0:3]
        data = MobilePrice.get_mobileprice()
        context = {'data': data, 'latest_posts': latest_post}
        return render(request, 'mobileprice.html', context)


class resultdistribution(View):
    def get(self, request):
        data = Post.get_authors_post()
        request = 'Respective Result of particular student.'
        message_request = "response of the user and the student"
        respose = "user requested!"
        context = {'data': data, 'messgae': message_request}
        return render(request, 'result.html', context)
