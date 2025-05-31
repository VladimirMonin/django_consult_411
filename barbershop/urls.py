from django.contrib import admin
from django.urls import path
from core.views import index, master_detail, master_list, order_list
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),
    path("masters/", master_list, name="master_list"),
    path("masters/<int:master_id>/", master_detail),
    path("orders/", order_list, name="order_list"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
