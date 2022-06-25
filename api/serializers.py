from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from inspects.models import Image
from drf_extra_fields.fields import Base64ImageField

class ImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    # username = serializers.SerializerMethodField()
    class Meta:
        model = Image
        fields = ('title', 'image')
    def create(self, validated_data):
        image     = validated_data.pop('image')
        title     = validated_data.pop('title')
        # username  = validated_data['username']
        # user = User.objects.filter(username__icontains=username) 
        # return Image.objects.create(owner=user,image=image,title=title)
        return Image.objects.create(image=image,title=title)
    

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user