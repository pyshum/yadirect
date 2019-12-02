from rest_framework import serializers

from yadirect_api.models import ApiData


class ApiDataSerializer(serializers.HyperlinkedModelSerializer):

    def to_representation(self, obj):
        result = {}
        row = obj.data.get('rows')
        header = obj.data.get('header')
        if row and len(row) != 0:
            result = dict(zip(header, row[0]))
        return result

    class Meta:
        model = ApiData
        fields = '__all__'
        # fields = ('pk', 'data', 'created_at')
