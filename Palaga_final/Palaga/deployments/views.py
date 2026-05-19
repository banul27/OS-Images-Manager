from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from images.models import OSImage

from docker.errors import NotFound

from .docker_service import restart_container, start_container, stop_container
from .models import Deployment


@login_required
def deployment_list(request):
    deployments = Deployment.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'deployments/list.html', {'deployments': deployments})


@login_required
def deploy_container(request, image_id):
    image = get_object_or_404(OSImage, id=image_id)
    try:
        container = start_container(image.docker_image)
    except Exception:
        messages.error(request, 'Failed to start.')
        return redirect('image_list')

    Deployment.objects.create(
        owner=request.user,
        image=image,
        container_id=container.id,
        status='Running',
    )
    messages.success(request, 'Container started.')
    return redirect('deployment_list')


@login_required
def stop_deployment(request, deployment_id):
    deployment = get_object_or_404(Deployment, id=deployment_id, owner=request.user)
    try:
        stop_container(deployment.container_id)
    except Exception:
        messages.error(request, 'Failed to stop. Is Docker Desktop running?')
        return redirect('deployment_list')

    deployment.status = 'Stopped'
    deployment.save()
    messages.success(request, 'Container stopped.')
    return redirect('deployment_list')


@login_required
def restart_deployment(request, deployment_id):
    deployment = get_object_or_404(Deployment, id=deployment_id, owner=request.user)
    if deployment.status == 'Running':
        messages.error(request, 'Container is already running.')
        return redirect('deployment_list')
    try:
        restart_container(deployment.container_id)
    except NotFound:
        messages.error(
            request,
            'Container no longer exists in Docker. Deploy a new one or remove this record.',
        )
        return redirect('deployment_list')
    except Exception:
        messages.error(request, 'Failed to restart. Is Docker Desktop running?')
        return redirect('deployment_list')

    deployment.status = 'Running'
    deployment.save()
    messages.success(request, 'Container restarted.')
    return redirect('deployment_list')


@login_required
def delete_deployment(request, deployment_id):
    deployment = get_object_or_404(Deployment, id=deployment_id, owner=request.user)
    if deployment.status == 'Running':
        messages.error(request, 'Stop the container before removing it from the list.')
        return redirect('deployment_list')
    deployment.delete()
    messages.success(request, 'Deployment removed from your list.')
    return redirect('deployment_list')
