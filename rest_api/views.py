from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions, serializers
from mathtutor.models import Result, ParentFormResult
from rest_api.serializers import ResultSerializer, UserSerializer, ParentFormSerializer
from django.contrib.auth.models import User
import datetime
from rest_api.permissions import IsSSL

# Create your views here.

class ResultViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ResultSerializer
    permission_classes = (IsSSL, permissions.IsAuthenticated,)

    def get_queryset(self):
        timestamp = datetime.datetime.now() - datetime.timedelta(hours=6)
        queryset = Result.objects.filter(timestamp__gte=timestamp)
        getAllResults = self.request.query_params.get('allResults', None)
        site = self.request.query_params.get('site', None)
        if getAllResults and not site:
            queryset = Result.objects.all()
        elif not getAllResults and site:
            queryset = Result.objects.filter(timestamp__gte=timestamp).filter(quiz__site=site)
        elif not getAllResults and not site:
            queryset = Result.objects.filter(timestamp__gte=timestamp)
        else:
            queryset = Result.objects.filter(site=site)

        return queryset

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSSL, permissions.IsAuthenticated,)

class ParentFormViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ParentFormResult.objects.all()
    serializer_class = ParentFormSerializer
    permission_classes = (IsSSL, permissions.IsAuthenticated,)
