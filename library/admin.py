from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import When, Case, Value
from django.urls import reverse
from django.utils.safestring import mark_safe

from library.models import Author, Book, Reader


class DatesAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Author)
class AuthorAdmin(DatesAdmin):
    list_display = ("first_name", "last_name")


@admin.register(Book)
class BookAdmin(DatesAdmin):
    list_display = ('title', 'author_link', 'count')
    readonly_fields = ('author_link', 'created_at', 'updated_at')
    actions = ("reset_count",)

    def author_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:library_author_change", args=(obj.author.pk,)),
            obj.author
        ))

    author_link.short_description = 'Автор'

    @admin.action(description='Set count of books to zero')
    def reset_count(self, request, queryset):
        queryset.update(count=0)


class ReaderForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = '__all__'

    def clean(self):
        active_books = self.cleaned_data.get('active_books')
        if active_books:
            if active_books.count() > 3:
                raise ValidationError("You can't assign more than three active books")
            for book in active_books:
                if book.count <= 0:
                    if self.instance.id and self.instance.active_books.filter(id=book.id).exists():
                        # Если эта книга уже принадлежала пользователю - не вызываем ошибку
                        continue
                    raise ValidationError("You can't assign books if they are not available.")
        return self.cleaned_data


@admin.register(Reader)
class ReaderAdmin(DatesAdmin):
    form = ReaderForm
    list_filter = ("is_active",)
    list_display = ("first_name", "last_name", "phone_number", "is_active", "active_books_links")
    actions = ("change_status", "clear_books")

    def active_books_links(self, obj):
        return mark_safe(" | ".join('<a href="{}">{}</a>'.format(
            reverse("admin:library_book_change", args=(b.pk,)),
            b.title
        ) for b in obj.active_books.all()))

    active_books_links.short_description = 'Активные книги'

    @admin.action(description='Changes the is_active field of the selected readers')
    def change_status(self, request, queryset):
        queryset.update(is_active=Case(
            When(is_active=True, then=Value(False)),
            When(is_active=False, then=Value(True)),
        ))

    @admin.action(description='Clear all books for selected readers')
    def clear_books(self, request, queryset):
        for obj in queryset:
            for book in obj.active_books.all():
                book.count += 1
                book.save()
            obj.active_books.clear()
            obj.save()
