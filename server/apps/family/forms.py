from django import forms

from apps.student.models import Student
from .models import AnswerFamily, AnswerMember, Family, MembershipFamily, QuestionFamily, QuestionMember



class CreateFamilyForm(forms.ModelForm):
    """Créer une nouvelle Famille"""
    class Meta:
        model = Family
        fields = ['name', 'summary']


class UpdateFamilyForm(forms.ModelForm):
    """Modifier une famille existante"""
    class Meta:
        model = Family
        fields = ['name', 'summary', 'non_subscribed_members']


class MemberForDeleteForm(forms.BaseInlineFormSet):
    def _should_delete_form(self, form):
        """Return whether or not the form was marked for deletion."""
        return form.cleaned_data.get('DELETE', False) or not form.cleaned_data.get('student', False)
        

Member2AFormset = forms.inlineformset_factory(
    parent_model=Family,
    model=MembershipFamily,
    extra=7,
    max_num=7,
    validate_max=True,
    fields=['student'],
    can_delete=True,
    formset=MemberForDeleteForm,
)


class FamilyQuestionsForm(forms.Form):

    def __init__(self, initial=None, *args, **kwargs):
        super(FamilyQuestionsForm, self).__init__(initial=initial, *args, **kwargs)
        questions = QuestionFamily.objects.all()
        for question in questions:
            name = f'question-{question.pk}'
            self.fields[name] = forms.ChoiceField(
                label = question.label,
                choices = [
                    (o.value, o.text)
                    for o in question.option_set.all()
                ],
                help_text = question.details,
                widget = forms.RadioSelect
            )
            self.fields[name].group = question.group

    def save(self, family:Family):
        """Save the answers"""
        if self.is_valid():
            answers = self.cleaned_data.items()
            print(answers)
            for question, val in answers:
                id = int(question[9:])
                try: 
                    ans = AnswerFamily.objects.get(
                        family = family,
                        question = QuestionFamily.objects.get(pk=id)
                    )
                    ans.answer = val
                    ans.save()
                except AnswerFamily.DoesNotExist:
                    AnswerFamily.objects.create(
                        answer = val,
                        family = family,
                        question = QuestionFamily.objects.get(pk=id)
                    )


class MembershipFamilyForm(forms.ModelForm):
    class Meta:
        model=MembershipFamily
        fields=('gender', 'foreign_student', 'itii')


class MemberQuestionsForm(forms.Form):

    def __init__(self, page, initial, *args, **kwargs):
        super(MemberQuestionsForm, self).__init__(initial=initial, *args, **kwargs)
        questions = QuestionMember.objects.filter(page=page)
        for question in questions:
            name = f'question-{question.pk}'
            self.fields[name] = forms.ChoiceField(
                label = question.label,
                choices = [
                    (o.value, o.text)
                    for o in question.option_set.all()
                ],
                help_text = question.details,
                widget = forms.RadioSelect
            )

    def save(self, member:MembershipFamily):
        """Save the answers"""
        if self.is_valid():
            answers = self.cleaned_data.items()
            for question, val in answers:
                id = int(question[9:])
                try: 
                    ans = AnswerMember.objects.get(
                        member = member,
                        question = QuestionMember.objects.get(pk=id)
                    )
                    ans.answer = val
                    ans.save()
                except AnswerMember.DoesNotExist:
                    AnswerMember.objects.create(
                        answer = val,
                        member = member,
                        question = QuestionMember.objects.get(pk=id)
                    )
