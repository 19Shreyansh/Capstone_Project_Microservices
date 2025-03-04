from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product
from .serializers import ProductSerializer

# Default Admins
ADMIN_USERS = ["Shreyansh", "Ankur"]

def get_user_role(request):
    """Determine user role from headers (simulated authentication)."""
    username = request.headers.get("Username", "").strip()
    role = request.headers.get("Role", "").strip().lower()
    
    if username in ADMIN_USERS:
        return "admin"
    elif role == "vendor":
        return "vendor"
    return "customer"  # Default role

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        """Set permissions based on user role."""
        if self.request.method in ["POST", "PUT", "DELETE"]:
            return [permissions.IsAuthenticated()]  # Ensure authentication for write actions
        return []

    def list(self, request, *args, **kwargs):
        """Customers, vendors, and admins can view products."""
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Customers, vendors, and admins can retrieve a product."""
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Only admins and vendors can add products."""
        role = get_user_role(request)
        if role in ["admin", "vendor"]:
            return super().create(request, *args, **kwargs)
        return Response({"error": "Permission denied"}, status=403)

    def update(self, request, *args, **kwargs):
        """Only admins and vendors can update products."""
        role = get_user_role(request)
        if role in ["admin", "vendor"]:
            return super().update(request, *args, **kwargs)
        return Response({"error": "Permission denied"}, status=403)

    def destroy(self, request, *args, **kwargs):
        """Only admins and vendors can delete products."""
        role = get_user_role(request)
        if role in ["admin", "vendor"]:
            response = super().destroy(request, *args, **kwargs)
            return Response({"message": "Product deleted successfully"}, status=200)
        return Response({"error": "Permission denied"}, status=403)

    @action(detail=False, methods=["GET"])
    def search(self, request):
        """Search for products by name (available to all users)."""
        query = request.query_params.get("q", "")
        if not query:
            return Response({"error": "No search term provided"}, status=400)
        
        products = Product.objects.filter(p_name__icontains=query)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
