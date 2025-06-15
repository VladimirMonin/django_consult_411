from django.contrib import admin
from django.urls import path
from core.views import (
    index,
    landing,
    master_detail,
    master_list,
    order_list,
    thanks,
    order_create,
)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", landing, name="landing"),
    path("index/", index, name="index"),
    path("masters/", master_list, name="master_list"),
    path("masters/<int:master_id>/", master_detail, name="master_detail"),
    path("orders/create/", order_create, name="order_create"),
    path("orders/", order_list, name="order_list"),
    path("thanks/", thanks, name="thanks"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
