from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.localflavor.us.models import PhoneNumberField, USStateField

class Catalog(models.Model):
        name = models.CharField(max_length=255)
        slug = models.SlugField(max_length=150)
        publisher = models.CharField(max_length=300)
        description = models.TextField()
        pub_date = models.DateTimeField(default=datetime.now)
        
        def __unicode__(self):
            return u'%s' % self.name

class Product(models.Model):
        category = models.ForeignKey('CatalogCategory',related_name='products')
        name = models.CharField(max_length=300)
        slug = models.SlugField(max_length=150)
        description = models.TextField()
        photo = models.ImageField(upload_to='product_photo',blank=True)
        manufacturer = models.CharField(max_length=300,blank=True)
        price_in_dollars = models.DecimalField(max_digits=6,decimal_places=2)

        def __unicode__(self):
            return u'%s' % self.name

        
        def get_absolute_url(self):
            return '%s/' % (self.slug)
            #return ('product_detail', (), {'slug': self.slug})
            
class CatalogCategory(models.Model):
        catalog = models.ForeignKey('Catalog',related_name='categories')
        parent = models.ForeignKey('self', blank=True, null=True,related_name='children')
        name = models.CharField(max_length=300)
        slug = models.SlugField(max_length=150)
        description = models.TextField(blank=True)
        
        def __unicode__(self):
            if self.parent:
                return u'%s: %s - %s' % (self.catalog.name,
                                     self.parent.name,
                                     self.name)
            return u'%s: %s' % (self.catalog.name, self.name)
        
class ProductDetail(models.Model):

        product = models.ForeignKey('Product',related_name='details')
        attribute = models.ForeignKey('ProductAttribute')
        value = models.CharField(max_length=500)
        description = models.TextField(blank=True)
        
        def __unicode__(self):
            return u'%s: %s - %s' % (self.product,self.attribute,self.value)
        
class ProductAttribute(models.Model):

        name = models.CharField(max_length=300)
        description = models.TextField(blank=True)
        
        def __unicode__(self):
            return u'%s' % self.name




class Order(models.Model):
    '''
    The ``Order`` model represents a customer order. It includes a
    ManyToManyField of products the customer is ordering and stores
    the date and total price information.
    '''
    customer = models.ForeignKey(User, blank=True, null=True)
    status_code = models.ForeignKey('StatusCode')
    date_placed = models.DateTimeField()
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    comments = models.TextField(blank=True)
    products = models.ManyToManyField(Product, through='ProductInOrder')

    def __unicode__(self):
        return u'%s <%s @ %s>' % (self.customer,
                                  self.total_price,
                                  self.date_placed)

class ProductInOrder(models.Model):
    '''
    The ``ProductInOrder`` model represents information about a
    specific product ordered by a customer.
    '''
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField()
    comments = models.TextField(blank=True)

class StatusCode(models.Model):
    '''
    The ``StatusCode`` model represents the status of an order in the
    system.
    '''
    short_name = models.CharField(max_length=10)
    name = models.CharField(max_length=300)
    description = models.TextField()

    def __unicode__(self):
        return u'%s: %s' % (self.short_name, self.name)    

class AmazonTransaction(models.Model):
    '''
    This class maps an Order object to a specific transaction with Amazon
    FPS to track the payment of an order.
    '''
    order = models.ForeignKey(Order)
    transactionId = models.CharField(max_length=500, blank=True)
    status = models.CharField(max_length=300, blank=True)
    
class Rating(models.Model):
    rating = models.IntegerField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    
class TokenReference(models.Model):
    order = models.ForeignKey(Order)
    funding_reference = models.CharField(max_length=128)
    sender_reference = models.CharField(max_length=128)
    transaction_id = models.CharField(max_length=35)

class Customer(models.Model):
    '''
    The ``Customer`` model represents a customer of the online
    store. It wraps Django's built-in ``auth.User`` model, which
    contains information like first and last name, and email, and adds
    phone number and address information.
    '''
    user = models.ForeignKey(User)
    address = models.ForeignKey('CustomerAddress')
    phone_number = PhoneNumberField(blank=True)

class CustomerAddress(models.Model):
    '''
    The ``CustomerAddress`` model represents a customer's address. It
    is slightly biased in favor of US addresses, but should contain
    enough fields to represent addresses in other countries.
    '''
    line_1 = models.CharField(max_length=300)
    line_2 = models.CharField(max_length=300)
    line_3 = models.CharField(max_length=300)
    city = models.CharField(max_length=150)
    postalcode = models.CharField(max_length=10)
    state = USStateField(blank=True)
    country = models.CharField(max_length=150)
        


