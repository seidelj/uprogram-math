from django.conf.urls import url, include, patterns
from rest_framework import routers
from rest_api import views

SECURE_SSL_REDIRECT=True

router = routers.DefaultRouter()
router.register(r'results', views.ResultViewSet, base_name="results-list")
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace="rest_framework")),
]
