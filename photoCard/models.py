from django.db import models

"""
포토카드에 대한 정보를 담는 테이블
컬럼은 PK, 포토카드 이름, 등록일자로 구성
"""
# 포토카드 리스트
class PhotoCard(models.Model):
    id = models.AutoField(primary_key=True)
    photo_name = models.CharField(max_length=128)
    create_date = models.DateTimeField(auto_now_add=True)   # 최초 저장 시에만 현재 날짜를 적용