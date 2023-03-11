from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.safestring import mark_safe

from library.models import Author, Book, Reader


class DatesAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


class BookAdmin(DatesAdmin):
    list_display = ('title', 'author_link', 'count')
    readonly_fields = ('author_link', 'created_at', 'updated_at')

    def author_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:library_author_change", args=(obj.author.pk,)),
            obj.author
        ))

    author_link.short_description = 'Автор'


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
                if book.count == 0:
                    raise ValidationError("You can't assign books if they are not available.")
        return self.cleaned_data


class ReaderAdmin(DatesAdmin):
    form = ReaderForm


admin.site.register(Author, DatesAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Reader, ReaderAdmin)
