from decimal import Decimal
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.models import Product
from stock.models import Inventory
from api.authentication import APIKeyAuthentication
from api.permissions import HasValidAPIKey
from api.serializers import ProductInventorySerializer
from drf_spectacular.utils import extend_schema

# Create your views here.

class ProductInventoryAPIView(APIView):
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [HasValidAPIKey]

    @extend_schema(responses=ProductInventorySerializer)
    def get(self, request, sku):
        organization = request.user

        product = Product.objects.filter(
            organization=organization,
            sku=sku,
        ).first()

        if not product:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        total_quantity = Inventory.objects.filter(
            organization=organization,
            product=product,
            warehouse__status="active",
        ).aggregate(total=Sum("quantity"))["total"] or Decimal("0.0")

        data = {
            "product": {
                "name": product.name,
                "sku": product.sku,
            },
            "inventory": {
                "total_quantity": total_quantity,
                "is_in_stock": total_quantity > 0,
            },
        }

        serializer = ProductInventorySerializer(data)

        return Response(serializer.data, status=status.HTTP_200_OK)
    