from django.contrib import admin
from .models import User
from .models import Section, Subsection, Test, UserTestResult, Question, Answer

admin.site.register(Section)
admin.site.register(Subsection)
admin.site.register(User)
admin.site.register(Test)
admin.site.register(UserTestResult)
admin.site.register(Question)
admin.site.register(Answer)
