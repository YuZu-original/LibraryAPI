from phonenumber_field.phonenumber import PhoneNumber
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from library.models import Author, Book, Reader


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "first_name", "last_name", "photo")


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "description", "page_count", "author", "count")


class ReaderSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # validate active books
        books = validated_data.get("active_books", [])
        for book in books:
            if book.count <= 0:
                raise ValidationError("You can't assign books if they are not available")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # validate active books
        books = validated_data.get("active_books", [])
        for book in books:
            if book.count <= 0 and not instance.active_books.filter(id=book.id).exists():
                raise ValidationError("You can't assign books if they are not available")
        return super().update(instance, validated_data)

    def validate(self, attrs):
        self.__validate_phone_number(attrs.get('phone_number'))
        self.__validate_books_count(attrs.get("active_books"))
        return super().validate(attrs)

    @staticmethod
    def __validate_phone_number(phone_number_raw: str):
        phone_number = PhoneNumber.from_string(phone_number=phone_number_raw)
        if phone_number.country_code != 7:
            raise ValidationError("Invalid phone number country code")
        if not (999_999_999 < phone_number.national_number < 10_000_000_000):
            raise ValidationError("Invalid phone number len (not 11)")

    @staticmethod
    def __validate_books_count(books: list):
        if len(books) > 3:
            raise ValidationError("Max count active books 3")

    class Meta:
        model = Reader
        fields = ("id", "first_name", "last_name", "phone_number", "is_active", "active_books")
