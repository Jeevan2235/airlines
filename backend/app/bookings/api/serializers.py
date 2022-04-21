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
    flight_number = serializers.SerializerMethodField("get_flight_number")
    baggage_limit = serializers.SerializerMethodField("get_baggage_limit")
    flight_time = serializers.SerializerMethodField("get_flight_time")
    duration = serializers.SerializerMethodField("get_duration")
    departure_date = serializers.SerializerMethodField("get_departure_date")
    arrival_location = serializers.SerializerMethodField("get_arrival_location")
    departure_location = serializers.SerializerMethodField("get_departure_location")
    seat_no = serializers.SerializerMethodField("get_seat_no")

    def get_seat_no(self, obj):
        return obj.ticket.seat_no

    def get_departure_location(self, obj):
        return obj.ticket.flight.departure_location

    def get_arrival_location(self, obj):
        return obj.ticket.flight.arrival_location

    def get_departure_date(self, obj):
        return obj.ticket.flight.departure_date

    def get_duration(self, obj):
        return obj.ticket.flight.duration

    def get_flight_time(self, obj):
        return obj.ticket.flight.flight_time

    def get_baggage_limit(self, obj):
        return obj.ticket.flight.baggage_limit

    def get_flight_number(self, obj):
        return obj.ticket.flight.flight_number

    class Meta:
        model = Purchase
        fields = [
            "passenger_name",
            "flight_number",
            "baggage_limit",
            "flight_time",
            "duration",
            "departure_date",
            "arrival_location",
            "departure_location",
            "seat_no",
            "is_paid",
            "status",
        ]
        read_only_fields = (
            "passenger_name",
            "flight_number",
            "baggage_limit",
            "flight_time",
            "duration",
            "departure_date",
            "arrival_location",
            "departure_location",
            "seat_no",
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
