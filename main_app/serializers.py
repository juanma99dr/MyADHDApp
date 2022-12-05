from rest_framework import serializers
from .models import Pomodoro, User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', )

class PomodoroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pomodoro
        fields = ('pomodoro_id', 'duration', 'user', )