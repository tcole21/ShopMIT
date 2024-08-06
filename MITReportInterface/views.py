from django.http import HttpResponse, FileResponse
from django.template import loader
from .reportDownload import process_get
import csv
import os
import xmltodict
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Merchant
from datetime import datetime
from django import forms

# Create your views here.


def index(request):
    template = loader.get_template("MITReportInterface/index.html")
    context = {}
    return HttpResponse(template.render(context, request))


def reportInformation(request):
    template = loader.get_template("MITReportInterface/reportInfo.html")
    merchant_ID = request.GET['merchant_ID']
    context = {
        'merchantID': merchant_ID
    }
    return HttpResponse(template.render(context, request))


def reportViewer(request):
    template = loader.get_template("MITReportInterface/reportView.html")
    context = {
        'ReportHeaders': [],
        'Requests': [],
        'Error_Report': ''
    }

    startDate = request.GET['start_date']
    endDate = request.GET['end_date']
    merchant_ID = request.GET['merchant_ID']

    downloadStatus, reportDict = process_get()


    if downloadStatus == 200:
        if reportDict['Report']['Requests'] is not None:
            for req in reportDict['Report']['Requests']['Request']:
                currentRequest = {}
                currentRequest.update(getMerchantInfo(reportDict['Report']))
                currentRequest.update(getRequestInfo(req))
                currentRequest.update(getBillingInfo(req['BillTo']))
                currentRequest.update(getShippingInfo(req['ShipTo']))
                #currentRequest.update(getCardInfo(req['PaymentMethod']['Card']))
                currentRequest.update(getCardInfo(req.get('PaymentMethod').get('Card')))
                currentRequest.update(getLineItems(req['LineItems']['LineItem']))
                context['Requests'].append(currentRequest)
                context['ReportHeaders'] = list(currentRequest.keys())
        else:
            currentRequest = {}
            currentRequest.update(getMerchantInfo(reportDict['Report']))
            currentRequest.update(getRequestInfo({}))
            currentRequest.update(getBillingInfo({}))
            currentRequest.update(getShippingInfo({}))
            currentRequest.update(getCardInfo({}))
            currentRequest.update(getLineItems({}))
            context['Requests'].append(currentRequest)
            context['ReportHeaders'] = list(currentRequest.keys())

        for i, req in enumerate(context['Requests']):
            for attribute in req.keys():
                if context['Requests'][i][attribute] is None:
                    context['Requests'][i][attribute] = ''

    else:
        context['Error_Report'] = 'An error occured when downloading desired report'

    return HttpResponse(template.render(context, request))

def downloadReport(request):
    pass



# Helper Function To extract merchant info from report
def getMerchantInfo(reportDict):
    merchantInfo = {}

    merchantInfo['Report Name'] = reportDict['@Name']
    merchantInfo['OrganizationID'] = reportDict['@OrganizationID']
    # should I use localized request date

    return merchantInfo


def getRequestInfo(requestDict):
    if requestDict == None:
        requestDict = {}
    requestInfo = {}
    requestInfo['Request Date'] = requestDict.get('@LocalizedRequestDate')
    requestInfo['Request ID'] = requestDict.get('@RequestID')
    requestInfo['Source'] = requestDict.get('@Source')
    requestInfo['Subscription ID'] = requestDict.get('@SubscriptionID')
    #requestInfo.update(getBillingInfo(requestDict['BillTo']))

    return requestInfo


def getBillingInfo(requestDict):
    if requestDict == None:
        requestDict = {}
    billingInfo = {}
    billingInfo['BillTo Address1'] = requestDict.get('Address1')
    billingInfo['BillTo Address2'] = requestDict.get('Address2')
    billingInfo['BillTo City'] = requestDict.get('City')
    billingInfo['BillTo State'] = requestDict.get('State')
    billingInfo['BillTo Company Name'] = requestDict.get('CompanyName')
    billingInfo['BillTo Country'] = requestDict.get('Country')
    billingInfo['BillTo CustomerID'] = requestDict.get('CustomerID')
    billingInfo['BillTo Email'] = requestDict.get('Email')
    billingInfo['BillTo Suffix'] = requestDict.get('NameSuffix')
    billingInfo['BillTo FirstName'] = requestDict.get('FirstName')
    billingInfo['BillTo MiddleName'] = requestDict.get('MiddleName')
    billingInfo['BillTo LastName'] = requestDict.get('LastName')
    billingInfo['BillTo HostName'] = requestDict.get('HostName')
    billingInfo['BillTo IPAddress'] = requestDict.get('IPAddress')
    billingInfo['BillTo Zip'] = requestDict.get('Zip')
    billingInfo['BillTo Phone'] = requestDict.get('Phone')
    billingInfo['BillTo Title'] = requestDict.get('Title')
    billingInfo['BillTo UserName'] = requestDict.get('UserName')
    return billingInfo


def getShippingInfo(requestDict):
    if requestDict == None:
        requestDict = {}
    shippingInfo = {}
    shippingInfo['ShipTo Address1'] = requestDict.get('Address1')
    shippingInfo['ShipTo Address2'] = requestDict.get('Address2')
    shippingInfo['ShipTo City'] = requestDict.get('City')
    shippingInfo['ShipTo Country'] = requestDict.get('Country')
    shippingInfo['ShipTo State'] = requestDict.get('State')
    shippingInfo['ShipTo Zip'] = requestDict.get('Zip')
    shippingInfo['ShipTo Company Name'] = requestDict.get('CompanyName')
    shippingInfo['ShipTo FirstName'] = requestDict.get('FirstName')
    shippingInfo['ShipTo LastName'] = requestDict.get('LastName')
    shippingInfo['ShipToPhone'] = requestDict.get('Phone')
    return shippingInfo


def getCardInfo(requestDict):
    if requestDict == None:
        requestDict = {}
    cardInfo = {}
    cardInfo['Card Type'] = requestDict.get('CardType')
    cardInfo['Card Expiration Month'] = requestDict.get('ExpirationMonth')
    cardInfo['Card Expiration Year'] = requestDict.get('ExpirationYear')
    cardInfo['Card Start Month'] = requestDict.get('StartMonth')
    cardInfo['Card Start Year'] = requestDict.get('StartYear')
    cardInfo['Card Issue Number'] = requestDict.get('IssueNumber')
    cardInfo['Card Account Suffix'] = requestDict.get('AccountSuffix')
    return cardInfo


def getLineItems(requestDict):
    if requestDict == None:
        requestDict = {}
    lineItemInfo = {}
    lineItemInfo['Line Item Number'] = requestDict.get('@Number')
    lineItemInfo['Line Item'] = requestDict.get('FulfillmentType')
    lineItemInfo['Line Item Quantity'] = requestDict.get('Quantity')
    lineItemInfo['Line Item Unit Price'] = requestDict.get('UnitPrice')
    lineItemInfo['Line Item tax amount'] = requestDict.get('TaxAmount')
    lineItemInfo['Line Item SKU'] = requestDict.get('MerchantProductSKU')
    lineItemInfo['Line Item product name'] = requestDict.get('ProductName')
    lineItemInfo['Line Item product code'] = requestDict.get('ProductCode')
    return lineItemInfo


def getReplyInfo(requestDict):
    print(requestDict)
    replyInfo = {}
    replyInfo[''] = requestDict['']

    return replyInfo


def getMerchantDefinedData():
    merchantData = {}

def home(request):
    current_date = datetime.now().strftime("%m/%d/%Y")
    if request.user.is_authenticated:
        user_name = request.user.username
    else:
        user_name = "Guest"

    context = {
        'current_date': current_date,
        'user_name': user_name
    }
    return render(request, 'MITReportInterface/home.html', context)

def list_merchants(request):
    merchants = Merchant.objects.all()
    context = {
        'merchants': merchants,
        'user': request.user,
        'current_date': timezone.now().strftime("%m/%d/%Y"),
    }
    return render(request, 'MITReportInterface/list_merchants.html', context)


class TestMerchantForm(forms.ModelForm):
    class Meta:
        model = Merchant
        fields = [
            'id', 'profile_id', 'access_key', 'confirmation_settings',
            'pricing_information', 'billing_information', 'additional_information'
        ]
        widgets = {
            'id': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'profile_id': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'access_key': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'confirmation_settings': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'pricing_information': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'required': 'required'}),
            'billing_information': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'additional_information': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
        }


def test_merchant(request, merchant_id=None):
    if merchant_id:
        merchant = get_object_or_404(Merchant, pk=merchant_id)
    else:
        merchant = None

    if request.method == 'POST':
        form = TestMerchantForm(request.POST, instance=merchant)
        if form.is_valid():
            form.save()
            return redirect('list_merchants')
    else:
        form = TestMerchantForm(instance=merchant)

    return render(request, 'MITReportInterface/test_merchants.html', {'form': form})


class NewMerchantForm(forms.ModelForm):
    class Meta:
        model = Merchant
        fields = [
            'merchant_id', 'orderpage_transaction_type', 'test_mode', 'disable_captcha'
        ]
        widgets = {
            'merchant_id': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'orderpage_transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'test_mode': forms.Select(choices=[(True, "Test Mode"), (False, "Production Mode")],
                                      attrs={'class': 'form-control'}),
            'disable_captcha': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


def new_merchant(request):
    if request.method == 'POST':
        form = NewMerchantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_merchants')
    else:
        form = NewMerchantForm()

    return render(request, 'MITReportInterface/new_merchant.html', {'form': form})
class SearchForm(forms.Form):
    merchant_id = forms.ChoiceField(
        choices=[
            ("", "-- select merchant --"),
            ("aquame_test", "aquame_test"),
            ("mit_adm_eecs", "mit_adm_eecs"),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'size': 30}),
        required=False
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'size': 30}),
        required=False
    )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control calendar', 'size': 12, 'maxlength': 10}),
        required=False
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control calendar', 'size': 12, 'maxlength': 10}),
        required=False
    )
    amount = forms.DecimalField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'size': 30}),
        required=False
    )
    prod_flag = forms.ChoiceField(
        choices=[("All", "All"), ("Production", "Production"), ("Test", "Test")],
        widget=forms.RadioSelect(),
        required=False
    )
    limit = forms.ChoiceField(
        choices=[
            ("", "..."),
            ("10", "10"),
            ("20", "20"),
            ("50", "50"),
            ("75", "75"),
            ("100", "100"),
            ("200", "200"),
            ("300", "300")
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
def search_transactions(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = SearchForm()

    return render(request, 'MITReportInterface/search_transactions.html', {'form': form})

def edit_merchant(request, merchant_id):
    merchant = get_object_or_404(Merchant, pk=merchant_id)
    return render(request, 'MITReportInterface/edit_merchant.html', {'merchant': merchant})

def delete_merchant(request, merchant_id):
    merchant = get_object_or_404(Merchant, pk=merchant_id)
    if request.method == 'POST':
        merchant.delete()
        return redirect('list_merchants')
    return render(request, 'MITReportInterface/delete_merchant.html', {'merchant': merchant})
def view_merchant(request, merchant_id):
    merchant = get_object_or_404(Merchant, pk=merchant_id)
    return render(request, 'MITReportInterface/view_merchant.html', {'merchant': merchant})
