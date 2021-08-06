from django.contrib import admin
from .models import *

# Register your models here.


#familles
class AnswerFamilyInline(admin.TabularInline):
    model=AnswerFamily
class FamilyAdmin(admin.ModelAdmin):
    inlines=[AnswerFamilyInline]
admin.site.register(Family, FamilyAdmin)


#members
class AnswerMemberInline(admin.TabularInline):
    model=AnswerMember
class MembershipFamilyAdmin(admin.ModelAdmin):
    inlines=[AnswerMemberInline]
admin.site.register(MembershipFamily, MembershipFamilyAdmin)


# questions
class OptionInline(admin.TabularInline):
    model = Option
class QuestionMemberAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
class QuestionFamilyAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
admin.site.register(QuestionMember, QuestionMemberAdmin)
admin.site.register(QuestionFamily, QuestionFamilyAdmin)
admin.site.register(QuestionGroup)

