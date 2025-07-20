from django.contrib import admin
from django.urls import path, include
from core.views import (
    LandingView,
    MasterDetailView,
    MasterListView,
    OrderListView,
    ThanksTemplateView,
    OrderUpdateView,
    OrderCreateView,
    ReviewCreateView,
    MasterServicesView,
)
from django.conf import settings
from django.conf.urls.static import static
from users import urls as users_urls


urlpatterns = [
    path("admin/", admin.site.urls),
    path("ajax/get-master-services/", MasterServicesView.as_view(), name="get_master_services"),
    path("", LandingView.as_view(), name="landing"),
    path("masters/", MasterListView.as_view(), name="master_list"),
    path("masters/<int:master_id>/", MasterDetailView.as_view(), name="master_detail"),
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
    path("orders/update/<int:order_id>/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/", OrderListView.as_view(), name="order_list"),
    path("thanks/", ThanksTemplateView.as_view(), name="thanks"),
    path("reviews/create/", ReviewCreateView.as_view(), name="review_create"),

    # Пользователи
    path("users/", include(users_urls)),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
