from user.models import User,Favourites
from rest_framework import serializers
from tours.serializers import ToursSerializer
from events.serializers import EventsSerializer
from eventsdate.serializers import MeetingSerializer

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Пароли не совпадают.")
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class CompanyRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password', 'phone_number', 'doc')

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Пароли не совпадают.")
        return data

    def create(self, validated_data):
        
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            doc=validated_data.get('doc', '')
        )
        user.set_password(validated_data['password'])
        user.role = 'company'
        user.save()
        return user 

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','name', 'last_name', 'email', 'photo', 'phone_number','gender','date_of_birth')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','name','password', 'last_name', 'email', 'photo', 'phone_number','gender','date_of_birth','doc')


class FavouritesSerializer(serializers.ModelSerializer):
    events = EventsSerializer()  
    

    class Meta:
        model = Favourites
        fields = '__all__' 