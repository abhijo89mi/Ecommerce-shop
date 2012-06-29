from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from cart import *
import hmac, base64, urllib
from datetime import datetime
from django.contrib.sites.models import Site
from django.conf import settings
from django import template
from models import *
from xml.dom.minidom import parseString


def index(request, template_name='index.html'):
    ctx={'product_list' : Product.objects.all()[:8]}
    return render_to_response(template_name, ctx,context_instance=RequestContext(request))


def product_list (request, template_name='products/product_list.html'):
    ctx={'product_list' : Product.objects.all()}
    return render_to_response(template_name, ctx,context_instance=RequestContext(request))

def product_details(request, slug, template_name='products/product_detail.html', ):
    c=Product.objects.get(slug=slug)
    ctx={'product_d' : c}
    return render_to_response(template_name, ctx,context_instance=RequestContext(request))

    
def lookup_object(queryset, object_id=None, slug=None, slug_field=None):
    if object_id is not None:
        obj = queryset.get(pk=object_id)
    elif slug and slug_field:
        kwargs = {slug_field: slug}
        obj = queryset.get(**kwargs)
    else:
        raise Http404
    return obj

def get_shopping_cart(request, cart_class=Cart):
    return request.session.get('cart', None) or cart_class()

def update_shopping_cart(request, cart):
    request.session['cart'] = cart
    
def shopping_cart(request, template_name='orders/shopping_cart.html'):
    '''
    This view allows a customer to see what products are currently in
    their shopping cart.
    '''
    cart = get_shopping_cart(request)
    ctx = {'cart': cart}
    return render_to_response(template_name, ctx,
                              context_instance=RequestContext(request))

def add_to_cart(request, queryset, object_id=None, slug=None,
                slug_field='slug', template_name='orders/add_to_cart.html'):
    '''
    This view allows a customer to add a product to their shopping
    cart. A single GET parameter can be included to specify the
    quantity of the product to add.
    '''
    obj = lookup_object(queryset, object_id, slug, slug_field)
    quantity = request.GET.get('quantity', 1)
    cart = get_shopping_cart(request)
    cart.add_item(obj, quantity)
    update_shopping_cart(request, cart)
    ctx = {'object': obj, 'cart': cart}
    return render_to_response(template_name, ctx,
                              context_instance=RequestContext(request))

def remove_from_cart(request, cart_item_id,
                     template_name='orders/remove_from_cart.html'):
    '''
    This view allows a customer to remove a product from their shopping
    cart. It simply removes the entire product from the cart, without
    regard to quantities.
    '''
    cart = get_shopping_cart(request)
    cart.remove_item(cart_item_id)
    update_shopping_cart(request, cart)
    ctx = {'cart': cart}
    return render_to_response(template_name, ctx,
                              context_instance=RequestContext(request))

def checkout(request, template_name='orders/checkout.html'):
    '''
    This view presents the user with an order confirmation page and
    the final "order" button to process their order through a checkout
    system.
    '''
    cart = get_shopping_cart(request)
    googleCart, googleSig = doGoogleCheckout(cart)
    ctx = {'cart': cart,
           'googleCart': googleCart,
           'googleSig': googleSig,
           'googleMerchantKey': settings.GOOGLE_MERCHANT_KEY,
           'googleMerchantID': settings.GOOGLE_MERCHANT_ID}
    return render_to_response(template_name, ctx,
                              context_instance=RequestContext(request))
def urlquote(string): 
    # urllib.quote (doesn't do _.-) 
    s = urllib.quote(str(string), '') 
    s = s.replace('.','%2E') 
    s = s.replace('_', '%5F') 
    s = s.replace('-', '%2D') 
    return s

class CheckoutView(object):
    template = 'payments/checkout.html'
    extra_context = {}
    cart_class = Cart
    results = []
    request = None
    form = None
    form_class = None
    order = None
'''
    def __init__(self, template=None, form_class=CheckoutForm,
                 context_class=RequestContext):
        self.context_class = context_class
        self.form_class = form_class
        if template is not None:
            self.template = template

    def __unicode__(self):
        return self.__class__.__name__

    def get_shopping_cart(self):
        if self.request is None:
            raise AttributeError("Cannot get cart for non-existent request")
        return self.request.session.get('cart', None) or self.cart_class()

    def __call__(self, request):
        self.request = request
        if self.request.method == 'POST':
            self.form = self.form_class(request.POST)
        else:
            self.form = self.form_class()
        self.save_order()
        return self.return_response()

    def return_response(self):
        context = {'cart': self.cart, 'form': self.form}
        context.update(self.get_extra_context())
        return render_to_response(
            self.template, context,
            context_instance=self.context_class(self.request))

    def save_order(self):
        cart = self.get_shopping_cart()        
        self.order = make_order_from_cart(order, customer=self.request.user)

    def get_extra_context(self):
        return self.extra_context
'''
class GoogleCheckoutXMLView(CheckoutView):
    google_cart_template = 'payments/googlecheckout.xml'
    merchant_key = getattr(settings, 'GOOGLE_MERCHANT_KEY', '')
    merchant_id = getattr(settings, 'GOOGLE_MERCHANT_ID', '')

    def convert_shopping_cart(self):
        cart = self.get_shopping_cart()
        cart_cleartext = render_to_string(self.google_cart_template,
                                          {'cart': cart})
        cart_sig = hmac.new(self.merchant_key, cart_cleartext, sha).digest()
        cart_base64 = base64.b64encode(cart_cleartext)
        sig_base64 = base64.b64encode(cart_sig)
        self.extra_context.update({'googleCart': cart_base64,
                                   'googleSig': sig_base64})

    def return_response(self):
        self.convert_shopping_cart()
        return super(CheckoutView, self).return_response()

class GoogleCheckoutHTMLView(CheckoutView):
    google_cart_template = 'payments/googlecheckout.html'
    merchant_key = getattr(settings, 'GOOGLE_MERCHANT_KEY', '')
    merchant_id = getattr(settings, 'GOOGLE_MERCHANT_ID', '')

    def convert_shopping_cart(self):
        cart = self.get_shopping_cart()
        checkout_form = render_to_string(self.google_cart_template,
                                         {'cart': cart})
        self.extra_context.update({'checkout_form': checkout_form})

    def return_response(self):
        self.convert_shopping_cart()
        return super(CheckoutView, self).return_response()
'''      
class AmazonCheckoutView(CheckoutView):
    endpoint = 'https://authorize.payments-sandbox.amazon.com/cobranded-ui/actions/start'
    aws_access_key = getattr(settings, 'AWS_ACCESS_KEY', None)
    aws_secret_key = getattr(settings, 'AWS_SECRET_KEY', None)
    currency_code = 'USD'
    default_aws_params = {'currencyCode': 'USD',
                          'paymentMethod': 'ABT,ACH,CC',
                          'version': '2009-01-09',
                          'pipelineName': 'SingleUse'}

    def create_reference(self):
        if self.order:
            return self.order.id
        raise AttributeError("No order exists for this view.")

    def make_signature(self, params):
        path = u'%s?' % self.endpoint
        keys = params.keys()
        keys.sort()

        sign_string = path
        for key in keys:
            sign_string += '%s=%s&' % (urlquote(k), urlquote(params[k]))
        sign_string = sign_string[:-1]
        sig = hmac.new(self.aws_secret_key, sign_string, sha).digest()
        return base64.b64encode(sig)

    def convert_shopping_cart(self):
        # documented at http://docs.amazonwebservices.com/AmazonFPS/2008-09-17/FPSGettingStartedGuide/
        cart = self.get_shopping_cart()
        site = Site.objects.get_current()
        params = dict(self.default_aws_params)
        caller_reference = self.create_reference()
        callback_path = reverse('amazon_callback',
                                kwargs={'reference': callerReference})
        callback_url = 'http://%s%s' % (site.domain,
                                           callback_path)

        params.update({'callerKey': self.aws_access_key,
                       'callerReference': caller_reference,
                       'paymentReason': 'Purchase from %s' % site.name,
                       'returnURL': callback_url,
                       'transactionAmount': cart.total()})
        signature = self.make_signature(params)
        params.update({'signature': signature,
                       'signatureMethod': 'HmacSHA256',
                       'signatureVersion': '2'})
        urlstring = urllib.urlencode(params)
        aws_request = '%s?%s' (self.endpoint, urlstring)
        self.extra_context.update({'requestUrl': aws_request})

def get_order_by_reference(reference):
    return Order.objects.get(id=reference)

def save_amazon_transaction(order, token, status):
    try:
        transaction = AmazonTransacion.objects.get(order=order)
    except AmazonTransaction.DoesNotExist:
        transaction = AmazonTransaction.objects.create(order=order)
    transaction.token = token
    transaction.status = status
    transaction.save()
        
def amazon_callback(request, reference,
                    template_name='payments/amazon_complete.html'):
    order = get_order_by_reference(reference)
    token = request.GET['tokenId']
    status = request.GET['status']
    # save the Amazon FPS token for this order to the database
    save_amazon_transaction(order, token, status)
    return render_to_response(template_name, {},
                              context_instance=RequestContext(request))
                              
def verify_googlecheckout(view_func):
   
    def _verified_view_func(request, *args, **kwargs):
        merchant_key = getattr(settings, 'GOOGLE_MERCHANT_KEY', None)
        merchant_id = getattr(settings, 'GOOGLE_MERCHANT_ID', None)    
        b64string = request.META.get('Authorization', None)
        if b64string:
            cleartext = base64.b64decode(b64string)
            auth_id, auth_key = cleartext.split(":")
            if auth_id != merchant_id or auth_key != merchant_key:
                raise Http404
            return view_func(request, *args, **kwargs)
        else:
            raise Http404
    return _verified_view_func(request, *args, **kwargs)

def get_notification_type(xmldoc):
    return xmldoc.documentElement.tagName

def get_private_data(xmldoc, private_data_tag='merchant-private-data'):
     return xmldoc.documentElement.getElementsByTagName(private_data_tag)[0]

def get_order_id(xmldoc, order_tag='django-order-id'):
    private_data = get_private_data(xmldoc)
    order_id = private_data.getElementsByTagName(order_tag)[0]
    return order_id.nodeValue

def set_status_code(order, status):
    status, created = StatusCode.objects.get_or_create(short_name=status)
    order.status_code = status

@verify_googlecheckout
def notification_callback(request):
   
    if request.method is not 'POST':
        raise Http404
    dom = parseString(request.raw_post_data)
    notify_type = get_notification_type(dom)
    if notify_type is 'new-order-notification':
        order_id = get_order_id(dom)
        order = Order.objects.get(id=order_id)
        set_status_code(order, 'NEW_CHKOUT')
        return HttpResponse('OK')
    raise Http404
def sender_reference(user):
    return '%s_%s' % (user.username, datetime.now())

def funding_reference(order):
    return '%s' % order.pk

def make_order(user, amount):
    # Create an Order object for this user's aggregated payments purchase
    return Order(customer=user, total_price=amount,
                 status_code=get_status_code("NEW"))

def cbui_redirect(request, amount=25.00, pay_type='prepaid'):
    order = make_order(request.user, amount)
    caller_sender_reference = sender_reference(request.user)
    caller_funding_reference = funding_reference(order)
    TokenReference.objects.create(order=order,
                                  sender_reference=caller_sender_reference,
                                  funding_reference=caller_funding_reference)
    if pay_type is 'prepaid':
        redirect_url = get_prepaid_token(
            caller_sender_reference,
            caller_funding_reference,
            amount,
            reverse('cbui_return'))
    elif pay_type is 'postpaid':
        redirect_url = get_postpaid_token(
            caller_sender_reference,
            caller_funding_reference,
            amount,
            reverse('cbui_return'))
    else:
        raise ValueError
    return HttpResponseRedirect(redirect_url)

def cbui_return(request):
    pass
'''
