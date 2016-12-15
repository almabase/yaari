import datetime

from models import PairCall


def get_pair_week(call_date):
    """
    Sat-Fri, is considered one unit.

    So, if the call_date is Sat or Sun, it's pair week is coming Mon - coming Fri.

    If the call_date is a weekday, then it's current week's Mon - current week's Fri

    """
    weekday = call_date.weekday()
    if weekday >= 5: #saturday or Sunday
        monday = call_date + datetime.timedelta(days=7 - weekday) #Coming Monday
    else:
        monday = call_date - datetime.timedelta(days=weekday) # Current Week Monday
    return monday, monday + datetime.timedelta(days=4) #Monday, Friday


def get_pair_week_label(monday, friday):
    """
    String representation of the week
    (Dec 19, 2016, Dec 23, 2016) -> "Dec 19-23"
    (Sep 29, 2016, Oct 2, 2016) -> "Sep 29 - Oct 2"
    """

    if monday.month == friday.month:
        return "%s %s-%s" % (monday.strftime("%b"), monday.day, friday.day)
    else:
        return "%s %s - %s %s" % (monday.strftime("%b"), monday.day, friday.strftime("%b"), friday.day)


def get_paircall_metadata(paircall):
    """
    Meta data of a paircall -> [Paircall status, Paircall Image, Paircall Caption]
    If Image or Caption is empty, then put False
    """
    return [paircall.is_done, paircall.picture.url if paircall.picture else False,
                paircall.caption if paircall.caption else False]

def get_pair_from_employees(emp1, emp2):
    return Pair.objects.filter(employee_one__in = [emp1, emp2], employee_two__in = [emp1, emp2])[0]

def get_time_elapsed(emp1, emp2):
    pair = get_pair_from_employees(emp1, emp2)

    paircalls = PairCall.objects.filter(pair=pair).order_by('-date')

    if paircalls:
        today = datetime.date.today()
        last_call_date = paircalls[0].date
        return (today - last_call_date).days
    else:
        return -1


def populate_interaction_analytics():
    for tl in TimeLapse.objects.all():
        tl.objects.save()
    pass

def generate_pairs(week_starting_date):

    """
    Create a 'Last interaction' table

    For every pair, store the below two details
        - the last time they have spoken to each other,
        - if they are from the same team

    For an employee from randomized employee pool:

        - randomly try to pick a diff team member that he has never spoken to
        - If failure, randomly try to pick a same team member he has never spoken to
        - If failure, find the list of employees with longest interaction gap
        - randomly try to pick a diff team member from above list
        - If failure, randomly pick a same team member from above list

    - At anypoint, if success, remove that matched team member from the pool and loop
    """

    populate_interaction_analytics()


