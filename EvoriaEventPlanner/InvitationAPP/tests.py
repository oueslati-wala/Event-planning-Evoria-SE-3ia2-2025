from django.test import TestCase
from django.utils import timezone
from .models import Invitation, Guest
from .forms import InvitationForm, GuestForm

class InvitationModelTest(TestCase):
    def setUp(self):
        """Set up a valid invitation for tests."""
        self.invitation = Invitation.objects.create(
            name="Conférence sur l'IA",
            theme="Intelligence Artificielle",
            location="Paris",
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=2),
        )

    def test_create_valid_guest(self):
        """Test creating a valid guest"""
        guest = Guest.objects.create(
            invitation=self.invitation,
            title="mr",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="+1 234 567 890",
            company="Doe Corp",
            position="CEO",
            status="confirmed",
        )
        self.assertEqual(str(guest), "mr John Doe")
        self.assertEqual(guest.invitation, self.invitation)
    def setUp(self):
        """Set up a valid invitation and guest for tests."""
        self.invitation = Invitation.objects.create(
            name="Conférence sur la Blockchain",
            theme="Technologie Blockchain",
            location="Lyon",
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=1),
        )
        self.guest = Guest.objects.create(
            invitation=self.invitation,
            title='mr',
            first_name='Jean',
            last_name='Dupont',
            email='jean.dupont@example.com',
            phone='+33 6 12 34 56 78',
        )
