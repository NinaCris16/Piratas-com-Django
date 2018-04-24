from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from piratapp.models import Tesouro
from django.urls.base import reverse, reverse_lazy

class TesouroInsert(CreateView):
    
    model = Tesouro
    template_name = "index.html"

    fields=["img_tesouro", "nome", "valor", "quantidade"]

    def get_context_data(self, **kwargs):
        context = super(TesouroInsert, self).get_context_data(**kwargs)
        context["lista_tesouro"] = Tesouro.objects.all()

        return context  

    def get_success_url(self):
        return reverse('GerenciadorTesouros')
    
    class Meta:
        labels = {
            "img_tesouro" : "Tesouro",
            "nome" : "Nome",
            "valor" : "Valor unitário",
            "quantidade" : "Quantidade"
        } 

