from datetime import datetime

from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.db.models import Sum, F
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.utils import translation
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView, ListView, UpdateView

from dsshop.settings import LANGUAGE_CODE
from frontend.forms import SignupForm, LoginForm
from frontend.helpers import calculate_cart, calculate_count_cart
from marketing.models import HotDeal, Certificate, Page, Partner, Review, Banner, Post
from order.models import Deliver, GuestAddress, Order, OrderItem
from product.models import Product, NewCategory, ProductReview
from user.models import UserAddress, User


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.prefetch_related('photos', 'cat_one')
        categories = NewCategory.objects.filter(is_main=True, parent=None)
        context['categories'] = categories.get_descendants(include_self=True)
        context['hot_deals'] = HotDeal.objects.select_related('product'). \
                                   prefetch_related('product__photos', 'product__cat_one') \
                                   .filter(date_end__gte=datetime.now()).order_by('?')[:5]
        context['new_products'] = Product.objects.prefetch_related('photos', 'cat_one').order_by('-id')[:20]
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product-details.html'
    queryset = Product.objects.prefetch_related('photos', 'cat_one')
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['like_products'] = Product.objects.prefetch_related('photos', 'cat_one').order_by('?')[:10]
        context['same_category'] = Product.objects.prefetch_related('photos', 'cat_one').order_by('?')[:10]
        context['comments'] = ProductReview.objects.filter(product=self.object).order_by('-id')[:5]
        return context


class CategoryDetailView(ListView):
    model = Product
    template_name = 'shop-list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        category = NewCategory.objects.get(slug=self.kwargs['slug'])
        context['category'] = category
        context['selected_sort'] = self.request.GET.get('sort', '')
        context['selected_category'] = int(self.request.GET.get('category', '')) \
            if 'category' in self.request.GET and self.request.GET['category'] else None
        context['banner'] = Banner.objects.filter(ad_type='category_page').order_by('?').first()
        context['products_count'] = Product.objects.filter(cat_one__in=[category]).count()
        return context

    def get_queryset(self):
        sort = self.request.GET.get('sort', '')
        cat = NewCategory.objects.get(slug=self.kwargs['slug'])
        filter_cat = self.request.GET.get('category', '')
        if filter_cat:
            products = Product.objects.prefetch_related('cat_one', 'photos').filter(cat_one__id__in=[filter_cat])
        else:
            products = Product.objects.prefetch_related('cat_one', 'photos').filter(cat_one__in=[cat])
        if sort:
            if sort == 'low_to_high':
                products = products.order_by('price')
            else:
                products = products.order_by('-price')
        else:
            products = products.order_by('price')
        return products


class SearchView(ListView):
    model = Product
    template_name = 'search.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        print(self.request.GET.get('sort'))
        context['selected_sort'] = self.request.GET.get('sort', '')
        categories = self.request.GET.getlist('categories')
        print(categories)
        context['selected_categories'] = categories
        context['banner'] = Banner.objects.filter(ad_type='category_page').order_by('?').first()

        return context

    def get_queryset(self):
        sort = self.request.GET.get('sort', '')
        query = self.request.GET.get('query', '')
        categories = self.request.GET.getlist('categories')
        if categories and categories != 'all':
            products = Product.objects.prefetch_related('cat_one', 'photos').filter(cat_one__id__in=categories)
        else:
            products = Product.objects.prefetch_related('cat_one', 'photos')
        if sort:
            if sort == 'low_to_high':
                products = products.order_by('price')
            else:
                products = products.order_by('-price')
        else:
            products = products.order_by('price')
        if query:
            products = products.filter(title_i18n__contains=query)
        return products


class SetLanguage(View):
    def post(self, request):
        language = request.POST.get('language', LANGUAGE_CODE)
        request.session[LANGUAGE_SESSION_KEY] = language
        print(language)
        translation.activate(language)
        return redirect('/{}/'.format(language))


class RegistrationView(TemplateView):
    template_name = 'registration/_signup.html'


class CertificateView(ListView):
    template_name = '_sertificat.html'
    model = Certificate
    queryset = Certificate.objects.all()
    context_object_name = 'certificates'


class PageView(DetailView):
    template_name = '_page.html'
    model = Page
    context_object_name = 'page'


class PartnerView(DetailView):
    template_name = '_page.html'
    model = Partner
    context_object_name = 'page'


class CartView(ListView):
    template_name = 'cart.html'
    model = Product
    context_object_name = 'product'

    def get_queryset(self):
        cart = self.request.session['cart'] if 'cart' in self.request.session else {}
        return Product.objects.prefetch_related('photos', 'cat_one') \
            .filter(id__in=[int(k) for k in cart.keys()])


class ReviewView(ListView):
    template_name = '_reviews.html'
    model = Review

    def post(self, request):
        if 'product' in request.POST:
            ProductReview.objects.create(title=request.POST['title'],
                                         content=request.POST['content'],
                                         user=request.user if not request.user.is_anonymous else None,
                                         product_id=request.POST['product'])
            return redirect('product-detail-frontend', slug=Product.objects.get(pk=request.POST['product']).slug)


class OrderView(TemplateView):
    template_name = '_order.html'

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        cart = self.request.session['cart'] if 'cart' in self.request.session else {}
        context['products'] = Product.objects.prefetch_related('photos', 'cat_one') \
            .filter(id__in=[int(k) for k in cart.keys()])
        context['delivers'] = Deliver.objects.all()
        if self.request.user.is_authenticated:
            context['user_address'] = UserAddress.objects.filter(user=self.request.user).first()
        context['form'] = LoginForm()
        return context

    def post(self, request):
        if request.user.is_anonymous:
            total = 0
            guest_address = GuestAddress()
            guest_address.fullname = request.POST.get('fullname', '')
            guest_address.email = request.POST.get('email', '')
            guest_address.phone = request.POST.get('phone', '')
            guest_address.address = request.POST.get('address', '')
            guest_address.save()
            order = Order()
            order.guest = guest_address
            order.deliver_id = request.POST.get('deliver')
            order.payment_method = request.POST.get('payment_method', 'cod')
            order.save()
            cart = request.session['cart'] if 'cart' in request.session else {}
            products = Product.objects.filter(id__in=[int(k) for k in cart.keys()])
            for product in products:
                oi = OrderItem()
                oi.product = product
                oi.count = cart[str(product.id)]
                if product.discount:
                    if product.discount_type == 'percent':
                        oi.price = product.price - (product.price*product.discount/100)
                    else:
                        oi.price = product.price - product.discount
                else:
                    oi.price = product.price
                total += oi.price * oi.count
                oi.save()
                order.products.add(oi)
            order.total = total
            order.save()

        else:
            region = request.POST.get('region', '')
            phone = request.POST.get('phone', '')
            address = request.POST.get('address', '')
            contact = request.POST.get('contact', '')
            user_addresses = UserAddress.objects.filter(user=request.user, region=region, phone=phone, address=address, contact=contact)
            total = 0
            order = Order()
            if user_addresses.exists():
                order.user_address = user_addresses.first()
            else:
                ua = UserAddress()
                ua.region = region
                ua.phone = phone
                ua.address = address
                ua.contact = contact
                ua.user = request.user
                ua.save()
                order.user_address = ua
            order.user = request.user
            order.deliver_id = request.POST.get('deliver')
            order.payment_method = request.POST.get('payment_method', 'cod')
            order.save()
            cart = request.session['cart'] if 'cart' in request.session else {}
            products = Product.objects.filter(id__in=[int(k) for k in cart.keys()])
            for product in products:
                oi = OrderItem()
                oi.product = product
                oi.count = cart[str(product.id)]
                if product.discount:
                    if product.discount_type == 'percent':
                        oi.price = product.price - (product.price * product.discount / 100)
                    else:
                        oi.price = product.price - product.discount
                else:
                    oi.price = product.price
                total += oi.price * oi.count
                oi.save()
                order.products.add(oi)
            order.total = total
            order.save()
        request.session['order_id'] = order.id
        clear_cart_session(request)
        if order.payment_method == 'online':
            return redirect('payment-view')
        else:
            return redirect('success-view')
        pass


class PaymentView(TemplateView):
    template_name = '_order_payment.html'

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        order_id = self.request.session['order_id']
        context['order'] = Order.objects.select_related('deliver') \
            .prefetch_related('products', 'products__product__photos').get(pk=order_id)
        return context

    def dispatch(self, request, *args, **kwargs):
        if 'order_id' in request.session:
            return super(PaymentView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('/')


class RegisterView(View):
    template_name = 'registration/_signup.html'

    def get(self, request):
        form = SignupForm()
        return render(request, 'registration/_signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create an inactive user with no password:
            user = form.save(commit=False)
            user.is_active = True
            user.save()

            # Uncomment if need mail activation

            # mail_subject = 'Activate your account.'
            # uid = urlsafe_base64_encode(force_bytes(user.pk))
            # token = account_activation_token.make_token(user)
            # activation_link = "{0}/activate/?uid={1}&token={2}".format(get_current_site(request), uid,
            #                                                            token)
            # message = "Hello {0},\n {1}".format(user.email, activation_link)
            # send_verification_email.delay(user.email, mail_subject, message

            # Send an email to the user with the token:

            return redirect('/')
        else:
            print(form.error_messages)
            return render(request, 'registration/_signup.html', {'form': form,
                                                                 'errors': form.error_messages})


class SuccessView(TemplateView):
    template_name = '_success.html'

    def get_context_data(self, **kwargs):
        context = super(SuccessView, self).get_context_data(**kwargs)
        if 'order_id' in self.request.session:
            order_id = self.request.session['order_id']
            context['order'] = Order.objects.prefetch_related('products', 'products__product__photos').get(pk=order_id)
            self.request.session.pop('order_id')
            return context

    def dispatch(self, request, *args, **kwargs):
        if 'order_id' in request.session:
            return super(SuccessView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('/')


class BlogListView(ListView):
    model = Post
    template_name = '_blog_list.html'
    paginate_by = 10


class BlogDetailView(DetailView):
    model = Post
    template_name = '_blog_view.html'
    context_object_name = 'post'


class LoginView(TemplateView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['form'] = LoginForm()
        return context

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if 'back_url' in request.POST:
                        return redirect(request.POST['back_url'])
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')


class ProfileView(DetailView):
    template_name = '_profile.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['user_address'] = UserAddress.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        return self.request.user

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super(ProfileView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('/')


class ProfileEditView(UpdateView):
    template_name = 'registration/update.html'
    model = User
    fields = 'first_name', 'last_name', 'email', 'phone'
    success_url = '/profile/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super(ProfileEditView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('/')

    def get_object(self, queryset=None):
        return self.request.user


class OrderHistoryView(ListView):
    model = Order
    template_name = '_order_history.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super(OrderHistoryView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('/')

    def get_queryset(self):
        return Order.objects.prefetch_related('products').filter(user=self.request.user)


@csrf_exempt
def cart_action(request):
    try:
        cart = request.session['cart'] if 'cart' in request.session else {}
        pk = request.POST['pk'] if 'pk' in request.POST else None
        method = request.POST['method'] if 'method' in request.POST else None

        deleted_elems = []

        if 'cart__set_product' == method and pk:
            quantity = request.POST['quantity'] if 'quantity' in request.POST else ''
            quantity = int(quantity) if quantity.isdigit() else 1
            cart.update({pk: quantity if quantity else 1})
            request.session.__setitem__('cart', cart)
        elif 'cart__plus_product' == method and pk:
            if pk in cart.keys():
                cart.update({pk: int(cart[pk]) + 1})
            else:
                cart[pk] = 1
            request.session.__setitem__('cart', cart)
        elif 'cart__minus_product' == method and pk:
            if int(cart[pk]) - 1 <= 0:
                cart.pop(pk)
                deleted_elems.append(pk)
            else:
                cart.update({pk: int(cart[pk]) - 1})
            request.session.__setitem__('cart', cart)
        elif 'cart__unset_product' == method and pk:
            cart.pop(pk)
            deleted_elems.append(pk)
            request.session.__setitem__('cart', cart)

        elif 'cart__clear_cart' == method:
            request.session.pop('cart')
        total = calculate_cart(cart)
        total_count = calculate_count_cart(cart)
        request.session['total_cart'] = total
        request.session['total_count'] = total_count
        print(cart)
        if request.is_ajax():
            return JsonResponse({
                'status': 'Успех',
                'total': total,
                'cart': cart,
                'deleted': deleted_elems,
                'total_count': total_count
            })
        else:
            return JsonResponse({
                'Ошибка': "Я не знаю в чём дело"
            })
    except Exception as ex:
        print(ex)
        return JsonResponse({
            'Ошибка': str(ex)
        })


@csrf_exempt
def change_currency(request):
    currency = request.POST['currency'] if 'currency' in request.POST else 'sum'
    request.session['currency'] = currency
    return JsonResponse({
        'status': 'Успех'
    })


def clear_cart_session(request):
    request.session.pop('cart')
    request.session.pop('total_cart')
    request.session.pop('total_count')


class TestView(TemplateView):
    template_name = 'test.html'

