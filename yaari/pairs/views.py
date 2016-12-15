import datetime

from django.db.models import Min
from django.views.generic.base import TemplateView

from models import PairCall
from utils import get_pair_week, get_pair_week_label, get_paircall_metadata


class ActivePairsView(TemplateView):
    """ Returns a data of all the active pairs of the current week"""
    template_name = 'active_pairs.html'

    def get_context_data(self, **kwargs):
        """ Info of an Active Pair is passed on as a list
        [pair, Status of pairs calls for that pair in that week]
        """
        context = {}
        monday, friday = get_pair_week(datetime.date.today())
        context["pair_week_label"] = get_pair_week_label(monday, friday)
        pair_calls = PairCall.objects.filter(date__range= [monday, friday]).order_by('date')
        active_pairs = {}
        for pair_call in pair_calls:
            pair = pair_call.pair
            if active_pairs.has_key(pair):
                active_pairs[pair].append(pair_call.is_done)
            else:
                active_pairs[pair] = [pair, pair_call.is_done]
        context["active_pairs"] = active_pairs
        return context


class HistoryView(TemplateView):
    """
    Returns the list of all the pairs and pair calls, historically.

    Its sorted in reverse chronological order

    The data is passed as 4 level nested list.

    First level (lowest) -> Meta data of a paircall -> [Paircall status, Paircall Image, Paircall Caption]
    If Image or Caption is empty, then put False

    Second level -> Pair activity for that week -> [Employee one picture, employee two picture,
    List of paircall metadata between those employees in that week]

    Third level -> Data of entire activity in a week -> [Pair week label, List of Pair Activities]

    Fourth level -> Entire history -> [List of Weekly Activities]

    """
    template_name = 'history.html'

    def get_context_data(self, **kwargs):
        context = {}

        today = datetime.date.today()

        #As its historical data, we don't consider current week's activity
        last_week_monday = today - datetime.timedelta(days=7 + today.weekday())

        first_paircall_date = PairCall.objects.all().aggregate(first_paircall_date=Min('date'))["first_paircall_date"]
        first_monday = first_paircall_date - datetime.timedelta(days=first_paircall_date.weekday())

        historical_activity = []
        for i in range(0, (last_week_monday - first_monday).days + 1, 7):
            monday = last_week_monday - datetime.timedelta(i)
            friday = monday + datetime.timedelta(5)
            pair_week_label = get_pair_week_label(monday, friday)
            pair_calls = PairCall.objects.filter(date__range= [monday, friday]).order_by('date')
            week_activity = {}
            for pair_call in pair_calls:
                pair = pair_call.pair
                if week_activity.has_key(pair):
                    week_activity[pair][2].append(get_paircall_metadata(pair_call))
                else:
                    week_activity[pair] = [pair.employee_one.profile_pic.url, pair.employee_two.profile_pic.url]
                    week_activity[pair].append([get_paircall_metadata(pair_call)])
            if week_activity:
                historical_activity.append([pair_week_label, week_activity.values()])

        context["data"] = historical_activity
        return context


class HistoryView(TemplateView):

