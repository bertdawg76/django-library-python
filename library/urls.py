"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from books import views
from django.conf.urls.static import static
from django.conf import settings
from books.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'book', views.BookViewSet)
router.register(r'branch', views.BranchViewSet)
router.register(r'shelf', views.ShelfViewSet)
router.register(r'checkout', views.CheckoutViewSet)
router.register(r'return', views.ReturnViewSet)
router.register(r'register', views.UserCreateAPIView)
router.register(r'userprofile', views.UserProfileViewSet)
router.register(r'reshelf', views.ReShelvingViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_auth_token)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



