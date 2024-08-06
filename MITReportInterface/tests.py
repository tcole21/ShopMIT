from django.test import TestCase
from django.urls import reverse
from .models import Merchant

class MerchantServicesTests(TestCase):
    def setUp(self):
        self.merchant1 = Merchant.objects.create(id=1, disabled=False, cancellation_date=None, secure_acceptance_status='Active', has_sa_keys=True, has_p12_keys=True, has_soap_keys=True, has_scmp_keys=True, notes='Test note 1')
        self.merchant2 = Merchant.objects.create(id=2, disabled=True, cancellation_date=None, secure_acceptance_status='Inactive', has_sa_keys=False, has_p12_keys=False, has_soap_keys=False, has_scmp_keys=False, notes='Test note 2')

    def test_list_merchants_view(self):
        response = self.client.get(reverse('list_merchants'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<tr>', count=3)  # 1 header row + 2 data rows
        self.assertIn('background-color: #f9f9f9;', response.content.decode())
        self.assertIn('background-color: #ffffff;', response.content.decode())

    def test_table_structure(self):
        response = self.client.get(reverse('list_merchants'))
        content = response.content.decode()
        self.assertIn('<th>Actions</th>', content)
        self.assertIn('<th>Merchant ID</th>', content)
        self.assertIn('<th>Disabled</th>', content)
        self.assertIn('<th>Cancellation Date</th>', content)
        self.assertIn('<th>Secure Acceptance Status</th>', content)
        self.assertIn('<th>Has SA Keys</th>', content)
        self.assertIn('<th>Has P12 Keys</th>', content)
        self.assertIn('<th>Has SOAP Keys</th>', content)
        self.assertIn('<th>Has SCMP Keys</th>', content)
        self.assertIn('Test note 1', content)
        self.assertIn('Test note 2', content)

    def test_view_merchant_view(self):
        response = self.client.get(reverse('view_merchant', args=[self.merchant1.id]))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, '/accounts/login/?next=/')
