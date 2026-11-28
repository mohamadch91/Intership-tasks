from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer, BorrowRequestSerializer

# Gets role
def get_role(user):
    return getattr(user, "role", None)

# Get approved books
def visible_books(user):
    # Admin can see all books
    if get_role(user) == "administration":
        return Book.objects.all()
    return Book.objects.filter(status=Book.Status.APPROVED)

# Shared by approve and reject: admin sets a book's status
def set_book_status(request, pk, new_status):
    if get_role(request.user) != "administration":
        return admin_only_response()

    book = get_object_or_404(Book, pk=pk)
    book.status = new_status
    book.save(update_fields=["status"])
    return Response(BookSerializer(book).data)

# Response for non admin users
def admin_only_response():
    return Response(
        {"detail": "Only administration users can perform this action."},
        status=status.HTTP_403_FORBIDDEN,
    )
# Bad request message
def bad_request(message):
    return Response({"detail": message}, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
# List all books and add books
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def book_list(request):
    # GET: List all books
    if request.method == "GET":
        books = visible_books(request.user)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST: Add book (admin: direct, author: needs approval)
    role = get_role(request.user)
    if role not in ("administration", "author"):
        return Response(
            {"detail": "Only administration and author users can add books"},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = BookSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    if role == "administration":
        # Admin books are published directly
        book = serializer.save(status=Book.Status.APPROVED)
    else:
        # Author books wait for admin approval
        book = serializer.save(status=Book.Status.PENDING, author=request.user)

    return Response(
        {
            "message": "Book added successfully",
            "book": BookSerializer(book).data,
        },
        status=status.HTTP_201_CREATED,
    )

# Get, update and delete specific books
@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def book_detail(request, pk):
    # GET: display selected book data
    book = get_object_or_404(visible_books(request.user), pk=pk)
    serializer = BookSerializer(book)

    if request.method == "GET":
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT/PATCH: Update book
    if get_role(request.user) != "administration":
        return Response(
            {"detail": "Only administration users can update books"},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method in ["PUT", "PATCH"]:
        serializer = BookSerializer(
            book,
            data=request.data,
            partial=(request.method == "PATCH"),
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Book updated successfully",
                "book": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    # DELETE: Delete book
    book.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Approves authors book
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def book_approve(request, pk):
    return set_book_status(request, pk, Book.Status.APPROVED)

# Reject an authors book
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def book_reject(request, pk):
    return set_book_status(request, pk, Book.Status.REJECTED)