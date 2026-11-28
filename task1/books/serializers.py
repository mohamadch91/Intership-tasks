from rest_framework import serializers
from .models import Book, BorrowRequest

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

    def validate(self, data):
        total = data.get("total_copies", getattr(self.instance, "total_copies", None))
        available = data.get("available_copies", getattr(self.instance, "available_copies", None))
        if total is not None and available is not None and available > total:
            raise serializers.ValidationError(
                "available_copies cannot exceed total_copies."
            )
        return data

class BorrowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRequest
        fields = [
            "id", "book", "user", "status", "created_at",
            "borrowed_at", "due_date", "returned_at",
        ]
        read_only_fields = fields