from django.contrib import admin

from .models import OSImage


@admin.register(OSImage)
class OSImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'docker_image', 'owner', 'created_at')
    search_fields = ('name', 'docker_image')
    list_filter = ('owner',)

    def get_changeform_initial_data(self, request):
        return {'owner': request.user.pk}

    def save_model(self, request, obj, form, change):
        if not obj.owner_id:
            obj.owner = request.user
        super().save_model(request, obj, form, change)
