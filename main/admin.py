from django.contrib import admin
from .models import User
from .models import Question, Answer, Groups, Disciplin, Topic, FinalQuizsResult, QuizResult,UserDisciplineDifficulty

admin.site.register(Topic)
admin.site.register(User)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Groups)
admin.site.register(Disciplin)
admin.site.register(FinalQuizsResult)
admin.site.register(QuizResult)
admin.site.register(UserDisciplineDifficulty)


