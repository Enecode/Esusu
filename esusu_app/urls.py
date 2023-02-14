from django.urls import path, include
from rest_framework import routers

from .views import GroupViewSet, MemberViewSet, CollectionViewSet, GroupAdminViewSet, UserViewSet, \
    SavingsPreferenceViewSet, ContributionViewSet, CollectionTableViewSet

app_name = 'esusu_app'
router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'group', GroupViewSet)
router.register(r'member', MemberViewSet)
router.register(r'collection', CollectionViewSet)
router.register(r'collectTable', CollectionTableViewSet)
router.register(r'contribution', ContributionViewSet)
router.register(r'groupadmin', GroupAdminViewSet)
router.register(r'savings', SavingsPreferenceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
