from django import forms
from activity.models import ThematicArea
from conf.utils import bootstrapify



class ThematicAreaForm(forms.ModelForm):
    class Meta:
        model = ThematicArea
        fields = ['thematic_area', 'description']
             
bootstrapify(ThematicAreaForm)