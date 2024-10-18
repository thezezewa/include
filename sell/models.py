from django.db import models
from buy.models import User
from photoCard import models as PhotoModels

# 판매 목록 테이블
class SellPhotoCardList(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    photo_card = models.ForeignKey(PhotoModels.PhotoCard, on_delete=models.CASCADE)
    price = models.IntegerField(null=False)
    fee = models.IntegerField(null=False)
    status = models.BooleanField(default=False)   # N: 판매 중, Y: 판매 완료
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="buyer")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    create_date = models.DateTimeField(auto_now_add=True)   # 최초 저장 시에만 현재 날짜를 적용
    renewal_date = models.DateTimeField(auto_now=True)  # 변경될 때마다 현재 날짜로 갱신
    sold_date = models.DateTimeField(null=True, blank=True)