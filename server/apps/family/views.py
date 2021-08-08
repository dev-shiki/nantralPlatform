from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date

from apps.group.views import DetailGroupView
from .models import Affichage, AnswerMember, QuestionMember, QuestionFamily


# Create your views here.

class HomeFamilyView(LoginRequiredMixin, TemplateView):
    """Page d'accueil de l'appli Parrainage"""

    template_name = 'family/home.html'

    def get_context_data(self, **kwargs):
        student = self.request.user.student
        try:
            phase = Affichage.objects.first().phase
        except Exception:
            Affichage().save()
            phase = Affichage.objects.first().phase
        context = {}
        context['phase'] = phase
        context['user_family'] = student.family.first()
        if context['user_family']:
            context['is_2Aplus'] = (student.membershipfamily.first().role == '2A+')
            context['1A_members'] = context['user_family'].memberships.filter(role='1A')
        else:
            context['is_2Aplus'] = (student.promo < date.today().year)
            context['1A_members'] = None
        # nombre de questions complétées
        nb_done = AnswerMember.objects.filter(member__student=student).count()
        nb_tot = QuestionMember.objects.all().count()
        nb_fam_only = QuestionFamily.objects.filter(quota=100).count()
        context['form_complete'] = (nb_done == (nb_tot - nb_fam_only*int(context['is_2Aplus'])))

        return context


class ListFamilyView(ListView):
    pass

class CreateFamilyView(TemplateView):
    pass

class QuestionnaryView(TemplateView):
    pass

class DetailFamilyView(DetailGroupView):
    pass