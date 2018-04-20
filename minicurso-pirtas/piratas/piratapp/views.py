from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from piratapp.models import Tesouro

class TesouroListView(ListView):
    
    model = Tesouro
    template_name = "index.html"

    def get_queryset(self):
        return Tesouro.objects.all()


# Não funciona ainda
class TesouroInsert(CreateView):
    
    model = Tesouro
    template_name = "index.html"

    fields=["img_tesouro", "nome", "valor", "quantidade"]

    def get_context_data(self, **kwargs):
        context = super(TesouroInsert, self).get_context_data(**kwargs)
        print(context)
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
