from django.contrib.auth import get_user_model
from businessdetails.models import BusinessDetail

User = get_user_model()

def run():
    try:
        user = User.objects.get(id=4)  # Replace with correct user ID or email
    except User.DoesNotExist:
        print("User with ID 4 not found.")
        return

    BusinessDetail.objects.create(
        user=user,
        business_category="IT Services",
        company_name="Techie Corp",
        address="123 Tech Street, Silicon Valley",
        gstin="22AAAAA0000A1Z5",
        pan="ABCDE1234F",
        email="contact@techiecorp.com",
        phone="9876543210"
    )

    BusinessDetail.objects.create(
        user=user,
        business_category="Retail",
        company_name="Retail Masters",
        address="456 Market Lane, Delhi",
        gstin="11BBBBB1111B2Z6",
        pan="FGHIJ5678K",
        email="info@retailmasters.com",
        phone="9123456789"
    )

    print("✅ Seeded 2 business detail entries for user:", user.email)
