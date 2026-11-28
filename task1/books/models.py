from django.db import models
from django.conf import settings

# Create your models here.
class Book(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending approval"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    title = models.CharField(max_length=255)

    # Author user (set when an author submits a book)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="books",
    )
    author_name = models.CharField(max_length=100, blank=True)

    isbn = models.CharField(max_length=13, unique=True)
    description = models.TextField(blank=True)
    published_date = models.DateField(null=True, blank=True)
    genre = models.CharField(max_length=100, blank=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    # Make available_copies never exceed total_copies
    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(available_copies__lte=models.F("total_copies")),
                name="available_copies_lte_total_copies"
            )
        ]

class BorrowRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        REJECTED = "rejected", "Rejected"
        BORROWED = "borrowed", "Borrowed"
        RETURNED = "returned", "Returned"

    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="borrow_requests"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrow_requests",
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    borrowed_at = models.DateTimeField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)