from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from deployments.models import Deployment

from .models import OSImage


def home(request):
    return redirect('image_list')


@login_required
def image_list(request):
    images = OSImage.objects.all().order_by('name')
    image_rows = []
    for image in images:
        latest = (
            Deployment.objects.filter(owner=request.user, image=image)
            .order_by('-created_at')
            .first()
        )
        if latest and latest.status == 'Running':
            deploy_status = 'Running'
        elif latest:
            deploy_status = 'Stopped'
        else:
            deploy_status = None
        image_rows.append({'image': image, 'deploy_status': deploy_status})
    return render(request, 'images/list.html', {'image_rows': image_rows})
