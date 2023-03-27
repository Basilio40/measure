import cv2
import numpy as np
from django.contrib.auth.models import User, Group
from rest_framework import serializers

from apps.medicao_lente.measure_lens import MeasurementLens
from apps.medicao_lente.models import DadosMedicao

mlens = MeasurementLens()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class DadosMedicaoSerializer(serializers.ModelSerializer):
    horizontal = serializers.HiddenField(default=0)
    vertical = serializers.HiddenField(default=0)
    diagonalMaior = serializers.HiddenField(default=0)
    OS = serializers.CharField(max_length=255)
    DNP = serializers.IntegerField()
    altura = serializers.IntegerField()
    leituraDireito = serializers.BooleanField()
    leituraEsquerdo = serializers.BooleanField()

    class Meta:
        model = DadosMedicao
        fields = "__all__"
        # fields = [
        #     "horizontal",
        #     "vertical",
        #     "diagonalMaior",
        #     "OS",
        #     "DNP",
        #     "altura",
        #     "leituraDireito",
        #     "leituraEsquerdo",
        #     "image"
        # ]

    def create(self, validated_data):
        data_image = validated_data.get('image')
        data = data_image.read()
        _image = np.asarray(bytearray(data), dtype='uint8')
        _image = cv2.imdecode(_image, cv2.IMREAD_GRAYSCALE)

        lens = mlens.run(image=_image)

        # validated_data["horizontal"] = lens["horizontal"]
        # validated_data["vertical"] = lens["vertical"]
        # validated_data["diagonalMaior"] = lens["diagonal_maior"]
        dado_medicao = DadosMedicao.objects.create(**validated_data)
        dado_medicao.horizontal = lens["horizontal"]
        dado_medicao.vertical = lens["vertical"]
        dado_medicao.diagonalMaior = lens["diagonalMaior"]
        dado_medicao.save()

        return dado_medicao