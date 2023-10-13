from django.contrib import admin
from .models import User
from .models import Section, Subsection, Question, Answer, TestResult, Groups, Disciplin

admin.site.register(Section)
admin.site.register(Subsection)
admin.site.register(User)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(TestResult)
admin.site.register(Groups)
admin.site.register(Disciplin)


