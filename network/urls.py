from django.urls import path
from .views import alumni_list, alumni_api, alumni_detail

urlpatterns = [
    path("", alumni_list, name="home"),
    path("api/alumni/", alumni_api, name="alumni-api"),
    path("alumni/<int:alumni_id>/", alumni_detail, name="alumni-detail"),
]
