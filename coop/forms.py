import xlrd
from django.utils import timezone
from django import forms
from os.path import splitext
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms.formsets import formset_factory, BaseFormSet

from conf.utils import bootstrapify, internationalize_number, PHONE_REGEX
from coop.models import *
from conf.models import District, SubCounty, Village, Parish, PaymentMethod

class CooperativeForm(forms.ModelForm):
    class Meta:
        model = Cooperative
        fields = ['name', 'logo', 'district', 'sub_county', 'phone_number', 'address', 'contact_person_name',
                  'product', 'is_active', 'send_message']
    
    def clean(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            try:
                phone_number = internationalize_number(phone_number)
                self.cleaned_data['phone_number'] = phone_number
            except ValueError:
                raise forms.ValidationError("Please enter a valid phone number.'%s' is not valid" % phone_number)
        return self.cleaned_data
        

class CooperativeUploadForm(forms.Form):
    
    sheetChoice = (
        ('1','sheet1'),
        ('2','sheet2'),
        ('3','sheet3'),
        ('4','sheet4'),
        ('5','sheet5'),
    )
    
    rowchoices = (
        ('1', 'Row 1'),
        ('2', 'Row 2'),
        ('3', 'Row 3'),
        ('4', 'Row 4'),
        ('5', 'Row 5')
        )
    
    choices = list()
    for i in range(65, 91):
        choices.append([i-65, chr(i)])

    
    excel_file = forms.FileField()
    sheet = forms.ChoiceField(label="Sheet", choices=sheetChoice, widget=forms.Select(attrs={'class':'form-control'}))
    row = forms.ChoiceField(label="Row", choices=rowchoices, widget=forms.Select(attrs={'class':'form-control'}))
    cooperative_col = forms.ChoiceField(label='Cooperative Column', initial=0, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Cooperative')
    district_col = forms.ChoiceField(label='District Column', initial=1, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the District')
    sub_county_col = forms.ChoiceField(label='Sub County Column', initial=2, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Sub County')
    contact_person = forms.ChoiceField(label='Contact Person Column', initial=3, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text="The column contains the Name of the Contact Person")
    phone_number = forms.ChoiceField(label='Phone Number Column', initial=4, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text="The column contains the Phone Number of Cooperative")
    
    
    def clean(self):
        data = self.cleaned_data
        f = data.get('excel_file', None)
        ext = splitext(f.name)[1][1:].lower()
        if not ext in ["xlsx", "xls"]:
            raise forms.ValidationError(("the File type is not accepted"))
        return data
            

class CooperativeSharePriceForm(forms.ModelForm):
    class Meta:
        model = CooperativeSharePrice
        exclude = ['created_by', 'create_date', 'update_date']
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CooperativeSharePriceForm, self).__init__(*args, **kwargs)
        if not self.request.user.profile.is_union():
            self.fields['cooperative'].widget=forms.HiddenInput()
            self.fields['cooperative'].initial=self.request.user.cooperative_admin.cooperative
        

class AnimalIdentificationForm(forms.ModelForm):
    class Meta:
        model = AnimalIdentification
        exclude = ['create_date', 'update_date']


class TickControlForm(forms.ModelForm):
    class Meta:
        model = TickControl
        exclude = ['create_date', 'update_date']
    

class MemberProfileForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MemberProfileForm, self).__init__(*args, **kwargs)
        
        self.fields['parish'].queryset = Parish.objects.none()
        
        if 'sub_county' in self.data:
            try:
                sub_county_id = int(self.data.get('sub_county'))
                self.fields['parish'].queryset = Parish.objects.filter(sub_county=sub_county_id).order_by('name')
                print Parish.objects.filter(sub_county=sub_county_id).order_by('name')
            except Exception as e: #(ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            if self.instance.sub_county:
                self.fields['parish'].queryset = self.instance.sub_county.parish_set.order_by('name')
            
        if not self.request.user.profile.is_union():
            self.fields['cooperative'].widget=forms.HiddenInput()
            self.fields['cooperative'].initial=self.request.user.cooperative_admin.cooperative
           
            
    class Meta:
        model = CooperativeMember
        exclude = ['created_by', 'create_date', 'update_date', 'member_id']
    
    def clean(self):
        phone_number = self.cleaned_data.get('phone_number')
        other_phone_number = self.cleaned_data.get('other_phone_number')
        
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth:
            if date_of_birth > timezone.now().date():
                raise forms.ValidationError("Error! Date of Birth cannot be in the Future")
        
        if phone_number:
            try:
                phone_number = internationalize_number(phone_number)
                self.cleaned_data['phone_number'] = phone_number
            except ValueError:
                raise forms.ValidationError("Please enter a valid phone number.'%s' is not valid" % phone_number)
        if other_phone_number:
            try:
                other_phone_number = internationalize_number(other_phone_number)
                self.cleaned_data['other_phone_number'] = other_phone_number
            except ValueError:
                raise forms.ValidationError("Please enter a valid phone number.'%s' is not valid" % other_phone_number)
        return self.cleaned_data


class MemberProfileSearchForm(forms.Form):
    choices=(('', 'Role'), ('Chairman', 'Chairman'), ('Vice Chairman', 'Vice Chairman'), ('Treasurer', 'Treasurer'),
        ('Secretary', 'Secretary'), ('Member', 'Member'),('Secretary Manager', 'Secretary Manager'), ('Patron', 'Patron'))
        
    name = forms.CharField(max_length=150, required=False)
    phone_number = forms.CharField(max_length=150, required=False)
    cooperative = forms.ChoiceField(widget=forms.Select(), choices=[], required=False)
    role = forms.ChoiceField(widget=forms.Select(), choices=choices, required=False)
    district = forms.ChoiceField(widget=forms.Select(), choices=[], required=False)
    
    def __init__(self,  *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super (MemberProfileSearchForm, self).__init__(*args, **kwargs)
       
        qs = CooperativeMember.objects.values('cooperative__id', 'cooperative__name').distinct()
        d_qs = CooperativeMember.objects.values('district__id', 'district__name').distinct()
        choices = [['', 'Cooperative']]
        dchoices = [['', 'District']]
        for q in qs:
            choices.append([q['cooperative__id'], q['cooperative__name']])
        
        for dq in d_qs:
            dchoices.append([dq['district__id'], dq['district__name']])
            
        self.fields['cooperative'].choices = choices
        self.fields['district'].choices = dchoices
        if not self.request.user.profile.is_union():
            self.fields.pop('cooperative')
    

class MemberUploadForm(forms.Form):
    
    sheetChoice = (
        ('1','sheet1'),
        ('2','sheet2'),
        ('3','sheet3'),
        ('4','sheet4'),
        ('5','sheet5'),
    )
    
    rowchoices = (
        ('1', 'Row 1'),
        ('2', 'Row 2'),
        ('3', 'Row 3'),
        ('4', 'Row 4'),
        ('5', 'Row 5')
        )
    
    choices = list()
    for i in range(65, 91):
        choices.append([i-65, chr(i)])
    
    excel_file = forms.FileField()
    sheet = forms.ChoiceField(label="Sheet", choices=sheetChoice, widget=forms.Select(attrs={'class':'form-control'}))
    row = forms.ChoiceField(label="Row", choices=rowchoices, widget=forms.Select(attrs={'class':'form-control'}))
    farmer_name_col = forms.ChoiceField(label='Farmer Name Column', initial=0, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Farmers Name')
    cooperative_col = forms.ChoiceField(label='Cooperative Column', initial=1, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Cooperative')
    district_col = forms.ChoiceField(label='distric Column', initial=2, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the District')
    sub_county_col = forms.ChoiceField(label='Sub County Column', initial=3, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Sub county')
    number_of_animals_col = forms.ChoiceField(label='Number of Animals Column', initial=4, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the No Of Animals')
    phone_number_col = forms.ChoiceField(label='Phone Number Column', initial=5, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Phone Number')
    email_address_col = forms.ChoiceField(label='Email Address Column', initial=6, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Email')
    role_col = forms.ChoiceField(label='Role Column', initial=7, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Cooperate Role')
    qualification_col = forms.ChoiceField(label='Qualification Column', initial=8, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Qualification Level')
    land_col = forms.ChoiceField(label='Size of Land Column', initial=9, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Size of Land in Acres')
    breeds_col = forms.ChoiceField(label='Breed Column', initial=10, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Breed. If more than one, seperate with a comma')
    fenced_col = forms.ChoiceField(label='Fenced Column', initial=11, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Land is Fenced')
    house_hold_members_col = forms.ChoiceField(label='Number of House Hold Members Column', initial=12, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Number of Household  Member')
    date_of_birth_col = forms.ChoiceField(label='Date of Birth Column', initial=13, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Date of birth')
    # organisation_col = forms.ChoiceField(label='Organisation Column', initial=14, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Organisation')
    
    
    def clean(self):
        data = self.cleaned_data
        f = data.get('excel_file', None)
        ext = splitext(f.name)[1][1:].lower()
        if not ext in ["xlsx", "xls"]:
            raise forms.ValidationError(("The File type is not accepted"))
        return data


class CooperativeMemberBusinessForm(forms.ModelForm):
    class Meta:
        model = CooperativeMemberBusiness
        exclude = ['create_date', 'update_date']
        
        widgets = {
          'other_animal_diseases': forms.Textarea(attrs={'rows':1}),
        }


class CooperativeMemberProductDefinitionForm(forms.ModelForm):
    class Meta:
        model = CooperativeMemberProductDefinition
        exclude = ['create_date', 'update_date']
        
        widgets = {
          'product_variation': forms.CheckboxSelectMultiple(),
        }
        

class CooperativeMemberProductQuantityForm(forms.ModelForm):
    class Meta:
        model = CooperativeMemberProductQuantity
        exclude = ['create_date', 'update_date']


class DewormingScheduleForm(forms.ModelForm):
    class Meta:
        model = DewormingSchedule
        exclude = ['create_date', 'update_date']
        
        
class CooperativeMemberHerdMaleForm(forms.ModelForm):
    class Meta:
        model = CooperativeMemberHerdMale
        exclude = ['create_date', 'update_date']
        

class CooperativeMemberHerdFemaleForm(forms.ModelForm):
    class Meta:
        model = CooperativeMemberHerdFemale
        exclude = ['create_date', 'update_date']
    
 
class CooperativeMemberProductForm(forms.ModelForm):
    class Meta:
        model = CooperativeMemberProduct
        exclude = ['create_date', 'update_date']
  
        
class CooperativeMemberSupplyForm(forms.ModelForm):
    
    choices = (
            ('January', 'January'),
            ('February', 'February'),
            ('March', 'March'),
            ('April', 'April'),
            ('May', 'May'),
            ('June', 'June'),
            ('July', 'July'),
            ('August', 'August'),
            ('September', 'September'),
            ('October', 'October'),
            ('November', 'November'),
            ('December', 'December'),
        )
    # probable_sell_month = forms.MultipleChoiceField(widget=forms.SelectMultiple,
                                             # choices=choices)
    class Meta:
        model = CooperativeMemberSupply
        exclude = ['create_date', 'update_date']
    
    def __init__(self, *args, **kwargs):
        super(CooperativeMemberSupplyForm, self).__init__(*args, **kwargs)
        self.fields['probable_sell_month'] = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices=self.choices, required=False)
        if self.instance.probable_sell_month:
            self.initial['probable_sell_month'] = eval(self.instance.probable_sell_month)


class CommonDiseasesForm(forms.ModelForm):
    class Meta:
        model = CommonDisease
        exclude = ['create_date', 'update_date']


class DownloadMemberOptionForm(forms.Form):
    profile = forms.BooleanField(initial=True)
    farm = forms.BooleanField(required=False)
    herd = forms.BooleanField(required=False)
    member_supply = forms.BooleanField(required=False)
    
     
class DeprecatedDownloadMemberOptionForm(forms.Form):
    profile_choices = [['cooperative', 'Cooperative'], ['member_id', 'Memeber Id'], ['surname', 'Surname'], ['other_name', 'Other Name'],['date_of_birth', 'date_of_birth'],['gender', 'gender'],['maritual_status', 'maritual_status'],
        ['phone_number', 'phone_number'],['email', 'email'],['district', 'district'],['sub_county', 'sub_county'],['village', 'village'],['address', 'address'],
        ['gps_coodinates', 'gps_coodinates'],['children', 'children'],['other_household_members', 'other_household_members'],['education_level', 'education_level'],
        ['primary_income_source', 'primary_income_source'],['membership_fee', 'membership_fee'],
        ['coop_role', 'coop_role'],['animal_count', 'animal_count'],['shares', 'shares'],['sale_amount', 'sale_amount'],['paid_amount', 'paid_amount'],['surname', 'surname'],]
    
    farm_choices = [['business_name','business_name'], ['farm_district','farm_district'],['farm_sub_county','farm_sub_county'],['gps_coodinates','gps_coodinates'],
        ['size','size'],['fenced','fenced'],['paddock','paddock'],['water_source','water_source'],
        ['animal_identification','animal_identification'],['common_diseases','common_diseases'],['other_animal_diseases','other_animal_diseases'],['tick_control','tick_control']]
    
    deworming = [['deworm_date', 'deworm_date'], ['dewormer', 'dewormer']]
    
    breed = [['product_variation', 'Breed']]
    
    male_herd = [['adults', 'adults'], ['bullocks', 'bullocks'], ['calves', 'calves']]
    female_herd = [['f_adults', 'f_adults'], ['bullocks', 'bullocks'], ['f_calves', 'f_calves']]
    member_supply = [['nearest_market', 'nearest_market'], ['product_average_cost', 'product_average_cost'], ['price_per_kilo', 'price_per_kilo'],
        ['probable_sell_month', 'probable_sell_month'], ['sell_to_cooperative_society', 'sell_to_cooperative_society']]
    
    profile = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=profile_choices)
    farm = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=farm_choices)
    deworming = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=deworming)
    breed = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=breed)
    bull_herd = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=male_herd)
    cow_herd = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=female_herd)
    member_supply = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=member_supply)
    
        
class CooperativeContributionForm(forms.ModelForm):
    class Meta:
        model = CooperativeContribution
        exclude = ['create_date', 'update_date']
        

class CooperativeShareTransactionForm(forms.ModelForm):
       
    class Meta:
        model = CooperativeShareTransaction
        exclude = ['create_date', 'update_date'] 
    

class MemberSubscriptionForm(forms.ModelForm):
    class Meta:
        model = CooperativeMemberSubscriptionLog
        exclude = ['create_date', 'update_date']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "Member is Subscribed for the Year provided",
            }
        }
      
        
class MemberSharesForm(forms.ModelForm):
    class Meta:
        model = CooperativeMemberSharesLog
        exclude = ['create_date', 'update_date']
        
        widgets = {
          'shares': forms.TextInput(attrs={'readonly': True}),
        }
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MemberSharesForm, self).__init__(*args, **kwargs)
        if not self.request.user.profile.is_union():
            cooperative = self.request.user.cooperative_admin.cooperative
            price = CooperativeSharePrice.objects.filter(
                cooperative=cooperative).order_by('-create_date')
            self.fields['shares_price'].initial=price[0].price if price else ""
            self.fields['cooperative_member'].queryset = self.fields['cooperative_member'].queryset.filter(cooperative=cooperative)
        

class MemberSupplyRequestConfirmForm(forms.ModelForm):
    class Meta:
        model = MemberSupplyRequest
        fields = ('status', 'confirmed_by', 'comfirmation_method', 'remark')
    
    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(MemberSupplyRequestConfirmForm, self).__init__(*args, **kwargs)
    #     if not self.request.user.profile.is_union():
    #         cooperative = self.request.user.cooperative_admin.cooperative
    #         self.fields['cooperative_member'].queryset = self.fields['cooperative_member'].queryset.filter(cooperative=cooperative)
    #    


class MemberSupplyRequestForm(forms.ModelForm):
    class Meta:
        model = MemberSupplyRequest
        exclude = ('create_date', 'update_date', 'transaction_reference', 'created_by')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MemberSupplyRequestForm, self).__init__(*args, **kwargs)
        if not self.request.user.profile.is_union():
            cooperative = self.request.user.cooperative_admin.cooperative
            self.fields['cooperative_member'].queryset = self.fields['cooperative_member'].queryset.filter(cooperative=cooperative)
    
    def clean(self):
        data = self.cleaned_data
        trx_date = data.get('supply_date')
        if trx_date < timezone.now().date():
                raise forms.ValidationError("Error! The Supply date cannot be in the Past")
        return data
    

class VariationSupplyRequestFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

        breeds = []
        duplicates = False
        
        
        for form in self.forms:
            if form.cleaned_data:
                breed = form.cleaned_data['breed']
                
                # Check that no two links have the same anchor or URL
                if breed:
                    if breed in breeds:
                        duplicates = True
                    breeds.append(breed)
                
                if duplicates:
                    raise forms.ValidationError(
                        'Duplicate Breeds Found',
                        code='duplicate_values'
                    )
        

class MemberSupplyRequestVariationForm(forms.ModelForm):
    class Meta:
        model = MemberSupplyRequestVariation
        exclude = ('create_date', 'update_date', 'created_by')
  
     
class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        exclude = ['create_date', 'update_date']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CollectionForm, self).__init__(*args, **kwargs)

        if not self.request.user.profile.is_union():
            self.fields['cooperative'].widget=forms.HiddenInput()
            self.fields['cooperative'].initial=self.request.user.cooperative_admin.cooperative
        
    def clean(self):
        data = self.cleaned_data
        member = data.get('member')
        name = data.get('name')
        phone_number = data.get('phone_number')
        if not member:
            if not name and not phone_number:
                raise forms.ValidationError("Error! Please Select a Member or provide the Name of a non-member")
        if phone_number:       
            try:
                phone_number = internationalize_number(phone_number)
                self.cleaned_data['phone_number'] = phone_number
            except ValueError:
                raise forms.ValidationError("Please enter a valid phone number.'%s' is not valid" % phone_number)
        
        return data

class MemberOrderForm(forms.ModelForm):
    class Meta:
        model = MemberOrder
        fields = ['member', 'order_date']
    
        
class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ['create_date', 'update_date']
        widgets = {
          'item': forms.Select(attrs={'onChange': 'refreshInput(this)', 'class': 'id_item'}),
          'quantity': forms.TextInput(attrs={'onkeydown': 'calculatePrice(this)'}),
        }

bootstrapify(MemberOrderForm)
bootstrapify(OrderItemForm)
bootstrapify(CooperativeForm)
bootstrapify(MemberUploadForm)
bootstrapify(CooperativeUploadForm)
bootstrapify(CooperativeSharePriceForm)
bootstrapify(MemberProfileForm)
bootstrapify(CooperativeMemberBusinessForm)
bootstrapify(CooperativeMemberProductForm)
bootstrapify(CooperativeMemberSupplyForm)
bootstrapify(CooperativeContributionForm)
bootstrapify(CooperativeShareTransactionForm)
bootstrapify(MemberSubscriptionForm)
bootstrapify(MemberSharesForm)
bootstrapify(CooperativeMemberProductDefinitionForm)
bootstrapify(CooperativeMemberProductQuantityForm)
bootstrapify(CooperativeMemberProductQuantityForm)
bootstrapify(MemberProfileSearchForm)
bootstrapify(CooperativeMemberHerdMaleForm)
bootstrapify(CooperativeMemberHerdFemaleForm)
bootstrapify(CommonDiseasesForm)
bootstrapify(DewormingScheduleForm)
bootstrapify(MemberSupplyRequestForm)
bootstrapify(MemberSupplyRequestConfirmForm)
bootstrapify(MemberSupplyRequestVariationForm)
bootstrapify(CollectionForm)
