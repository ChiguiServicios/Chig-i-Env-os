from django.shortcuts import render
from ubicaciones.models import Agencia, Ciudad, Estado
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from ubicaciones.serializers import EstadoSerializer, CiudadGETSerializer, AgenciaSerializer

class EstadoView(APIView):
    permission_classes = [AllowAny,]
    def get(self, request):
        import ipdb; ipdb.set_trace()
        data = Estado.objects.all()

        nombre = self.request.query_params.get('estado')

        if nombre:
            data = data.filter(nombre__icontains=nombre)

        serializer = EstadoSerializer(data, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EstadoSerializer(data = self.request.data)
        serializer.is_valid(raise_exception=True)
        existe = Estado.objects.filter(nombre__icontains=serializer.data["nombre"]).exists()
        if existe:
            return Response({"mensaje": "Ese Estado ya existe"}, status=status.HTTP_400_BAD_REQUEST)
        Estado.objects.create(**serializer.data)
        return Response({"mensaje": f"El Estado {serializer.data["nombre"]} ha sido creado"}, status=status.HTTP_201_CREATED)
    
class EstadoViewDetail(APIView):
    def get(self, request, pk=None):

        try:
            registro = Estado.objects.get(pk=pk)
        except:
            return Response({"mensaje":"Ese Estado no existe"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EstadoSerializer(registro)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):

        try:
            registro = Estado.objects.get(pk=pk)
            registro.delete
        except:
            return Response({"mensaje":"Ese Estado no existe"}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def put (self, request, pk=None, is_partial = False):

        nombre = self.request.data["nombre"]

        if not nombre:
            return Response({"mensaje":"El nombre es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            registro = Estado.objects.get(pk=pk)
            serializer = EstadoSerializer(registro, data = self.request.data, partial = False)
            if serializer.is_valid():
                serializer.save()
                return Response({"mensaje":"El Estado se ha actualizado"}, status=status.HTTP_200_OK)
        except Estado.DoesNotExist:
            return Response({"mensaje":"Ese Estado no existe"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk=None):
        return self.put(request=request, pk=pk, is_partial = True)

class CiudadViewSet(ViewSet):
    def list(self, request):
        queryset = Ciudad.objects.all()
        nombre = self.request.query_params.get('nombre')
        estado_param = self.request.query_params.get('estado')
        estado = int(estado_param) if estado_param is not None and estado_param != '' else None
        
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)

        if estado:
            queryset = queryset.filter(estado=estado)

        paginator = PageNumberPagination()
        datos = paginator.paginate_queryset(queryset, request, view=self)

        if datos is not None:
            serializer = CiudadGETSerializer(datos, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = CiudadGETSerializer(Ciudad.objects.all(), many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):

        try:
            registro = Ciudad.objects.get(pk=pk)
            serializer = CiudadGETSerializer(registro)
        except Ciudad.DoesNotExist:
            return Response({"mensaje":"Esta Ciudad no existe"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = CiudadGETSerializer(data = self.request.data)
        serializer.is_valid(raise_exception=True)
        datos = self.request.data.copy()
        id_estado = datos["estado"]
        estado = Estado.objects.get(id=id_estado)
        existe = Ciudad.objects.filter(nombre__icontains=serializer.data["nombre"], estado=estado).exists()
        
        if existe:
            return Response({"mensaje": f"{datos["nombre"]} ya existe registrada en ese Estado"}, status=status.HTTP_400_BAD_REQUEST)
        Ciudad.objects.create(estado=estado, nombre=serializer.data["nombre"])
        return Response({"mensaje": f"La Ciudad {serializer.data["nombre"]} ha sido creada"}, status=status.HTTP_201_CREATED)
    
    def update(self, request):
            pass

    def partial_update(self, request):
            pass

    def delete(self, request):
            try:
                ciudad = Ciudad.objects.get(pk=pk)
                ciudad.delete()
                return Response({"mensaje": "La ciudad se ha borrado"}, status.HTTP_204_NO_CONTENT)
            except Ciudad.DoesNotExist:
                return Response({"mensaje": "No existe la ciudad que intentas borrar"}, status.HTTP_404_NOT_FOUND)

class AgenciaViewSet(ModelViewSet):
    serializer_class = AgenciaSerializer
    queryset = Agencia.objects.all()