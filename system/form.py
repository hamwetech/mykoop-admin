from django import forms
from conf.utils import bootstrapify
from system.models import Union, CooperativeMember


class UnionForm(forms.ModelForm):
    class Meta:
        model = Union
        fields = ['name', 'url', 'token']


class MemberProfileSearchForm(forms.Form):
    choices = (('', 'Role'), ('Chairman', 'Chairman'), ('Vice Chairman', 'Vice Chairman'), ('Treasurer', 'Treasurer'),
               ('Secretary', 'Secretary'), ('Member', 'Member'), ('Secretary Manager', 'Secretary Manager'),
               ('Patron', 'Patron'))

    name = forms.CharField(max_length=150, required=False)
    phone_number = forms.CharField(max_length=150, required=False)
    cooperative = forms.ChoiceField(widget=forms.Select(), choices=[], required=False)
    union = forms.ChoiceField(widget=forms.Select(), choices=[], required=False)
    role = forms.ChoiceField(widget=forms.Select(), choices=choices, required=False)
    district = forms.ChoiceField(widget=forms.Select(), choices=[], required=False)
    start_date = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class':'some_class', 'id':'uk_dp_1',
                                                                                               'data-uk-datepicker': "{format:'YYYY-MM-DD'}",
                                                                                               'autocomplete':"off"}))
    end_date = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class':'some_class', 'id':'uk_dp_1',
                                                                                               'data-uk-datepicker': "{format:'YYYY-MM-DD'}",
                                                                                               'autocomplete':"off"}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MemberProfileSearchForm, self).__init__(*args, **kwargs)
        unions = Union.objects.all()
        uchoices = [['', 'Union']]
        choices = []
        dchoices = []
        members = list()
        for u in unions:

            uchoices.append([u.id, u.name])
            # r = CooperativeMember.objects.using(u.name.lower()).all()
            qs = CooperativeMember.objects.using(u.name.lower()).values('cooperative__id', 'cooperative__name').distinct()
            d_qs = CooperativeMember.objects.using(u.name.lower()).values('district__id', 'district__name').distinct()
            if qs:
                # members.extend(qs)
                choices = [['', 'Cooperative']]
                for q in qs:
                    choices.append([q['cooperative__id'], q['cooperative__name']])
            if d_qs:
                # members.extend(d_qs)
                dchoices = [['', 'District']]
                for dq in d_qs:
                    dchoices.append([dq['district__id'], dq['district__name']])

        self.fields['cooperative'].choices = choices
        self.fields['district'].choices = dchoices
        self.fields['union'].choices = uchoices

class DownloadMemberOptionForm(forms.Form):
    profile = forms.BooleanField(initial=True)
    farm = forms.BooleanField(required=False)
    herd = forms.BooleanField(required=False)
    member_supply = forms.BooleanField(required=False)

bootstrapify(UnionForm)
bootstrapify(MemberProfileSearchForm)