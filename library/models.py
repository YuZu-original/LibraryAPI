from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import m2m_changed
from phonenumber_field.modelfields import PhoneNumberField


class DatesModel(models.Model):
    """`DatesModel` add `created_at` and `updated_at` fields. These fields will update automatically."""

    class Meta:
        abstract = True

    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)


class Author(DatesModel):
    """Author model"""

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    first_name = models.CharField(verbose_name="Имя", max_length=100)
    last_name = models.CharField(verbose_name="Фамилия", max_length=100)
    photo = models.ImageField(verbose_name="Фото", upload_to="author_images")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(DatesModel):
    """Book model"""

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    title = models.CharField(verbose_name="Название", max_length=100)
    description = models.TextField(verbose_name="Описание")
    page_count = models.PositiveIntegerField(verbose_name="Кол-во страниц")
    author = models.ForeignKey(Author, verbose_name="Автор", related_name="books", on_delete=models.CASCADE)
    count = models.PositiveIntegerField(verbose_name="Кол-во книг в библиотеке")

    def __str__(self):
        return self.title


class Reader(DatesModel):
    """Reader model"""

    class Meta:
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'

    first_name = models.CharField(verbose_name="Имя", max_length=100)
    last_name = models.CharField(verbose_name="Фамилия", max_length=100)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    is_active = models.BooleanField(verbose_name="Статус", default=True)
    active_books = models.ManyToManyField(Book, verbose_name="Книги", related_name="readers")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# def active_books_changed(sender, instance, action, **kwargs):
#     """When active_books changed"""
#     if instance.active_books.count() > 3:
#         raise ValidationError("You can't assign more than three active books")
#     if action == "pre_add":
#         for pk in kwargs["pk_set"]:
#             book = Book.objects.get(pk=pk)
#             if book.count == 0:
#                 raise ValidationError("You can't assign books if they are not available.")
#
#
# m2m_changed.connect(active_books_changed, sender=Reader.active_books.through)
