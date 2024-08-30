from django.urls import path
from . import views

app_name = 'MITReportInterface'

urlpatterns = [
    # ex: /MITReportInterface
    path("", views.home, name="home"),

    # ex: /MITReportInterface/reportInformation
    path("reportInformation/", views.reportInformation, name="reportInformation"),

    # ex: /MITReportInterface/mit
    path("reportView/", views.reportViewer, name="reportView"),
    path("downloadReport/", views.downloadReport, name="downloadReport"),
    path('web/admin/home/', views.home, name='home'),
    path('web/admin/list/', views.list_merchants, name='list_merchants'),
    path('web/admin/new/', views.new_merchant, name='new_merchant'),
    path('web/admin/test/', views.test_merchant, name='test_merchant'),
    path('web/admin/search/', views.search_transactions, name='search_transactions'),
    path('edit/<int:merchant_id>/', views.edit_merchant, name='edit_merchant'),
    path('delete/<int:merchant_id>/', views.delete_merchant, name='delete_merchant'),
    path('view/<int:merchant_id>/', views.view_merchant, name='view_merchant'),
    path('admin_tools/', views.home, name='admin_tools'),
]
