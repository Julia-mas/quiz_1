from django.contrib import admin

from .models import Choice, Exam, Question, Result
from .forms import ChoicesInlineFormset, QuestionInlineFormset


class ChoicesInline(admin.TabularInline):
    model = Choice
    fields = ('text', 'is_correct')
    show_change_link = True
    extra = 0
    formset = ChoicesInlineFormset


class QuestionAdmin(admin.ModelAdmin):
    inlines = (ChoicesInline,)


class QuestionInline(admin.TabularInline):
    model = Question
    fields = ('text', 'order_num')
    show_change_link = True
    extra = 0
    ordering = ('order_num', )


class ExamAdmin(admin.ModelAdmin):
    readonly_fields = ['uuid']
    inlines = (QuestionInline,)
    formset = QuestionInlineFormset


admin.site.register(Exam, ExamAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Result)
