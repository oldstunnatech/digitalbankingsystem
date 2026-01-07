from django import forms
from .models import Account_table, Bill_payment, Transaction_table
from django.contrib.auth.hashers import check_password 
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now




class Account_Open_form(forms. ModelForm):
    account_pin = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter four digits"}), label="Create PIN", max_length=4)
    account_pin_confirm = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm four digits"}), label="Confirm PIN",  max_length=4)
    class Meta:
        model = Account_table
        fields =[
            "account_type",
            "account_pin",

        ]

class Change_pin_form(forms.Form):
    oldpin = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter Your Old Pin"}), label="Old Pin", max_length=4)
    newpin = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter Your New Pin"}), label="New Pin", max_length=4)
    newpin2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter Your Confirm Pin"}), label="Confirm New Pin", max_length=4)



class PinAuthentication_form(forms.Form):
        def __init__(self, *args, account_list=None, **kwargs):
            super().__init__(*args, **kwargs)
            self.account_list = account_list

            self.fields["account_number"] = forms.ChoiceField(
                required= False, 
                widget = forms.Select({"class": "form-control"}),
                choices = account_list,
                label="",
            )

            self.fields['account_pin'] = forms.CharField(
                widget = forms.PasswordInput(attrs={"placeholder": "Enter Your Pin", "class": "form-control"}),
                label = "",
                required = False,
                max_length=4,
            )


class GeneralChoices(forms.Form):
    bank_name = [
        ("Select Bank", "Select Bank"),
        ("FBN", "FBN"),
        ("FCMB", "FCMB"),
        ("GTB", "GTB"),
        ("UBA", "UBA"),
        ("ZENITH", "ZENITH"),
        ("ACCESS BANK PLC", "ACCESS BANK PLC"),
        ("FIDELITY", "FIDELITY"),
        ("First City Monument Bank", "First City Monument Bank"),
        ("Stanbic IBTC Bank", "Stanbic IBTC Bank"),
        ("Keystone Bank Ltd", "Keystone Bank Ltd"),
        ("Polaris Bank Plc", "Polaris Bank Plc"),
        ("Premium Trust Bank", "Premium Trust Bank"),
        ("Providus Bank Ltd", "Providus Bank Ltd"),
        ("Sterling Bank Plc", "Sterling Bank Plc"),
        ("SunTrust Bank Nigeria Ltd", "SunTrust Bank Nigeria Ltd"),
        ("Union Bank of Nigeria Plc", "Union Bank of Nigeria Plc"),
        ("Unity Bank Plc", "Unity Bank Plc"),
        ("Wema Bank Plc", "Wema Bank Plc"),

    ]   

    bill_choices = [
        ("Electricity", "Electricity"),
        ("Cable", "Cable"),
        ("Water Bill", "Water Bill"),
        
    ] 

    network_choices = [
        ("MTN", "MTN"),
        ("GLO", "GLO"),
        ("AIRTEL", "AIRTEL"),
        ("ETISALAT", "ETISALAT"),
    ] 

    def get_account(request):
        account_list = [("", "Select your account number")]
        # account_number = Account_table.objects.filter(user=user).values()
        account_number = Account_table.objects.all().values()  
        for account in account_number:
            account_list.append((account["account_number"], account["account_number"])) 
        return account_list


class Transaction_form(forms.Form):
    param = GeneralChoices()
    your_account = forms.ChoiceField(choices=param.get_account(), label="", required=False)
    beneficiary_account = forms.CharField(label="Beneficiary Account Number", required=False, max_length=10)
    beneficiary_bank = forms.ChoiceField(choices=param.bank_name, label="", required=False)
    bill_type = forms.ChoiceField(choices=param.bill_choices, label="", required=False)
    amount = forms.IntegerField(widget=forms.TextInput(attrs={"placeholder": "Amount"}), label="")
    recepient_phone_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Number"}), label="", required=False, max_length=11)
    mobile_networks = forms.ChoiceField(choices=param.network_choices, label="", required=False)

# class Transaction_form(forms.ModelForm):
#     class Meta:
#         model = Transaction_table
#         fields = [
#             "account",
#             "transaction_type",
#             "transaction_amount",
#             "recepient_phone_number",
#             "recepient_bank_name",
#             "recepient_account_number",
#             "sender_bank_name",
#             "sender_account_number",
#             "bill_type",
#             "mobile_networks",
#         ]

class TransactionHistory_form(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={"type":"date"}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={"type":"date"}))

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")

        if start and end and start > end:
            raise forms.ValidationError("Start date must be before end date.")


class BillTypeForm(forms.Form):
    

    


    BILL_TYPE_CHOICES = [
        ("Electricity", "Electricity"),
        ("Cable", "Cable"),
        ("Water Bill", "Water Bill"),
    ]
    bill_type = forms.ChoiceField(choices=BILL_TYPE_CHOICES, label="Bill Type")



class PayBills_form(forms. ModelForm):

    class Meta:
        model = Bill_payment
        fields =[
            "bill_type",
            "amount",
            "account_number",
            "electricity_type",
            "cable_type",
            "water_bill_type",
            "meter_number",
            "decoder_number",
            "months_of_sub",
            "request_type",
            "phone_number",
            "water_service_number",
            "account_pin"
            
        #I exlcude the account type and account balance from user input

         ]

    MONTHS_OF_SUB_CHOICES = [(str(i), str(i)) for i in range(1, 13)]

    REQUEST_TYPE_CHOICES = [
        ("New Request", "New Request"),
        ("Renewal", "Renewal"),
    ]

    ELECT_CHOICES =[
        ("", ""),
        ("PHCN", "PHCN"),
        ("IKEJA Electricity", "IKEJA Electricity"),
        ("Abuja Electricity", "Abuja Electricity"),
    ]

    CABLES_CHOICES =[
        ("", ""),
        ("DSTV", "DSTV"),
        ("GOTV", "GOTV"),
        ("Startimes", "Startimes"),
    ]

    WATER_CHOICES =[
        ("", ""),
        ("Nigeria Water Cooperation", "Nigeria Water Cooperation"),
        ("General Waters", "General Waters"),
        ("Lagos Inc", "Lagos Inc"),
    ]

    BILL_TYPE_CHOICES = [
        ("Electricity", "Electricity"),
        ("Cable", "Cable"),
        ("Water", "Water"),
    ]

    meter_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter Meter Number"}), label="Meter Number",required=False, max_length=13)
    decoder_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter Decoder Number"}), label="Decoder Number", required=False, max_length=13)
    water_service_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Water Service Number"}), label="Water Service Number", required=False, max_length=13)
    electricity_type = forms.ChoiceField(choices=ELECT_CHOICES, label="Electricity Type", required=False)
    cable_type = forms.ChoiceField(choices=CABLES_CHOICES, label="Cable Type", required=False)
    water_bill_type = forms.ChoiceField(choices=WATER_CHOICES, label="Water Bill", required=False)
    months_of_sub = forms.ChoiceField(choices=MONTHS_OF_SUB_CHOICES, label="Months", required=False)
    request_type = forms.ChoiceField(choices=REQUEST_TYPE_CHOICES, label="Request Type", required=False)
    bill_type = forms.ChoiceField(choices=Bill_payment.BILL_TYPE_CHOICES, label="Bill Type", required=True)
    

    paramm = GeneralChoices()
    account_number = forms.ModelChoiceField(queryset=Account_table.objects.all(), to_field_name='account_number')
    account_type = forms.CharField(required=False,widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),label='Account Type')
    account_balance = forms.CharField(required=False,widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),label='Account Balance')
    # account_number = forms.ChoiceField(choices=paramm.get_account() or [], label="", required=False)
    account_pin = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "PIN"}), label="Enter account PIN", required=False, max_length=4)
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={"placeholder": "Enter amount", "step": "0.01"}), label="Amount", required=False)
    phone_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter Phone Number"}), label="Phone Number", required=False, max_length=11)

    def __init__(self, *args, **kwargs):
        bill_type = kwargs.pop('bill_type', None)
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.bill_type = bill_type

        if user:
            self.fields['account_number'].queryset = Account_table.objects.filter(user=user)
            # Optionally remove the blank label '--------'
            # self.fields['account_number'].empty_label = None

            # Make account_type and balance read-only (display only)
            # self.fields['account_type'].queryset = Account_table.objects.filter(user=user)
            # self.fields['account_balance'].queryset = Account_table.objects.filter(user=user)
            # self.fields['account_balance'].widget.attrs['readonly'] = True
            # self.fields['account_type'].queryset = Account_table.objects.filter(user=user)
            # self.fields['account_balance'].queryset = Account_table.objects.filter(user=user)
            #This ensures selected_account is an Account_table object, so selected_account.account_pin works.


    def clean(self):
        cleaned_data = super().clean()
        entered_pin = cleaned_data.get('account_pin')
        selected_account = cleaned_data.get('account_number')
        amount = cleaned_data.get('amount')


        if not selected_account:
            self.add_error('account_number', "Please select an account.")

        if not entered_pin:
            self.add_error('account_pin', "PIN is required.")
        else: 
            if selected_account and not check_password(str(entered_pin), selected_account.account_pin):
                self.add_error('account_pin', "Invalid PIN entered.")
        #  Deduct the amount from the user's account balance
        if selected_account and entered_pin and amount:
            if selected_account.account_balance < amount:
                self.add_error('amount', "Insufficient account balance.")

            
        return cleaned_data

    def clean_bill_type(self):
        bill_type = self.cleaned_data.get('bill_type')
        valid_types = dict(Bill_payment.BILL_TYPE_CHOICES).keys()
        if bill_type not in valid_types:
            raise forms.ValidationError("Invalid bill type selected.")
        return bill_type


    def save(self, commit=True):
        instance = super().save(commit=False)
        selected_account = self.cleaned_data['account_number']
        amount = self.cleaned_data.get('amount')
        
        instance.account_type = selected_account.account_type
        instance.account_balance = selected_account.account_balance
        # 💥 Deduct the amount from the user's account balance
        if amount:
            selected_account.account_balance -= amount
            selected_account.save()  # 💾 Save updated balance
        if commit:
            instance.save()
        return instance

       




        #         account = Account_table.objects.get(account_number=selected_account)
        #         if entered_pin != account.account_pin:
        #             self.add_error('account_pin', "Invalid PIN entered.")
        #     except Account_table.DoesNotExist:
        #         raise forms.ValidationError("Account not found.")

        # return cleaned_data





 # Remove all optional fields by default
        # self.fields["meter_number"].widget = forms.HiddenInput()
        # self.fields["decoder_number"].widget = forms.HiddenInput()
        # self.fields["electricity_type"].widget = forms.HiddenInput()
        # self.fields["cable_type"].widget = forms.HiddenInput()
        # self.fields["water_bill"].widget = forms.HiddenInput()

        # Show relevant fields
        # if bill_type == "Electricity":
        #     self.fields["meter_number"].required=True
        #     self.fields["meter_number"].widget = forms.TextInput(attrs={"placeholder": "Enter Meter Number"})

        #     self.fields["electricity_type"].choices = [("", "Select Electricity Type")] + self.ELECT_CHOICES
        #     self.fields["electricity_type"].widget = forms.Select(attrs={"placeholder": "Select Electricity Type"})
        #     self.fields["electricity_type"].required = True

        # elif bill_type == "Cable":
        #     self.fields["decoder_number"].required=True
        #     self.fields["decoder_number"].widget = forms.TextInput(attrs={"placeholder": "Enter Decoder Number"})

        #     self.fields["cable_type"].choices = [("", "Select Cable Type")] + self.CABLES_CHOICES
        #     self.fields["cable_type"].widget = forms.Select(attrs={"placeholder": "Select Cable Type"})
        #     self.fields["cable_type"].required = True

        # elif bill_type == "Water Bill":
        #     self.fields["decoder_number"].required=True
        #     self.fields["decoder_number"].widget = forms.TextInput(attrs={"placeholder": "Enter Decoder Number"})
            
        #     self.fields["water_bill"].choices = [("", "Select Water Bill Type")] + self.WATER_CHOICES
        #     self.fields["water_bill"].widget = forms.Select(attrs={"placeholder": "Enter Service Number"})
        #     self.fields["water_bill"].required = True


# class PayBills_form(forms.ModelForm):

#     MONTHS_OF_SUB_CHOICES = [(str(i), str(i)) for i in range(1, 13)]

#     REQUEST_TYPE_CHOICES = [
#         ("New Request", "New Request"),
#         ("Renewal", "Renewal"),
#     ]

#     ELECT_CHOICES =[
#         ("PHCN", "PHCN"),
#         ("IKEJA Electricity", "IKEJA Electricity"),
#         ("Abuja Electricity", "Abuja Electricity"),
#     ]

#     CABLES_CHOICES =[
#         ("DSTV", "DSTV"),
#         ("GOTV", "GOTV"),
#         ("Startimes", "Startimes"),
#     ]

#     WATER_CHOICES =[
#         ("Nigeria Cooperation", "Nigeria Cooperation"),
#         ("General Waters", "General Waters"),
#         ("Lagos Inc", "Lagos Inc"),
#     ]


#     paramm = GeneralChoices()
    
    
#     account_number = forms.ChoiceField(choices=paramm.get_account() or [], label="", required=False)
#     account_pin = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter Your Pin"}), label="")
#     amount = forms.CharField(widget=forms.TextInput(attrs={"placeholder": ""}), label="Amount")

#     meter_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": ""}), label="Enter Meter Number")
#     decoder_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter Decoder Number"}))
#     electricity_type = forms.ChoiceField(choices=ELECT_CHOICES, label="Electricity Type", required=False)
#     cable_type = forms.ChoiceField(choices=CABLES_CHOICES, label="Cable Type", required=False)
#     water_bill = forms.ChoiceField(choices=WATER_CHOICES, label="water bill", required=False)
    
#     months_of_sub = forms.ChoiceField(choices=MONTHS_OF_SUB_CHOICES, label="Months", required=False)
#     request_type = forms.ChoiceField(choices=REQUEST_TYPE_CHOICES, label="Request Type", required=False)
#     phone_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter Phone Number"}), label="Phone Number")

    
        


#     class Meta:
#         model = Bill_payment
#         fields =[
#             "amount",
#             "electricity_type",
#             "cable_type",
#             "water_bill",
#             "meter_number",
#             "decoder_number",
#             "months_of_sub",
#             "request_type",
#             "phone_number",

#         ]


#     def __init__(self, *args, **kwargs):
#         bill_type = kwargs.pop('bill_type', None)
#         super().__init__(*args, **kwargs)


#         # Remove all optional fields by default
#         self.fields["meter_number"].widget = forms.HiddenInput()
#         self.fields["decoder_number"].widget = forms.HiddenInput()
#         self.fields["electricity_type"].widget = forms.HiddenInput()
#         self.fields["cable_type"].widget = forms.HiddenInput()
#         self.fields["water_bill"].widget = forms.HiddenInput()

#         # Show relevant fields
#         if bill_type == "Electricity":
#             self.fields["meter_number"].required=True
#             self.fields["meter_number"].widget = forms.TextInput(attrs={"placeholder": "Enter Meter Number"})

#             self.fields["electricity_type"].choices = [("", "Select Electricity Type")] + self.ELECT_CHOICES
#             self.fields["electricity_type"].widget = forms.Select(attrs={"placeholder": "Select Electricity Type"})
#             self.fields["electricity_type"].required = True

#         elif bill_type == "Cable":
#             self.fields["decoder_number"].required=True
#             self.fields["decoder_number"].widget = forms.TextInput(attrs={"placeholder": "Enter Decoder Number"})

#             self.fields["cable_type"].choices = [("", "Select Cable Type")] + self.CABLES_CHOICES
#             self.fields["cable_type"].widget = forms.Select(attrs={"placeholder": "Select Cable Type"})
#             self.fields["cable_type"].required = True

#         elif bill_type == "Water Bill":
#             self.fields["decoder_number"].required=True
#             self.fields["decoder_number"].widget = forms.TextInput(attrs={"placeholder": "Enter Decoder Number"})
            
#             self.fields["water_bill"].choices = [("", "Select Water Bill Type")] + self.WATER_CHOICES
#             self.fields["water_bill"].widget = forms.Select(attrs={"placeholder": "Enter Water Service Number"})
#             self.fields["water_bill"].required = True



            

    
            

#     def clean(self):
#         cleaned_data = super().clean()
#         entered_pin = cleaned_data.get('account_pin')
#         selected_account = cleaned_data.get('account_number')

#         if not selected_account:
#             self.add_error('account_number', "Please select an account.")
#         if not entered_pin:
#             self.add_error('account_pin', "PIN is required.")
#         else:
#             try:
#                 account = Account_table.objects.get(account_number=selected_account)
#                 if entered_pin != account.account_pin:
#                     self.add_error('account_pin', "Invalid PIN entered.")
#             except Account_table.DoesNotExist:
#                 raise forms.ValidationError("Account not found.")

#         return cleaned_data
    

    
    


    


