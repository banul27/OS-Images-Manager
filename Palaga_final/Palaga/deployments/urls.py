from django.urls import path

from .views import (
    delete_deployment,
    deploy_container,
    deployment_list,
    restart_deployment,
    stop_deployment,
)

urlpatterns = [
    path('', deployment_list, name='deployment_list'),
    path('deploy/<int:image_id>/', deploy_container, name='deploy_container'),
    path('stop/<int:deployment_id>/', stop_deployment, name='stop_deployment'),
    path('restart/<int:deployment_id>/', restart_deployment, name='restart_deployment'),
    path('delete/<int:deployment_id>/', delete_deployment, name='delete_deployment'),
]
