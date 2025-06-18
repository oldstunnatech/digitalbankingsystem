from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Account_table, Transaction_table, Bill_payment
from .forms import Account_Open_form, Change_pin_form, PinAuthentication_form, TransactionHistory_form, Transaction_form, PayBills_form, BillTypeForm
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
import random
from django.contrib import messages
from django.urls import reverse
from userapp.models import Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from transactionapp.models import Account_table
from django.utils import timezone
from django.db.models import F
from django.db import transaction
import json
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from decimal import Decimal
from django.utils.timezone import make_aware
from datetime import datetime, time
from django.utils.timezone import now











# Create your views here.
def is_profile_complete(user):
    profile = user.profile
    return all([profile.address,
    profile.phone_number,
    profile.date_of_birth,
    profile.sex,
    profile.nationality,
    profile.state,
    profile.occupation,
    profile.means_of_identity,
    profile.BVN,
    profile.NIN,
    profile.electricity_bills, 
    profile.profile_passport,
    profile.position,
    profile.marital_status,
    profile.staff,
    profile.user_status])
    



@login_required
def newAccount(request, userId):
    user = User.objects.get(pk=userId)
    if not hasattr(user, "profile") or not user.profile.email or not user.profile.date_of_birth:
        messages.warning(request, "Please complete your profile before creating an account.")
        return redirect('edit_profile', userId=user.id)
    # if not is_profile_complete(request.user):
    #     return redirect('new_account', userId=request.user.id)
    
    if request.method=="POST":
        account_form = Account_Open_form(request.POST)
        if account_form.is_valid():
            add_user = account_form.save(commit=False)
            add_user.user_id = userId
            account = "77"+str(random.randint(00000000, 99999999))
            add_user.account_number=account
            add_user.save()
            my_account = Account_table.objects.all().filter(user_id=userId)
            messages.success(request, ("Your account was successfully created. Thank you!"))
            return render(request, "transactionapp/display_account.html", {"my_account":my_account})
        else:
            messages.error(request, ("Please correct the errrow below."))
            return HttpResponsePermanentRedirect(reverse('new_account', args=(userId,) ))
    else:
        account_form=Account_Open_form()
        return render(request, "transactionapp/account_open_form.html", {"form":account_form})
        

@login_required
def displayAccount(request, userId):
    my_account = Account_table.objects.all().filter(user_id=userId)
    return render(request, "transactionapp/display_account.html", {"my_account":my_account})
    

@login_required
def changePin(request, acctId):
    if request.method=="POST":
        pin_form = Change_pin_form(request.POST)
        if pin_form.is_valid():
            oldpin = pin_form.cleaned_data["oldpin"]
            newpin = pin_form.cleaned_data["newpin"]
            confirm_pin = pin_form.cleaned_data["newpin2"]

            try:
                user_account = Account_table.objects.get(account_id=acctId)
            except Account_table.DoesNotExist:
                messages.error(request, "Account not found.")
                return HttpResponseRedirect(reverse('change_pin', args=(acctId,)))

            if check_password(oldpin, user_account.account_pin):
                if newpin == confirm_pin:
                    user_account.account_pin = make_password(newpin) # ✅ secure PIN save
                    user_account.save(update_fields=["account_pin"])
                    messages.success(request, ("Your account pin updated successfully. Thank You!"))
                    return HttpResponsePermanentRedirect(reverse('my_account', args=(request.user.id,)))
                else:
                    messages.error(request, "New PINs do not match.")
                    return HttpResponsePermanentRedirect(reverse('change_pin', args=(acctId,) ))
            else:
                messages.error(request, "Old PIN is incorrect.")
            return HttpResponseRedirect(reverse('change_pin', args=(acctId,)))
    else:
        pin_form = Change_pin_form()
    return render(request, "transactionapp/account_open_form.html", {"form": pin_form})
        
            
@login_required
def resetPin(request, acctId, userId):
    try:
        account = Account_table.objects.get(account_id=acctId)
        account.account_pin = make_password("0000")  # ✅ Hash the reset PIN
        account.save(update_fields=["account_pin"])  # Save securely
        messages.success(request, "PIN has been reset to default.")
        send_mail(
        "Pin Reset Update", #Subject of the mail
        f"Dear customer your account {account.account_number} pin has been reset successfully. Your new pin is 0000. Please go ahead and change the pin to your preffered secure pin",  #Body of the mail
        "digitalbanking@gmail.com", #From email (sender)
        [account.user.email], #To email (Receiver)
        fail_silently=False, #Handle any erro
        )
    except Account_table.DoesNotExist:
        messages.error(request, "Account not found.")
    return HttpResponsePermanentRedirect(reverse("my_account", args=(userId,)))
    
    # return redirect("some_view_name")  # Replace wi
    # Account_table.objects.filter(account_id=acctId).update(account_pin="0000")
    # account = Account_table.objects.get(account_id=acctId)


    #send email to customer
    

@login_required
def pinAuthentication(request, action):
    account_list = [("", "Select account number"),]
    account_num = Account_table.objects.filter(user_id=request.user.id).values()
    for account in account_num:
        account_list.append((account["account_number"], account["account_number"]))

    if request.method=="POST":
        pin_form = PinAuthentication_form(request.POST, account_list=account_list)

        if pin_form.is_valid():
            acct_number = pin_form.cleaned_data["account_number"]
            entered_pin = pin_form.cleaned_data["account_pin"]
        
            try:
                user_account = Account_table.objects.get(account_number=acct_number)
                if check_password(entered_pin, user_account.account_pin):
                    return HttpResponsePermanentRedirect(reverse('transaction', args = (user_account.account_id, action) ))
                else:
                    messages.error(request, "Invalid PIN entered.")
                
            except Account_table.DoesNotExist:
                messages.error(request, "Account not found.")
        else:
            messages.error(request, "Please correct the form errors below.")
        return render(request, 'transactionapp/pin_auth_form.html', {'pin_form': pin_form,})

    else:
        pin_form = PinAuthentication_form(account_list = account_list)
        return render(request, "transactionapp/pin_auth_form.html", {"pin_form": pin_form,})


@login_required
def userTransaction(request, acctId, action):
    if action == "balance":
        balance = Account_table.objects.filter(account_id=acctId)
        return render(request, "transactionapp/balance_page.html", {"transaction":balance})

    if request.method == "POST":
        tran_form = Transaction_form(request.POST)
        tran_list = {}
        
        try:
            user_info = Account_table.objects.get(account_id = acctId)
        except Exception as e:
            messages.error(request, (f"Account Verification Failed: {e}"))
            return HttpResponsePermanentRedirect(reverse('transaction', args=(acctId, action) ))
        
        if tran_form.is_valid():
            amount = tran_form.cleaned_data.get("amount")

            if action == "transfer":
                tran_list.update({
                    "beneficial_bank": tran_form.cleaned_data.get("beneficiary_bank"),
                    "beneficial_account": tran_form.cleaned_data.get("beneficiary_account"),
                    "amount": amount,
                    "transaction_type": action,
                })

            elif action == "pay_bill":
                tran_list.update({
                    "bill_type": tran_form.cleaned_data.get("bill_type"),
                    "beneficial_bank": tran_form.cleaned_data.get("beneficiary_bank"),
                    "beneficial_account": tran_form.cleaned_data.get("beneficiary_account"),
                    "amount": amount,
                    "transaction_type": action,
                })
            
            elif action == "recharge":
                tran_list.update({
                    "mobile_networks": tran_form.cleaned_data.get("mobile_networks"),
                    "recepient_phone_number": tran_form.cleaned_data.get("recepient_phone_number"),
                    "amount": amount,
                    "transaction_type": action,
                })
            else:
                tran_list.update({
                    "amount": amount,
                    "transaction_type": action,
                })
            transaction_time = timezone.now()
            return render(request, "transactionapp/confirmpage.html", {
                "tran_list": [tran_list],
                "user_info": user_info,
                "transaction_time": transaction_time,
                "url_tran_list": json.dumps(tran_list)
            })
        else:
            messages.error(request, "Failed to process form.")
            return HttpResponsePermanentRedirect(reverse('transaction', args=(acctId, action)))

    else:
        tran_form = Transaction_form()
        return render(request, "transactionapp/transaction_form.html", {
            "trans_form": tran_form,
            "action": action
        })

@login_required
def submitTransaction(request, tran_list, acctId):
    try:
        tran_list = json.loads(tran_list)
    except json.JSONDecodeError as e:
        messages.error(request, (f"Invalid transaction data: {e}"))
        return HttpResponsePermanentRedirect(reverse('transaction', args = (acctId, "deposit")))
    
    with transaction.atomic():
        try:
            account = Account_table.objects.get(account_id=acctId)
            balance = account.account_balance
        except Exception as e:
            messages.error(request, f"Failed to process account balance: {e}")
            return redirect(reverse('transaction', args=(acctId, tran_list.get("transaction_type", "deposit"))))
            
        amount = int(tran_list.get("amount", 0))
        transaction_type = tran_list.get("transaction_type")

        if transaction_type == "deposit":
            Account_table.objects.filter(user_id=request.user.id, account_id=acctId).update(account_balance=F("account_balance") + amount)
            transact = Transaction_table(
                user_id=request.user.id,
                account_id=acctId,
                transaction_amount=amount,
                transaction_type=transaction_type
            )

        else:
            if balance < amount:
                messages.error(request, "Transaction failed due to insufficient balance")
                return redirect(reverse('transaction', args=(acctId, transaction_type)))
            
            if transaction_type == "transfer":
                Account_table.objects.filter(user_id=request.user.id, account_id=acctId).update(account_balance=F("account_balance") - amount)
                transact = Transaction_table(
                    user_id=request.user.id,
                    account_id=acctId,
                    transaction_amount=amount,
                    transaction_type=transaction_type,
                    recepient_bank_name=tran_list.get("beneficial_bank"),
                    recepient_account_number=tran_list.get("beneficial_account"),
                    sender_account_number=account,
                )

            elif transaction_type == "pay_bill":
                Account_table.objects.filter(user_id=request.user.id, account_id=acctId).update(account_balance=F("account_balance") - amount)
                transact = Transaction_table(
                    user_id=request.user.id,
                    account_id=acctId,
                    transaction_amount=amount,
                    transaction_type=transaction_type,
                    recepient_bank_name=tran_list.get("beneficial_bank"),
                    recepient_account_number=tran_list.get("beneficial_account"),
                    bill_type=tran_list.get("bill_type")
                )

            elif transaction_type == "recharge":
                Account_table.objects.filter(user_id=request.user.id, account_id=acctId).update(account_balance=F("account_balance")- amount)
                transact = Transaction_table(
                    user_id=request.user.id,
                    account_id=acctId,
                    transaction_amount=amount,
                    transaction_type=transaction_type,
                    mobile_networks=tran_list.get("mobile_networks"),
                    recepient_phone_number=tran_list.get("recepient_phone_number")
                )

            else:
                Account_table.objects.filter(user_id=request.user.id, account_id=acctId).update(account_balance=F("account_balance") - amount)
                transact = Transaction_table(
                    user_id=request.user.id,
                    account_id=acctId,
                    transaction_amount=amount,
                    transaction_type=transaction_type
                )

        try:
            transact.save()
        except Exception as e:
            messages.error(request, f"Transaction failed: {e}")
            return redirect(reverse('transaction', args=(acctId, transaction_type)))

        last_transaction = Transaction_table.objects.filter(account_id=acctId).order_by("transaction_date").last()
        messages.success(request, "")
        return render(request, "transactionapp/receipt_page.html", {"transaction": [last_transaction]})

            
        


@login_required
def transactionHistory(request, acctId):
    history_form = TransactionHistory_form(request.POST)
    transactions = Transaction_table.objects.filter(account_id=acctId)
    paybills = Bill_payment.objects.filter(account_number=acctId)
    today = now().date()
    combined_history = list(transactions) + list(paybills)

    
    if history_form.is_valid():
        start_date = history_form.cleaned_data["start_date"]
        end_date = history_form.cleaned_data["end_date"]

        start_datetime = make_aware(datetime.combine(start_date, time.min))
        end_datetime = make_aware(datetime.combine(end_date, time.max))
            

        transactions = transactions.filter(transaction_date__range=(start_datetime, end_datetime))
        paybills = paybills.filter(transaction_date__range=(start_datetime, end_datetime))
    else:
        history_form = TransactionHistory_form(initial={"start_date": today, "end_date": today})
    
    combined_history = list(transactions) + list(paybills)    
    combined_history.sort(key=lambda x: x.transaction_date, reverse=True)
    return render(request, "transactionapp/trans_history.html", {
        "combined_history": combined_history,
        "transactions": transaction,
        "paybills": paybills,
        "history_form": history_form,
    })

    #     else:
    #         messages.error(request, "Please enter a valid date range.")
    # else:
    #     history_form = TransactionHistory_form()

    # return render(request, "transactionapp/trans_history.html", {"transactions": transactions, "history_form": history_form})

    #         except Exception as e:
    #             messages.error(request, (f"Failed to process request: {e}"))
    #             return redirect("transactionHistory", acctId=acctId)
    #         else:
    #             messages.error(request, "Invalid form input.")
    #             return redirect("transactionHistory", acctId=acctId)

    # else:
    #     transactions = Transaction_table.objects.filter(account_id=acctId).order_by('-transaction_date')
    #     history_form = TransactionHistory_form()
    #     return render(request, "transactionapp/trans_history.html", {"transactions": transactions, "history_form": history_form})


# def selectBillTypeView(request):
#     if request.method == "POST":
#         form = BillTypeForm(request.POST)
#         if form.is_valid():
#             bill_type = form.cleaned_data['bill_type']
#             return redirect('pay_bill', bill_type=bill_type)  # Route to Step 2
#     else:
#         form = BillTypeForm()
#     return render(request, "transactionapp/select_bill_type.html", {"form": form})


# def bill_form_fields(bill_type):
#     if bill_type == "electricity":
#         return {
#             "label": "Meter Number",
#             "placeholder": "Enter your electricity meter number",
#             "input_type": "text"
#         }
#     elif bill_type == "Cable":
#         return {
#             "label": "Decoder Number",
#             "placeholder": "Enter your decoder number",
#             "input_type": "text"
#         }
#     elif bill_type == "Water Bill":
#         return {
#             "label": "Water ID",
#             "placeholder": "Enter your Water Id",
#             "input_type": "text"
#         }
#     else:
#         return None


@login_required
def payBillsView(request, bill_type):
    
    if request.method=="POST":
        form = PayBills_form(request.POST, bill_type=request.POST.get("bill_type"), user=request.user)
        
        if form.is_valid():
            print(form.errors)
            account_number = form.cleaned_data.get('account_number')
            entered_pin = form.cleaned_data["account_pin"]
            amount = Decimal(form.cleaned_data.get('amount'))

            try:
                account = Account_table.objects.get(account_number = account_number)

                if not check_password(entered_pin,account.account_pin):
                    form.add_error("account_pin", "Incorrect PIN entered.")
                    return render(request, "transactionapp/pay_bill.html", {"form": form, "bill_type": bill_type})

                

            except Account_table.DoesNotExist:
                messages.error(request, "Account not found.")
                return render(request, "transactionapp/pay_bill.html", {"form": form, "bill_type": bill_type})
            
            if account.account_balance < amount:
                messages.error(request, "Insufficient account balance.")
                return render(request, "transactionapp/pay_bill.html", {"form": form, "bill_type": bill_type})

            # Deduct and save    
            account.account_balance -= amount
            account.save()  # save updated balance

            
            bill_payment = form.save(commit=False)
            bill_payment.reference = f"BILL-{uuid.uuid4().hex[:10].upper()}"
            bill_payment.account_number = account
            bill_payment.bill_type = form.cleaned_data.get("bill_type")
            bill_payment.account_type = account.account_type
            bill_payment.amount = amount
            bill_payment.account_balance = account.account_balance
            bill_payment.save()
            print(account.account_balance)

            

            messages.success(request, '')
            return render(request, 'transactionapp/bill_receipt.html', {
                'reference': bill_payment.reference,
                'bill_payment': bill_payment,
                'account_number': bill_payment.account_number,
                'bill_type': bill_payment.get_bill_type_display(),
                'amount': bill_payment.amount,
                'phone_number': bill_payment.phone_number,
                'transaction_date': bill_payment.transaction_date,
                'decoder_number': bill_payment.decoder_number,
                'meter_number': bill_payment.meter_number,
                'months_of_sub': bill_payment.months_of_sub,
                'request_type': bill_payment.request_type,
                'water_service_number': bill_payment.water_service_number,
                'electricity_type': bill_payment.electricity_type,
                'cable_type': bill_payment.cable_type,
                'water_bill_type': bill_payment.water_bill_type,
                'account_type': bill_payment.account_type,
                'account_balance': bill_payment.account_balance
                })
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, "transactionapp/pay_bill.html", {"form": form, "bill_type": bill_type})
             
    else:
        form = PayBills_form(bill_type=bill_type, user=request.user)
        
    return render(request, "transactionapp/pay_bill.html", {"form": form, "bill_type": bill_type,})



@login_required
def get_account_details(request):
    account_number = request.GET.get('account_number')
    account = Account_table.objects.filter(account_number=account_number, user=request.user).first()

    if account:
        data = {
            "account_type": account.account_type,
            "account_balance": str(account.account_balance),
        }
    else:
        data = {"error": "Account not found"}
    return JsonResponse(data)
                
            # STEP 2: Handle full form submission




        # Now show full bill form based on selected type
        # if request.POST.get("amount") is None:
        #     form = PayBills_form(bill_type=bill_type)
        #     form.fields["account_number"].choices = [(acct.account_number, acct.account_number) for acct in accounts]
        #     return render(request, "transactionapp/pay_bill.html", {
        #         "form": form,
        #         "bill_type": bill_type,
        #     })

        # if 'amount' not in request.POST:
            
        #     return render(request, "transactionapp/pay_bill.html", {
        #             "form": form,
        #             "bill_type": bill_type,
        #         })

        
        # bill_type = request.POST.get("bill_type")  # recover bill_type
        # form = PayBills_form(request.POST, bill_type=bill_type)
        # form.fields["account_number"].choices = [(acct.account_number, acct.account_number) for acct in accounts]

        # # Handle actual bill form submission (step 2)
        # if form.is_valid():
        #     selected_account_number = form.cleaned_data["account_number"]

        #     try:
        #         account_number = Account_table.objects.get(account_number = selected_account_number)
        #     except Account_table.DoesNotExist:
        #         messages.error(request, "Invalid account number selected.")
        #         return redirect("PayBillsView")

            


    #     # Step 1: User selected bill type
    #     if 'bill_type' in request.POST and 'amount' not in request.POST:
    #         bill_type_form = BillTypeForm(request.POST)
    #         if bill_type_form.is_valid():
    #             bill_type = bill_type_form.cleaned_data["bill_type"]
    #             form = PayBills_form(bill_type=bill_type)
    #             form.fields["account_number"].choices = [(acct.account_number, acct.account_number) for acct in accounts]
    #             return render(request, "transactionapp/pay_bill.html", {
    #                 "form": form,
    #                 "bill_type": bill_type
    #             })
    #     # bill_type = request.POST.get("bill_type")
    #     # form = PayBills_form(request.POST, bill_type=bill_type)
    #     # form.fields['account_number'].choices = [(acct.account_number, acct.account_number) for acct in accounts]
    
    #         # Step 2: Full bill form submitted

    #     # bill_type = request.POST.get("bill_type")
    #     # print("BILL TYPE IS:", bill_type)

    #     # form = PayBills_form(request.POST, bill_type=bill_type)
    #     # form.fields["account_number"].choices = [(acct.account_number, acct.account_number) for acct in accounts]


    #     if form.is_valid():
    #         selected_account_number = form.cleaned_data["account_number"]
    #         account = Account_table.objects.get(account_number=selected_account_number)
            
    #         bill_payment = form.save(commit=False)
    #         bill_payment.reference = f"BILL-{uuid.uuid4().hex[:10].upper()}"
    #         bill_payment.account_number = account
    #         bill_payment.bill_type = bill_type

    #         # bill_payment.account_id = acctId
    #         bill_payment.save()
            
    #         messages.success(request, 'Bill Payment Successful')
    #         return render(request, 'transactionapp/bill_receipt.html', {
    #             'reference': bill_payment.reference,
    #             'account_number': bill_payment.account_number,
    #             'bill_type': bill_payment.bill_type,
    #             'amount': bill_payment.amount,
    #             'phone_number': bill_payment.phone_number,
    #             'transaction_date': bill_payment.transaction_date,
    #             'decoder_number': bill_payment.decoder_number,
    #             'meter_number': bill_payment.meter_number,
    #             'months_of_sub': bill_payment.months_of_sub,
    #             'request_type': bill_payment.request_type,
    #             })
    #     else:
    #         form = PayBills_form(bill_type=bill_type)
    #         messages.error(request, "Please correct the errors below.")
    #         return render(request, "transactionapp/pay_bill.html", {"form": form})
    # else:
    #     form = BillTypeForm()
    #     return render(request, "transactionapp/pay_bill.html", {"form":form})