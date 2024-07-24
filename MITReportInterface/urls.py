from django.urls import path

from . import views

app_name = 'MITReportInterface'

urlpatterns = [
    # ex: /MITReportInterface
    path("", views.index, name="index"),

    # ex: /MITReportInterface/reportInformation
    path("reportInformation/", views.reportInformation, name="reportInformation"),

    # ex: /MITReportInterface/mit
    path("reportView/", views.reportViewer, name="reportView"),

    path("downloadReport/", views.downloadReport, name="downloadReport")
]
