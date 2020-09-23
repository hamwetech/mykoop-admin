from django import forms
from conf.utils import bootstrapify
from system.models import Union


class UnionForm(forms.ModelForm):
    class Meta:
        model = Union
        fields = ['name', 'url', 'token']


bootstrapify(UnionForm)