from rest_framework.viewsets import  ModelViewSet
from encomiendas.models import GuiaEnvio, HistorialSeguimiento
from encomiendas.serializers import GuiaSerializer, HistorialSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from encomiendas.models import ESTADOS_PAQUETE
from rest_framework import status
from rest_framework.response import Response

class  GuiaViewSet(ModelViewSet):
    serializer_class = GuiaSerializer
    queryset = GuiaEnvio.objects.all()
    lookup_field = "numero_guia"
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(creado_por=user)
        return super().perform_create(serializer)

    @action(detail=True, methods=["post"])
    def actualizar_estado(self, request, numero_guia = None):
        estado = self.request.data.get("estado")
        observacion = self.request.data.get("observacion")
        guia = self.get_object()
        usuario = self.request.user if self.request.user.is_authenticated else None

        if estado in dict(ESTADOS_PAQUETE):
            guia.estado_actual = estado
            guia.save()

            HistorialSeguimiento.objects.create(guia=guia, estado=estado, observacion=observacion, actualizado_por=usuario)
            return Response({"mensaje": "Estado Actualizado"}, status=status.HTTP_200_OK)
        return Response({"mensaje": "Error, estado no válido"}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = GuiaEnvio.objects.all()

        estado = self.request.query_params.get('estado')

        if estado:
            queryset = queryset.filter(estado_actual__icontains=estado)

        return queryset

class HistorialViewSet(ModelViewSet):
    serializer_class = HistorialSerializer
    queryset = HistorialSeguimiento.objects.all()
    pagination_class = LimitOffsetPagination


