from phonenumber_field.phonenumber import PhoneNumber
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from library.models import Author, Book, Reader


class PhoneNumberValidator:
    def __init__(
        self,
        country_code: int,
        min_national_number: int = 0,
        max_national_number: int = 10_000_000_000,
    ):
        self.country_code = country_code
        self.min_national_number = min_national_number
        self.max_national_number = max_national_number

    def __call__(self, value):
        if value.country_code != self.country_code:
            raise ValidationError("Invalid phone number country code")
        if not (
            self.min_national_number < value.national_number < self.max_national_number
        ):
            raise ValidationError("Invalid phone number len")


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "first_name", "last_name", "photo")


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "description", "page_count", "author", "count")


class ReaderSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(validators=[PhoneNumberValidator(7, 999_999_999)])

    def create(self, validated_data):
        # validate active books
        books = validated_data.get("active_books", [])
        for book in books:
            if book.count <= 0:
                raise ValidationError(
                    "You can't assign books if they are not available"
                )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # validate active books
        books = validated_data.get("active_books", [])
        for book in books:
            if (
                book.count <= 0
                and not instance.active_books.filter(id=book.id).exists()
            ):
                raise ValidationError(
                    "You can't assign books if they are not available"
                )
        return super().update(instance, validated_data)

    def validate(self, attrs):
        books = attrs.get("active_books")
        if books and len(books) > 3:
            raise ValidationError("Max count active books 3")
        return super().validate(attrs)

    class Meta:
        model = Reader
        fields = (
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "is_active",
            "active_books",
        )
