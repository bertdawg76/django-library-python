from django.core.management.base import BaseCommand, CommandError
from books.models import Book
import csv
# from books.management.commands import books.csv
filepathname = '/Users/bertcoleman/anaconda/envs/library/library/books/management/commands/books.csv'

class Command(BaseCommand):
    help = 'populate database with books from text file'

    def handle(self, *args, **options):

        infoReader = csv.reader(open(filepathname), delimiter=',')

        for row in infoReader:
            if Book.objects.filter(book_name=row[0].strip(), book_author=row[1].strip()).exists():
                print('already exists', row[0])
            else:
                bookinfo = Book(
                    book_name=row[0].strip(),
                    book_author=row[1].strip(),
                    book_isbn=row[2].strip(),
                    book_genre=row[3].strip()
                    )

                bookinfo.save()



