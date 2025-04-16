from django.contrib.auth import get_user_model
from businessdetails.models import BusinessDetail, TeamSize
from common_country_module.models import Country

User = get_user_model()

def run():
    try:
        user = User.objects.get(id=3)  # Replace with correct user ID
    except User.DoesNotExist:
        print("User with ID 4 not found.")
        return

    # Get or create TeamSize instances
    team1, _ = TeamSize.objects.get_or_create(Size="10-50")
    team2, _ = TeamSize.objects.get_or_create(Size="50-100")

    # Get country instance by code or name (adjust accordingly)
    try:
        country = Country.objects.get(code="IN")  # or use name="India" based on your Country model
    except Country.DoesNotExist:
        print("Country with code IN not found.")
        return

    # Create first business detail
    BusinessDetail.objects.create(
        user=user,
        business_name="Techie Corp",
        team_size=team1,
        website="https://www.techiecorp.com",
        phone="9876543210",
        country=country,
        gstin="22AAAAA0000A1Z5"
    )

    # Create second business detail
    BusinessDetail.objects.create(
        user=user,
        business_name="Retail Masters",
        team_size=team2,
        website="https://www.retailmasters.com",
        phone="9123456789",
        country=country,
        gstin="11BBBBB1111B2Z6"
    )

