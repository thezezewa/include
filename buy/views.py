from sell.models import SellPhotoCardList
from buy.models import User
from .serializers import BuySerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.shortcuts import get_object_or_404


# 구매하기
class BuyViewSet(viewsets.ModelViewSet):
    queryset = SellPhotoCardList.objects.filter(status=False)  # 판매 중인 목록 조회
    serializer_class = BuySerializer


    """
    Detail에서 조회한 객체를 구매할 수 있어야 합니다. > /sell/<int:photo_card_id>로 판매 목록 확인 가능
    유저는 현재 판매중인 가장 최소 가격의 판매건을 확인하고, 해당 객체를 구매할 수 있어야 합니다. > /sell/로 판매 목록 확인 가능
    판매 목록 테이블의 객체 id를 입력하여, 구매 합니다.

    만약, 로그인이 구현된 상태라면
    buyer_instance = get_object_or_404(User, id=request.user.id)
    이런 방식으로 구매자를 따로 가져오지 않고 구매 가능
    """
    # 구매하기
    def update(self, request, *args, **kwargs):
        # 구매할 포토카드 판매 목록 테이블의 객체 ID값 가져오기
        pk = self.kwargs.get("pk")
        photo_card = get_object_or_404(SellPhotoCardList, pk=pk)
        
        # 중복 구매 방지
        if photo_card.status is True:
            return Response(
                {"error": "이미 판매된 항목입니다."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # buyer의 ID 값 가져오기
        buyer_id = request.data.get("buyer")

        # buyer 객체 가져오기
        buyer = get_object_or_404(User, id=buyer_id)

        # 가격과 수수료 합친 금액 계산
        total_price = photo_card.price + photo_card.fee

        # 구매자의 cash 값이 부족할 경우
        if buyer.cash < total_price:
            return Response(
                {"error": "잔액이 부족합니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 정상 결제 (금액 업데이트)
        buyer.cash -= total_price
        buyer.save()

        # 구매 진행 (판매 상태 업데이트)
        photo_card.buyer = buyer
        photo_card.status = True
        photo_card.sold_date = datetime.today()
        photo_card.save()

        # 응답 반환
        return Response(
            self.serializer_class(photo_card).data,
            status=status.HTTP_200_OK
        )