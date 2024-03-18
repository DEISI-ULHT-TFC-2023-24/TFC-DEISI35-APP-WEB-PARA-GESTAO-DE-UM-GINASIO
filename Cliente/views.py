from django.shortcuts import render

# Create your views here.
def area_cliente(request):
    return render(request, 'area-cliente.html')  # Substitua 'nome_do_seu_template.html' pelo nome real do seu arquivo de template
