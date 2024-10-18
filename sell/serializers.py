from .models import SellPhotoCardList
from rest_framework import serializers

# 일반 조회
class SellSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellPhotoCardList
        """
        User는 photo_card_id와 price를 입력하여, 판매를 등록 할 수 있습니다.
        각 객체는 id, photo_card_id, price를 필수 포함 하여야 합니다.

        로그인 기능을 구현하지 않고 판매자를 등록하기 위해 seller 항목 추가
        """
        fields = ["id", "photo_card", "price", "seller"]

# 상세 조회
class SellDetailSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()    # 합계

    class Meta:
        model = SellPhotoCardList
        fields = ["photo_card", "price", "fee", "total_price", "seller"]

    # total_price 계산
    def get_total_price(self, obj):
        return obj.price + obj.fee