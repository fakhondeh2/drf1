from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from . import serializers
from .models import Todo
from .serializers import TodoSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics , mixins
from rest_framework import viewsets


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
def todo_detail_view(request: Request, pk: int):
    global todo
    try:
        todo=Todo.objects.get(id=pk)
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

# region mixins


class Todo_mixin_list_mixin_api_view(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Todo.objects.order_by("priority").all()
    serializer_class = TodoSerializer


    def get(self,request: Request):
        return self.list(request)


    def post(self,request: Request):
        return self.create(request)




class Todo_detail_mixin_api_view(mixins.RetrieveModelMixin , mixins.UpdateModelMixin , mixins.DestroyModelMixin , generics.GenericAPIView):
    queryset = Todo.objects.order_by("priority").all()
    serializer_class = TodoSerializer


    def get(self,request: Request ,pk: int):
        return self.retrieve(request,pk)

    def put(self,request: Request ,pk: int):
        return self.update(request,pk)

    def delete(self,request: Request ,pk: int):
        return self.destroy(request,pk)
#endregion mixins

#region generics


class Todo_generic_list_api_view(generics.ListCreateAPIView):
    queryset = Todo.objects.order_by("priority").all()
    serializer_class = TodoSerializer


class Todo_generic_detail_api_view(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.order_by("priority").all()
    serializer_class = TodoSerializer

#endregion


#region viewsets

class Todo_viewsets_api_view(viewsets.ModelViewSet):
    queryset = Todo.objects.order_by("priority").all()
    serializer_class = TodoSerializer

#endregion