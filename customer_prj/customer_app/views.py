from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Customer
from .serializer import CustomerSerializer

# Hardcoded Admins
ADMIN_USERS = ["Shreyansh", "Ankur"]

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_user_role(self, request):
        """Determine the user role based on username"""
        username = request.headers.get("Username", "")  # Extract from request header
        if username in ADMIN_USERS:
            return "admin"
        elif username.startswith("vendor_"):  # Example check for vendors
            return "vendor"
        else:
            return "customer"

    def get_permissions(self):
        """Assign permissions based on user role"""
        role = self.get_user_role(self.request)

        if role == "admin":
            return [permissions.AllowAny()]  # Admin has all rights
        elif role == "customer":
            return [permissions.IsAuthenticated()]  # Customers have CRUD
        elif role == "vendor":
            return [permissions.IsAuthenticated()]  # Vendor has no access
        return [permissions.IsAuthenticated()]
        # return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        """Admin and Customer can create"""
        role = self.get_user_role(request)
        if role in ["admin", "customer"]:
            return super().create(request, *args, **kwargs)
        return Response({"error": "Permission denied"}, status=403)

    def update(self, request, *args, **kwargs):
        """Only Admin can update"""
        role = self.get_user_role(request)
        if role == "admin":
            return super().update(request, *args, **kwargs)
        return Response({"error": "Permission denied"}, status=403)

    def destroy(self, request, *args, **kwargs):
        '''Admin can delete anyone, but a Customer can only delete themselves'''
        role = self.get_user_role(request)
        username = request.headers.get("Username", "")

        customer = self.get_object()

        if role == "admin":
            self.perform_destroy(customer)
            return Response({"message": f"Customer {customer.c_fname} deleted successfully."}, status=status.HTTP_200_OK)
        elif role == "customer" and username == customer.c_fname:  # Assuming c_fname is their unique username
            self.perform_destroy(customer)
            return Response({"message": "Your account has been deleted successfully."}, status=status.HTTP_200_OK)

        return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)