from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Livro
from .serializers import LivroSerializer

# substitui csrf_exempt por api_view para corrigir o erro AssertionError: .accepted_renderer not set on Response
@api_view(['GET', 'POST'])
def livro_list_create(request):
    if request.method == 'GET':
        livros = Livro.objects.all()
        serializer = LivroSerializer(livros, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = LivroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def livro_detail(request, pk):
    # acidionado try except para tratar o erro 500 ao tentar deletar um livro que não existe
    try:
        livro = Livro.objects.get(pk=pk)
    except Livro.DoesNotExist:
        return Response({'error': 'Livro não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LivroSerializer(livro)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = LivroSerializer(livro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        livro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
