from django import forms
from conf.utils import bootstrapify
from payment.models import MemberPayment
from coop.models import CooperativeMember

class MemberPaymentForm(forms.ModelForm):
    class Meta:
        model = MemberPayment
        fields = ['cooperative', 'member', 'amount', 'payment_date']
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MemberPaymentForm, self).__init__(*args, **kwargs)
        
        self.fields['member'].queryset = CooperativeMember.objects.none()
        
        if 'cooperative' in self.data:
            try:
                cooperative_id = int(self.data.get('cooperative'))
                self.fields['member'].queryset = CooperativeMember.objects.filter(cooperative=cooperative_id).order_by('first_name')
            except Exception as e: #(ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            if self.instance.cooperative:
                self.fields['member'].queryset = self.instance.cooperative.member_set.order_by('first_name')
        

bootstrapify(MemberPaymentForm)
        
    
