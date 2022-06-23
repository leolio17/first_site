from django.contrib import admin

# Register your models here.
from .models import Answer, Question

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject', 'content']

class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['content']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)

#admin.site.register(Question)
#admin.site.register(Answer)
