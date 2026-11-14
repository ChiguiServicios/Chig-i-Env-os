from rest_framework import serializers
from encomiendas.models import GuiaEnvio, HistorialSeguimiento
from uuid import uuid8
from utils.bcv import obtener_dolar_bcv_manual
from decimal import Decimal

class GuiaSerializer(serializers.ModelSerializer):
    monto_usd = serializers.DecimalField(max_digits=8, decimal_places=2, required=False, allow_null = True)
    monto_bolivares = serializers.DecimalField(max_digits=8, decimal_places=2, required=False, allow_null = True)
    class Meta:
        model = GuiaEnvio
        fields = '__all__'
        read_only_fields = ('numero_guia', 'estado_actual', 'fecha_creacion', 'creado_por')
        #lookup_field = "numero_guia"

    def create(self, validated_data):
        monto_usd = validated_data.get("monto_usd")
        monto_bolivares = validated_data.get("monto_bolivares")
        tasa_bcv = obtener_dolar_bcv_manual()

        if tasa_bcv and monto_usd:
            validated_data['monto_bolivares'] = Decimal(str(monto_usd)) * Decimal(str(tasa_bcv))
        elif tasa_bcv and monto_bolivares:
            validated_data['monto_usd'] = Decimal(str(monto_bolivares)) / Decimal(str(tasa_bcv))
        return super().create(validated_data)

class HistorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialSeguimiento
        fields = '__all__'