from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Invoice, InvoiceItem
from .serializers import InvoiceSerializer, InvoiceListSerializer
import json
from rest_framework import  filters


# ✅ Create - already done (keeping for context)
class InvoiceCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        raw_items_str = data.get("items")
        items = []

        if raw_items_str:
            try:
                items = json.loads(raw_items_str)
            except json.JSONDecodeError as e:
                return Response({"error": f"Invalid JSON in items: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        final_data = {
            key: value[0] if isinstance(value, list) else value
            for key, value in request.data.lists()
        }
        final_data["items"] = items

        serializer = InvoiceSerializer(data=final_data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ Fetch single
class InvoiceDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, invoice_id):
        try:
            invoice = Invoice.objects.get(id=invoice_id, user=request.user)
            serializer = InvoiceListSerializer(invoice)
            return Response(serializer.data)
        except Invoice.DoesNotExist:
            return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)


# ✅ Update
class InvoiceUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, invoice_id):
        try:
            invoice = Invoice.objects.get(id=invoice_id, user=request.user)
        except Invoice.DoesNotExist:
            return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        raw_items_str = data.get("items")
        items = []

        if raw_items_str:
            try:
                items = json.loads(raw_items_str)
            except json.JSONDecodeError as e:
                return Response({"error": f"Invalid JSON in items: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        final_data = {
            key: value[0] if isinstance(value, list) else value
            for key, value in request.data.lists()
        }
        final_data["items"] = items

        serializer = InvoiceSerializer(invoice, data=final_data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ Delete by ID
class InvoiceDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, invoice_id):
        try:
            invoice = Invoice.objects.get(id=invoice_id, user=request.user)
            invoice.delete()
            return Response({"success": "Invoice deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Invoice.DoesNotExist:
            return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)


# ✅ List all

class InvoiceListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['due_date']
    search_fields = ['invoice_number']

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user).order_by('-created_at')
