# rpc_app/views.py

import json
from django.views.generic import FormView
from django.shortcuts import render
from .forms import RpcMethodForm
from .rpc_client import call_jsonrpc

class RpcMethodView(FormView):
    template_name = 'rpc_app/method_form.html'
    form_class = RpcMethodForm

    def form_valid(self, form):
        # Получаем данные из формы
        method_name = form.cleaned_data['method_name']
        raw_params = form.cleaned_data['params'].strip()

        # Парсим входящие параметры как JSON
        if raw_params:
            try:
                params = json.loads(raw_params)
            except json.JSONDecodeError:
                params = {}
        else:
            params = {}

        # Вызываем JSON-RPC
        response = call_jsonrpc(method_name, params=params, request_id=1)

        # Передадим результат в тот же шаблон
        context = {
            'form': form,
            'rpc_response': response
        }
        return render(self.request, self.template_name, context)
