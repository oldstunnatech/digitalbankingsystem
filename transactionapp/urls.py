from django.urls import path, re_path
from transactionapp import views as tran_view
from userapp import views as trans_view

urlpatterns = [
    re_path(r'^new_account/(?P<userId>\d+)/', tran_view.newAccount, name="new_account"),
    re_path(r'^my_account/(?P<userId>\d+)/', tran_view.displayAccount, name="my_account"),
    re_path(r'^edit_profile/(?P<userId>\d+)/', trans_view.edit_profile, name= "edit_profile"),
    re_path(r'^change_pin/(?P<acctId>\d+)', tran_view.changePin, name="change_pin"),
    re_path(r'^reset_pin/(?P<acctId>\d+)/(?P<userId>\d+)/', tran_view.resetPin, name="reset_pin"),
    re_path(r'^pin_auth/(?P<action>\w+)/', tran_view.pinAuthentication, name="pin_auth"),
    re_path(r'^transaction/(?P<acctId>\d+)/(?P<action>\w+)/', tran_view.userTransaction, name="transaction"),
    path("submit_transaction/<str:tran_list>/<int:acctId>/", tran_view.submitTransaction, name="submit_transaction"),
    re_path(r'^transaction_history/(?P<acctId>\d+)/', tran_view.transactionHistory, name="transaction_history"),
    # re_path(r'^pay_bill/(?P<acctId>\d+)/', tran_view.payBillsView, name="pay_bill")
    # path('pay_bill/<int:acctId>/', tran_view.payBillsView, name='pay_bill'),
    # path("pay/select/", tran_view.selectBillTypeView, name="select_bill_type"),
    path("pay/<str:bill_type>/", tran_view.payBillsView, name="pay_bill"),
    path("account-details/", tran_view.get_account_details, name="get_account_details"),


]