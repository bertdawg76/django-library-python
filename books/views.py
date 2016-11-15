from django.db.models import Q
from django.contrib.auth import get_user_model
from .serializers import UserCreateSerializer
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from datetime import timedelta, datetime
from books.serializers import BookSerializer, BranchSerializer, CheckoutSerializer, \
    ReturnSerializer, ShelfSerializer, UserProfileSerializer
from books.models import Book, Branch, Checkout, Shelf, Return, UserProfile
from .permissions import IsAllowed, OnlyLibrarian
from .pagination import BookLimitOffsetPagination
from rest_framework.authtoken.views import ObtainAuthToken as OriginalObtain
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from django.http import HttpResponseRedirect


User = get_user_model()

class ObtainAuthToken(OriginalObtain):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'id': user.id, 'Librarian': user.isLibrarian})


obtain_auth_token = ObtainAuthToken.as_view()



class UserCreateAPIView(viewsets.ModelViewSet):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class BranchViewSet(viewsets.ModelViewSet):

    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class BookViewSet(viewsets.ModelViewSet):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookLimitOffsetPagination

    # filter_backends = [SearchFilter]
    # search_fields = ['book_author', 'book_name', 'book_shelf']
    # permission_classes = (IsAllowed, )

    def get_queryset(self, *args, **kwargs):

        queryset_list = Book.objects.all()
        query = self.request.query_params.get("search")

        if query:
            queryset_list = queryset_list.filter(
                Q(book_author__icontains=query) |
                Q(book_name__icontains=query) |
                Q(book_shelf__genre__icontains=query)

            ).distinct()
        return queryset_list

    @detail_route(methods=['POST'], permission_classes=(OnlyLibrarian, ))

    def reshelf(self, request, *args, **kwargs):
        book = self.get_object()
        book.is_available = True
        book.save()

        print(book)
        return Response('success')

    @list_route(methods=['POST'])

    def upload_book(self, request):
        print(self.request.data)
        if self.request.data['isLibrarian']:
            shelf = Shelf.objects.get(id=request.data['book_shelf'])
            book = Book(
                book_name=self.request.data['book_name'],
                book_author=self.request.data['book_author'],
                book_isbn=self.request.data['book_isbn'],
                book_genre=self.request.data['book_genre'],
                book_image=self.request.data['book_image'],
                book_shelf=shelf,
            )

            book.save()
        return HttpResponseRedirect('http://127.0.0.1:3000/bookdisplay')




class CheckoutViewSet(viewsets.ModelViewSet):

    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer
    permission_classes = (IsAllowed, )
    # pagination_class = BookLimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user

        if user.isLibrarian:
            return Checkout.objects.all().order_by('user')

        # user = self.request.user
        return Checkout.objects.filter(user=user).order_by('-issue_date')

    def create(self, request, *args, **kwargs):
        a = super().create(request, *args, **kwargs)
        print(a.data)
        d = timedelta(days=12)
        checkout = Checkout.objects.get(id=a.data['id'])
        available = Book.objects.get(id=a.data['book'])

        available.is_available = False

        calculate_date = checkout.issue_date + d

        checkout.due_date = calculate_date

        available.save()
        checkout.save()
        print(calculate_date)
        print(d)
        print(checkout.due_date)
        return a


class ShelfViewSet(viewsets.ModelViewSet):

    queryset = Shelf.objects.all()
    serializer_class = ShelfSerializer


class ReShelvingViewSet(viewsets.ModelViewSet):

    queryset = Return.objects.all()
    serializer_class = ReturnSerializer
    permission_classes = (OnlyLibrarian,)
    # pagination_class = BookLimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def get_queryset(self):
    #     user = self.request.user
    #     return Return.objects.filter(user=user).order_by('-return_date')

    def get_queryset(self):
        user = self.request.user

        if user.isLibrarian:
            return Return.objects.all().order_by('user')

        return Return.objects.filter(user=user).order_by('-return_date')

    # def update(self, request, *args, **kwargs):
    #     d = super().create(request, *args, **kwargs)
    #     print(d.data)
    #
    #     book_available = Book.objects.get(id=d.data['book'])
    #     book_available.is_available = True
    #
    #     book_available.patch()
    #
    #     return d


class ReturnViewSet(viewsets.ModelViewSet):

    queryset = Return.objects.all()
    serializer_class = ReturnSerializer
    # pagination_class = BookLimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Return.objects.filter(user=user).order_by('-issue_date')

    def create(self, request, *args, **kwargs):
        c = super().create(request, *args, **kwargs)
        print(c.data)
        checkedoutbook = Checkout.objects.get(id=c.data['checkouts'])
        changetoavailable = Book.objects.get(id=c.data['book'])
        # changetoavailable.is_available = True
        checkedoutbook.return_date = datetime.now()
        # changetoavailable.save()
        checkedoutbook.save()
        print(checkedoutbook)

        return c

    # def create(self, request, *args, **kwargs):
    #     d = super().create(request, *args, **kwargs)
    #     print(d.data)
    #     changetoavailable = Book.objects.get(id=d.data['book'])
    #
    #     changetoavailable.is_available = True
    #
    #     changetoavailable.save()
    #     print(changetoavailable)
    #     print(changetoavailable.is_available)
    #     return d


class UserProfileViewSet(viewsets.ModelViewSet):

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    #
    # def get_queryset(self):
    #     user = self.request.user
    #     return UserProfile.objects.filter(username=user)