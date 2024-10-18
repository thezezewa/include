from .models import PhotoCard
from rest_framework import serializers

class PhotoCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoCard
        """
        상세 조회 시 보여질 포토카드 세부 내용
        """
        fields = ["photo_name", "create_date"]