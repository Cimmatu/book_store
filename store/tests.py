from django.test import TestCase
from django.urls import reverse
from django.test.client import RequestFactory
from .views import *
from .forms import *
from .models import Product, Customer
from django.test import Client
from django.contrib.auth.models import User, AnonymousUser


class BaseTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.product = Product.objects.create(id=30, name='Book', price=3.99, digital=True)

        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.create_url = reverse('create_product')
        self.edit_url = reverse('edit_product', kwargs={'pk': self.product.id})
        self.delete_url = reverse('delete_product', kwargs={'pk': self.product.id})

        self.client = Client()
        self.client.login(username='xxxx', password='xxxxx')

        self.user = User.objects.create_user(username='username', password='password',
                                        email='email@gmail.com')
        self.anon_user = AnonymousUser

        self.user_valid_data = {'username': 'some_user', 'email': 'pashagurin@gmail.com', 'password1': '07p11g1999',
                           'password2': '07p11g1999'}

        self.user_invalid_data = {'username': '', 'email': 'gmail.com',
                          'password1': 'asdqwef', 'password2': 'password'}

        self.customer = {'user': self.user_valid_data, 'name': 'name', 'email': 'email@gmail.con'}

        self.data = {'name': 'name', 'price': 3.14, 'digital': True}
        self.invalid_data = {'name': '', 'price': 'asdas', 'digital': True}

        return super().setUp()


class RegisterTest(BaseTest):
    def test_register_authenticated_user(self):
        request = self.factory.get(self.register_url)
        request.user = self.user
        response = register_view(request)
        response.client = Client()
        response.client.login(username='client', password='password')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_register_view_method_not_post(self):
        request = self.factory.get(self.register_url)
        request.user = self.anon_user
        response = register_view(request)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(self.register_url)
        self.assertTemplateUsed(response, 'store/register.html')

    def test_register_view_not_valid_form(self):
        request = self.factory.post(self.register_url)
        request.user = self.anon_user
        response = register_view(request)
        form = CreateUserForm(self.user_invalid_data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(form.is_valid())
        response = self.client.get(self.register_url)
        self.assertTemplateUsed(response, 'store/register.html')

    def test_register_view_success(self):
        request = self.factory.post(self.register_url)
        request.user = self.anon_user
        form = CreateUserForm(self.user_valid_data)
        response = register_view(request)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(response.status_code, 302)
        response.client = Client()
        response.client.login(username='username', password='password3')
        self.assertRedirects(response, '/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)


class LoginTest(BaseTest):
    def test_login_authenticated_user(self):
        request = self.factory.get(self.login_url)
        request.user = self.user
        response = login_view(request)
        response.client = Client()
        response.client.login(username='xxxx', password='xxxxx')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_login_view_method_not_post(self):
        request = self.factory.get(self.login_url)
        request.user = self.anon_user
        response = register_view(request)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(self.login_url)
        self.assertTemplateUsed(response, 'store/login.html')

    def test_login_view_success(self):
        request = self.factory.post(self.login_url)
        request.user = self.anon_user
        response = login_view(request)
        self.assertEqual(response.status_code, 302)
        response.client = Client()
        response.client.login(username='username', password='password2')
        self.assertRedirects(response, '/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_login_view_error_message(self):
        request = self.factory.post(self.login_url)
        request.user = self.anon_user
        response = login_view(request)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(self.login_url)
        self.assertTemplateUsed(response, 'store/login.html')


#done
class CreateProductTest(BaseTest):
    def test_product_create_view_method_not_post(self):
        request = self.factory.get(self.create_url)
        response = create_product_view(request)
        self.assertNotEqual(response.status_code, 302)
        response = self.client.get(self.create_url)
        self.assertTemplateUsed(response, 'store/product_form.html')

    def test_product_create_view_form_is_not_valid(self):
        request = self.factory.post(self.create_url, self.data)
        response = create_product_view(request)
        form = ProductForm(self.invalid_data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(form.is_valid())
        response = self.client.get(self.create_url)
        self.assertTemplateUsed(response, 'store/product_form.html')

    def test_create_product_view_success(self):
        request = self.factory.post(self.create_url, self.data)
        response = create_product_view(request)
        form = ProductForm(self.data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(form.is_valid())
        response.client = Client()
        response.client.login(username='username', password='password1')
        self.assertRedirects(response, '/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)


#done
class EditProductTest(BaseTest):
    def test_product_edit_view_method_not_post(self):
        product = Product.objects.create(id=1, name='Book', price=3.99, digital=True)
        edit_url = reverse('edit_product', kwargs={'pk': product.id})
        request = self.factory.get(self.edit_url)
        response = edit_product_view(request, pk=product.id)
        self.assertNotEqual(response.status_code, 302)
        response = self.client.get(edit_url)
        self.assertTemplateUsed(response, 'store/product_form.html')

    def test_edit_product_view_form_is_not_valid(self):
        product = Product.objects.create(id=1, name='Book', price=3.99, digital=True)
        edit_url = reverse('edit_product', kwargs={'pk': product.id})
        request = self.factory.get(self.create_url, self.data)
        response = edit_product_view(request, pk=product.id)
        form = ProductForm(self.invalid_data, instance=product)
        self.assertNotEqual(response.status_code, 302)
        self.assertFalse(form.is_valid())
        response = self.client.get(edit_url)
        self.assertTemplateUsed(response, 'store/product_form.html')

    def test_edit_product_view_success(self):
        product = Product.objects.create(id=1, name='Book', price=3.99, digital=True)
        request = self.factory.post(self.create_url, self.data)
        response = edit_product_view(request, pk=product.id)
        form = ProductForm(self.data, instance=product)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(form.is_valid())
        response.client = Client()
        response.client.login(username='username', password='passwrdo')
        self.assertRedirects(response, '/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)


#done
class DeleteProductTest(BaseTest):
    def test_delete_product_view_success(self):
        request = self.factory.post(self.delete_url)
        response = delete_product_view(request, pk=self.product.pk)
        self.assertEqual(response.status_code, 302)
        response.client = Client()
        response.client.login(username='xxxx', password='xxxxx')
        self.assertRedirects(response, '/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_delete_product_view_cancel(self):
        product = Product.objects.create(id=31, name='Book', price=3.99, digital=True)
        delete_url = reverse('delete_product', kwargs={'pk': product.id})
        request = self.factory.get(self.delete_url)
        response = delete_product_view(request, pk=self.product.pk)
        self.assertNotEqual(response.status_code, 302)
        response = self.client.get(delete_url)
        self.assertTemplateUsed(response, 'store/product_delete.html')

