from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet, EtiquetaViewSet

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'etiquetas', EtiquetaViewSet)

urlpatterns = [
    path('api/inventario/', include(router.urls)),
] 