from django.urls import include, path
from rest_framework.routers import SimpleRouter

from orcamento import views

router = SimpleRouter()
router.register('receitas', views.ReceitaViewSet)

app_name = 'receita'

urlpatterns = [
    path('', include(router.urls)),
]
