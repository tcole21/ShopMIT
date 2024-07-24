from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.template import loader
#from MITReportInterface.getReports import reportLoader
import csv
import os
import xmltodict


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

    downloadedFilePath = os.path.join(os.getcwd(), "resources", "download_report.csv")
    #downloadStatus = reportLoader.download_report(merchant_ID, endDate)

    if downloadStatus == 200:
        with open(downloadedFilePath) as report:
            reportString = report.read()
            reportDict = xmltodict.parse(reportString)

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
    download_file_path = os.path.join(os.getcwd(), "resources", "download_report.csv")

    context = {}
    response = FileResponse(open(download_file_path, 'rb'))
    return response


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
