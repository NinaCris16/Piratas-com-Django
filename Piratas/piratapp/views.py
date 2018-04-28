from django.shortcuts import render
from django.forms.utils import ErrorList
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from piratapp.models import Tesouro
from django.urls.base import reverse, reverse_lazy
from django.db.models import F,ExpressionWrapper,DecimalField

class TesouroUtil(object):

    def form_valid(self, view, form):
        lsta_tesouro = Tesouro.objects.filter(nome=form.instance.nome)
        if(form.instance.pk != None):
            lsta_tesouro = lsta_tesouro.exclude(pk=form.instance.pk)
        if len(lsta_tesouro) > 0:
            errors = form._errors.setdefault("nome", ErrorList())
            errors.append(u"nomes iguais não são permitidos")
            return False
        
        return True

    def get_context_data(self, context):
        lstTesouros = Tesouro.objects.annotate(total=ExpressionWrapper(F('valor') * F('quantidade'),output_field=DecimalField(max_digits=10,decimal_places=2, blank=True)))
        context["lista_tesouro"] = lstTesouros
        soma = 0
        for tesouro in lstTesouros:
            soma += tesouro.total
        context["preco_total"] = soma 
      

class TesouroInsert(CreateView):
    
    model = Tesouro
    template_name = "index.html"
    util = TesouroUtil()

    fields=["img_tesouro", "nome", "valor", "quantidade"]

    def form_valid(self, form):        
        bol_valid = TesouroInsert.util.form_valid(self, form)
        return super(CreateView, self).form_valid(form) if bol_valid else super(CreateView, self).form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super(TesouroInsert, self).get_context_data(**kwargs)
        TesouroInsert.util.get_context_data(context)
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

class TesouroUpdate(UpdateView):
    model = Tesouro
    template_name = "index.html"
    util = TesouroUtil()

    fields=["img_tesouro", "nome", "valor", "quantidade"]
	
    def form_valid(self, form):        
        bol_valid = TesouroUpdate.util.form_valid(self, form)
        return super(UpdateView, self).form_valid(form) if bol_valid else super(UpdateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(TesouroUpdate, self).get_context_data(**kwargs)
        TesouroUpdate.util.get_context_data(context)
        return context

    def get_object(self):
        return Tesouro.objects.get(nome=self.kwargs["nome"])
    
    def get_success_url(self):
        return reverse('GerenciadorTesouros')
    
class TesouroDelete(DeleteView):
    model = Tesouro

    def get_object(self):
        return Tesouro.objects.get(nome=self.kwargs["nome"])
     
    def get_success_url(self):
        return reverse_lazy('GerenciadorTesouros')

