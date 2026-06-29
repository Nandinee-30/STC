# Register your models here.
from django.contrib import admin
from .models import Reg , StudentLogin , AdminLogin,LORSubmission,FeesChallan,BatchAllotment,ContactMessage,Certificate


admin.site.register(Reg)
admin.site.register(StudentLogin)
admin.site.register(AdminLogin)
admin.site.register(LORSubmission)
admin.site.register(FeesChallan)
admin.site.register(BatchAllotment)
admin.site.register(ContactMessage)
admin.site.register(Certificate)
class Certificate(admin.ModelAdmin):
    list_display = ('certificate_number', 'rollno', 'name', 'created_at')
    search_fields = ('certificate_number', 'rollno', 'name')
    list_filter = ('created_at',)
