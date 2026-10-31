from django.shortcuts import render
from django.http import HttpRequest,JsonResponse,HttpResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from todo.models import Todo


# Create your views here.



def index(request):

    context = {"todos":Todo.objects.order_by("priority").all(),

               }
    return render(request,"index_page.html",context)


@api_view(['GET'])
def todos_json(request: Request):
    todos = list(Todo.objects.order_by("priority").all().values("is_done", "priority"))
    return Response({"todos": todos}, status=status.HTTP_200_OK)
