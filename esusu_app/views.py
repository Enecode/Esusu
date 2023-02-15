import base64
from datetime import datetime
from django.db.models import Sum
import password as password
import requests
import username as username
from django.contrib.auth import authenticate
from rest_framework import permissions, authentication
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Group, Member, Collection, GroupAdmin, User, SavingsPreference, Contribution, CollectTable
from .serializers import UserSerializer, GroupSerializer, MemberSerializer, CollectionSerializer, \
    CollectTableSerializer, \
    GroupAdminSerializer, SavingsPreferenceSerializer, ContributionSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None):
        user = User.objects.get(id=pk)
        serializer = UserSerializer(instance=user)
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    authentication_classes = [BasicAuthentication]


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


class CollectionTableViewSet(viewsets.ModelViewSet):
    queryset = CollectTable.objects.all()
    serializer_class = CollectTableSerializer
    permission_classes = [permissions.IsAdminUser]


class GroupAdminViewSet(viewsets.ModelViewSet):
    queryset = GroupAdmin.objects.all()
    serializer_class = GroupAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


class SavingsPreferenceViewSet(viewsets.ModelViewSet):
    queryset = SavingsPreference.objects.all()
    serializer_class = SavingsPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


class ContributionViewSet(viewsets.ModelViewSet):
    queryset = Contribution.objects.all()
    serializer_class = ContributionSerializer
    permission_classes = (IsAdminUser,)

    def list(self, request):
        start_date = datetime(2023, 2, 1)
        end_date = datetime(2023, 2, 28)
        user = User.objects.get(id=1)
        contributions = CollectTable.objects.filter(
            member=user,
            contribution_date__range=(start_date, end_date),
            contribution_interval=CollectTable.CONTRIBUTION_INTERVAL_MONTHLY
        ).aggregate(Sum('contribution_amount'))

        return Response({'contributions': contributions})


class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        if not username or not password:
            return None

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if not user:
            return None

        # Return the authenticated user and token
        return user, None


def credentials(request):
    username = "username"
    password = "password"

    # Encode the credentials
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    # Include the encoded credentials in the Authorization header of the HTTP request
    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }
    # Make the API request
    response = requests.get("http://127.0.0.1:8000/group/", headers=headers)
