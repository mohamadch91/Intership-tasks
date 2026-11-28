from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from users.models import User
from books.models import Book


class BookTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_user(
            phone="07111111111",
            first_name="Admin",
            last_name="User",
            password="Test123456!",
            role="administration",
        )

        self.client.force_authenticate(user=self.admin)

        self.book = Book.objects.create(
            title="Harry Potter",
            author_name="J.K. Rowling",
            isbn="1234567890123",
            description="A fantasy novel",
            genre="Fantasy",
            total_copies=5,
            available_copies=5,
            status=Book.Status.APPROVED,
        )

    # Test 1: List all books
    def test_list_books(self):
        url = reverse("book-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Harry Potter")

    # Test 2: Get a specific book
    def test_get_book_detail(self):
        url = reverse("book-detail", kwargs={"pk": self.book.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Harry Potter")

    # Test 3: Add a book
    def test_add_book(self):
        url = reverse("book-list")

        data = {
            "title": "The Hobbit",
            "author_name": "J.R.R. Tolkien",
            "isbn": "1234567890124",
            "description": "A fantasy adventure",
            "genre": "Fantasy",
            "total_copies": 4,
            "available_copies": 4,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(response.data["book"]["title"], "The Hobbit")

    # Test 4: Update a book
    def test_update_book(self):
        url = reverse("book-detail", kwargs={"pk": self.book.pk})

        data = {
            "title": "Harry Potter 2",
        }

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["book"]["title"],
            "Harry Potter 2",
        )

        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Harry Potter 2")


    # Test 5: Delete a book
    def test_delete_book(self):
        url = reverse("book-detail", kwargs={"pk": self.book.pk})

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Book.objects.filter(pk=self.book.pk).exists()
        )
