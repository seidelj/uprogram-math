from rest_framework import serializers
from mathtutor.models import Result, ParentFormResult
from django.contrib.auth.models import User

class ResultSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.ReadOnlyField(source="name.username")
    quiz = serializers.ReadOnlyField(source="quiz.q_id")

    class Meta:
        model = Result
        fields = ('name', 'response_id', 'score', 'finished', 'quiz')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    result_set = serializers.HyperlinkedRelatedField(many=True, queryset=Result.objects.all(), view_name='result-detail')

    class Meta:
        model = User
        fields = ('id', 'username', 'result_set')

class ParentFormSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.ReadOnlyField(source="student.username")

    class Meta:
        model = ParentFormResult
        fields = ('student', 'response_id', 'completeBool', 'qualtrics_id')
