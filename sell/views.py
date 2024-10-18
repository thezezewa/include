from .models import SellPhotoCardList
from .serializers import SellSerializer, SellDetailSerializer
from photoCard.serializers import PhotoCardSerializer
from rest_framework import viewsets
from buy.models import User
from rest_framework.response import Response
from rest_framework import status
from photoCard import models as PhotoModels
from django.db.models import OuterRef, Subquery
from django.shortcuts import get_object_or_404

# 판매하기
class SellViewSet(viewsets.ModelViewSet):
    queryset = SellPhotoCardList.objects.filter(status=False)
    serializer_class = SellSerializer


    """
    현재 판매중인 건만 List에서 조회할 수 있어야 합니다.
    photo_card_id는 중복될 수 있으며, 만약 동일한 photo_card_id의 판매가 여러건 존재 한다면, 가장 최소 가격의 객체만 조회해야 합니다.
    최소 가격까지 모두 동일하다면, renewal_date(가격 수정일)가 가정 먼저 등록된 객체가 조회 되어야 합니다.
    """
    # 판매 조회
    def get_queryset(self):
        subquery = SellPhotoCardList.objects.filter(
            photo_card=OuterRef('photo_card'), 
            status=False
        ).order_by('price', 'renewal_date').values('id')[:1]    # 포토카드별 최저가, 수정일이 제일 먼저 등록된 객체 가져오기

        queryset = SellPhotoCardList.objects.filter(
            id__in=Subquery(subquery)   # 위 subquery에서 찾은 ID에 해당하는 판매 내역 가져오기
        )
        
        return queryset


    """
    photo_card_id를 입력하여, Detail 조회할 수 있어야 합니다.
    id, price, fee, total_price(price + fee)를 필수 포함 하여야 합니다.
    해당 photo_card_id의 최근 거래가를 5개 조회할 수 있어야 합니다.

    Detail에서 조회한 객체를 구매할 수 있어야 합니다.
    : 이 문구가 있는 것으로 보아 현재 올라온 제품도 보이도록 구현
    """
    # Detail 조회
    def retrieve(self, request, *args, **kwargs):
        photo_card_id = self.kwargs.get('pk')   # 조회하려는 포토카드 ID
        photo_card = get_object_or_404(PhotoModels.PhotoCard, id=photo_card_id) # 조회하려는 포토 카드 객체 가져오기
        
        # 현재 판매 중인 포토카드
        queryset = SellPhotoCardList.objects.filter(
            photo_card=photo_card,
            status=False 
        ).order_by('price', 'renewal_date').first()

        # 최근 거래 내역
        recent_transactions = SellPhotoCardList.objects.filter(
            photo_card=photo_card,
            status=True  # 거래 완료 항목 조회
        ).order_by('-sold_date')[:5]

        # 최근 거래 내용 상세 조회 시리얼라이저 이용
        recent_transactions_serializer = SellDetailSerializer(recent_transactions, many=True)

        # 포토카드 데이터 상세 조회 및 최근 거래 5건
        result = {
            "detail": PhotoCardSerializer(photo_card).data,  # 포토카드 상세 데이터
            "photo_card": self.serializer_class(queryset).data if queryset else "판매 중인 포토카드가 없습니다.",
            "recent_transactions": recent_transactions_serializer.data  # 최근 거래 조회 데이터
        }

        return Response(result, status=status.HTTP_200_OK)


    """
    fee는 일정한 계산식을 통해 자동으로 입력됩니다.
    : fee = price * 0.1 이라는 간단한 계산식을 추가해서 구현

    만약, 로그인이 구현된 상태라면
    serializer.save(seller_id=self.request.user, fee=fee)
    이런 방식으로 판매자를 따로 가져오지 않고 판매 등록
    """
    # 판매 등록
    def perform_create(self, serializer):
        seller = serializer.validated_data.get('seller')  # 판매자 계정 가져오기
        price = self.request.data.get("price")   # price 값 가져오기
        fee = int(price) * 0.1   # fee 는 일정한 계산식을 통해 자동으로 입력 구현
        serializer.save(seller=seller, fee=fee)