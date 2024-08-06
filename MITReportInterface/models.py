from django.db import models

class Merchant(models.Model):
    id = models.AutoField(primary_key=True)
    merchant_id = models.CharField(max_length=100, unique=True, default='default_merchant_id')
    orderpage_transaction_type = models.CharField(max_length=20, choices=[("sale", "Sale"), ("authorization", "Authorization")], default='sale')
    test_mode = models.BooleanField(choices=[(True, "Submit Orders to the Cybersource test system."), (False, "Submit Orders to the Cybersource production system.")], default=True)
    disable_captcha = models.BooleanField(default=False)
    disabled = models.BooleanField(default=False)
    cancellation_date = models.DateField(null=True, blank=True)
    secure_acceptance_status = models.CharField(max_length=100, blank=True)
    has_sa_keys = models.BooleanField(default=False)
    has_p12_keys = models.BooleanField(default=False)
    has_soap_keys = models.BooleanField(default=False)
    has_scmp_keys = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    profile_id = models.CharField(max_length=100, blank=True)
    access_key = models.CharField(max_length=100, blank=True)
    confirmation_settings = models.CharField(max_length=100, blank=True)
    pricing_information = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    billing_information = models.CharField(max_length=255, blank=True)
    additional_information = models.CharField(max_length=255, blank=True)

