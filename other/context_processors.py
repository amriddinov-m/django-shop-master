from marketing.models import Page, Partner
from other.models import Project
from product.models import NewCategory, Product


def pages(request):
        if not 'currency' in request.session:
                print(request.session)
                request.session['currency'] = 'usd'
        else:
                print(request.session['currency'])
        cart = request.session['cart'] if 'cart' in request.session else {}
        cart_products = Product.objects.prefetch_related('photos', 'cat_one') \
                .filter(id__in=[int(k) for k in cart.keys()])
        return {
                'pages': Page.objects.all(),
                'partners': Partner.objects.all(),
                'categories': NewCategory.objects.prefetch_related('parent').all(),
                'random_categories': NewCategory.objects.order_by('?')[:6],
                'ps': Project.objects.first(),
                'cart_products': cart_products
}
