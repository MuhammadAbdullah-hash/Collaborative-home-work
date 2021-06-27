from django.contrib import admin
from . models import New_user , Question , Answers
# Register your models here.

admin.site.register( New_user )
admin.site.register( Question )
admin.site.register( Answers )
