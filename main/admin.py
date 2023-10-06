from django.contrib import admin
from .models import User
from .models import Section, Subsection

admin.site.register(Section)
admin.site.register(Subsection)
admin.site.register(User)


