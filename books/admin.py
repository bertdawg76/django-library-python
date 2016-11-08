from django.contrib import admin
from .models import Branch, Book, Shelf, Checkout, Return, UserProfile


class BookModelAdmin(admin.ModelAdmin):

    search_fields = ["book_name", "book_author", "book_shelf__genre"]

    class Meta:
        model = Book

admin.site.register(Branch)
admin.site.register(Book, BookModelAdmin)
admin.site.register(Shelf)
admin.site.register(Checkout)
admin.site.register(Return)
admin.site.register(UserProfile)
