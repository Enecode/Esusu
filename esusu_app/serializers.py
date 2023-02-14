from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User, Group, Member, Collection, GroupAdmin, SavingsPreference, CollectTable, Contribution


class PasswordField(serializers.CharField):
    def to_internal_value(self, data):
        return make_password(data)

    def to_representation(self, value):
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'gender',
            'marital_status',
            'address',
            'email',
            'username',
            'password',
            'phone_number',
            'state_of_origin',
            'state_of_residence'
        ]
        password = PasswordField(write_only=True)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["name", "description", "admin", "members", "max_capacity", "is_public", "is_searchable"]


class SavingsPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsPreference
        fields = ["user", 'periodic_amount']


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ["name", "group", "username"]


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["amount", "date", "member", "group"]


class GroupAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupAdmin
        fields = ["group", "collection_table", "contribution"]


class CollectTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectTable
        fields = ["member", "contribution_amount", "contribution_interval", "contribution_date", "group"]


class ContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = ["member", "amount", "interval", "date", "group"]
