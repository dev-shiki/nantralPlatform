from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from apps.roommates.models import Housing, Roommates, NamedMembershipRoommates
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, UpdateView, DetailView
import locale

from django.conf import settings

from apps.roommates.models import Housing


class HousingMap(LoginRequiredMixin, TemplateView):
    template_name = 'roommates/housing/map.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['MAPBOX_API_KEY'] = settings.MAPBOX_API_KEY
        return context


class HousingDetailView(LoginRequiredMixin, DetailView):
    template_name = 'roommates/housing/detail.html'
    model = Housing

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['Roommates'] = Roommates.objects.filter( housing = self.object.pk).order_by('-begin_date')

        list_roommates = []
        context['roommates_groups'] = Roommates.objects.filter(housing=self.object.pk).order_by('-begin_date')

        locale.setlocale(locale.LC_TIME,'')
        for group in context['roommates_groups']: 
            member_list=[]

            #On met les dates en français et au bon format.
            begin_date = str(group.begin_date.strftime('%d/%m/%Y'))
            end_date = str(group.end_date.strftime('%d/%m/%Y')) if group.end_date is not None else None
            
            #On évite d'afficher None si la date de fin n'est pas renseignée
            duration="Du " + begin_date + " au " + end_date if group.end_date is not None else "Depuis le " + begin_date + " (date de fin non renseignée)"

            for member in NamedMembershipRoommates.objects.filter(roommates=group.id):
                #On évite d'afficher un None si le coloc n'a pas de surnom
                nicknm="" if member.nickname is None else member.nickname

                member_list.append({
                'first_name': member.student.first_name,
                'last_name' : member.student.last_name,
                'nickname' : nicknm,
                })
            list_roommates.append({'name': group.name, 'description' : group.description, 'duration' : duration,'members': member_list})
        context['roommates_groups'] = list_roommates

        return context


class CreateHousingView(LoginRequiredMixin, TemplateView):
    template_name = 'roommates/housing/create.html'


class EditHousingView(LoginRequiredMixin, UpdateView):
    template_name = 'roommates/housing/edit.html'
    model = Housing
    fields = ['details']
