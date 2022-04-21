from os import stat
from rest_framework import serializers

from bookings.models import Purchase, Booking
from tickets.models import Ticket
from tickets.api.serializers import TicketSerializer
from accounts.api.serializers import UserSerializer


class BookingSerializer(serializers.ModelSerializer):
    """Serializes Purchase Object"""

    booking_user_details = serializers.SerializerMethodField("get_booking_user_details")
    ticket_details = serializers.SerializerMethodField("get_ticket_details")

    def get_booking_user_details(self, obj):
        return UserSerializer(obj.booked_by).data

    def get_ticket_details(self, obj):
        return TicketSerializer(obj.ticket).data

    class Meta:
        model = Booking
        fields = "__all__"

    def create(self, validated_data):
        ticket = validated_data.get("ticket")
        if Ticket.objects.filter(id=ticket.id, booked=True).exists():
            raise serializers.ValidationError(
                "TICKET ALREADY BOOKED PLEASE CHOOSE ANOTHER TICKET"
            )
        return super().create(validated_data)


class PurchaseSerializer(serializers.ModelSerializer):
    """Serializes Purchase Object"""

    ticket_details = serializers.SerializerMethodField("get_ticket_details")

    def get_ticket_details(self, obj):
        return TicketSerializer(obj.ticket).data

    class Meta:
        model = Purchase
        fields = "__all__"

    def create(self, validated_data):
        ticket = validated_data.get("ticket")
        if Ticket.objects.filter(id=ticket.id, booked=True).exists():
            raise serializers.ValidationError(
                "TICKET ALREADY BOOKED OR PURCHASED PLEASE CHOOSE ANOTHER TICKET"
            )
        return super().create(validated_data)


class PurchaseConfirmSerializer(serializers.ModelSerializer):
    """Serializes Purchase Object"""

    status = serializers.CharField(write_only=True, required=True)
    ticket_details = serializers.SerializerMethodField("get_ticket_details")

    def get_ticket_details(self, obj):
        return TicketSerializer(obj.ticket).data

    class Meta:
        model = Purchase
        fields = "__all__"
        read_only_fields = (
            "passenger_name",
            "passenger_gender",
            "passenger_document_type",
            "passenger_document_number",
            "passenger_nationality",
            "contact_name",
            "contact_gender",
            "contact_phone",
            "contact_email",
            "ticket",
            "is_paid",
        )
        write_only_fields = ("status",)

    def update(self, instance, validated_data):
        status = validated_data.pop("status", None)
        if status is not None:
            if status.lower() == "completed":
                instance = super().update(instance, validated_data)
                instance.is_paid = True
                instance.save()
                return instance
            raise serializers.ValidationError("Failed Transaction Not Complete")
        raise serializers.ValidationError("Transaction Status Must be Provided")
