from rest_framework import serializers

from yadirect_api.models import ApiData


class ApiDataSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ApiData
        fields = ('pk', 'data', 'created_at')
