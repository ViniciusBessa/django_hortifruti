from django.shortcuts import render
from dados_comuns import dados_comuns


def page_error_404_view(request, exception):
    return render(request, '404.html', status=404, context=dados_comuns(request.user))
