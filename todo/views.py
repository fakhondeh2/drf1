from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from . import serializers
from .models import Todo
from .serializers import TodoSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
# Create your views here.


#region function base view

@api_view(['GET',"post"])
def all_todos(request: Request):
    if request.method == 'GET':
        todos = Todo.objects.order_by("priority").all()
        todo_serializer = TodoSerializer(todos, many=True)
        return Response(todo_serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(None , status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET',"PUT","DELETE"])
def todo_detail_view(request: Request, todo_id: int):
    global todo
    try:
        todo=Todo.objects.get(id=todo_id)
    except Todo.DoesNotExist:
        return Response(None, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer=TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer=TodoSerializer(todo , data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        todo.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    else:
        return Response(None, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#endregion


#region class base view


class TodoList(APIView):
    def get(self ,request: Request):
        todos = Todo.objects.order_by("priority").all()
        todo_serializer = TodoSerializer(todos, many=True)
        return Response(todo_serializer.data, status=status.HTTP_200_OK)


    def post(self, request: Request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Todo_detail_api_view(APIView):


    def get_object(self,pk: int):
        try:
            todoo = Todo.objects.get(id=pk)
            return todoo
        except Todo.DoesNotExist:
            return None


    def get(self, request: Request, pk: int):
        todo = self.get_object(pk)
        if todo is not None:
            serializer=TodoSerializer(todo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_404_NOT_FOUND)



    def put(self, request: Request, pk: int):
        todo = self.get_object(pk)
        if todo is not None:
            serializer = TodoSerializer(todo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(None, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request: Request, pk: int):
        todo = self.get_object(pk)
        if todo is not None:
            todo.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
#endregion