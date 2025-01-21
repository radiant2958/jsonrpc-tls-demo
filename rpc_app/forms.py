# rpc_app/forms.py
from django import forms

class RpcMethodForm(forms.Form):
    method_name = forms.CharField(
        label='Method name',
        initial='auth.check',
        required=True
    )
    # Параметры метода, которые пользователь укажет в JSON-формате
    params = forms.CharField(
        label='Method params (JSON)',
        required=False,
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50})
    )
