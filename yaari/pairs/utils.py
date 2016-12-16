import datetime
import itertools

from models import PairCall, Employee, Pair


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
    return [paircall.is_done, paircall.picture.url if paircall.picture else "",
                paircall.caption if paircall.caption else ""]

def get_pair_from_employees(emp1, emp2):
    return Pair.objects.filter(employee_one__in = [emp1, emp2], employee_two__in = [emp1, emp2])[0]


def populate_new_pairs():
    employees_set = Employee.objects.all().values_list("id", flat=True)
    all_pairs_iter = itertools.combinations(employees_set, 2)

    current_pairs = []
    for pair in Pair.objects.all():
        current_pairs.append(set((pair.employee_one.id, pair.employee_two.id)))

    for pair in all_pairs_iter:
        if not set(pair) in current_pairs:
            Pair.objects.create(employee_one_id = pair[0], employee_two_id = pair[1])