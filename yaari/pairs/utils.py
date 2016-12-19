import datetime
import itertools
import random
import pdb

from django.db.models import Max

from models import PairCall, Employee, Pair, TimeLapse


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
    """
    Generate all the missing pairs.

    This function is needed to ensure that pairs table is updated whenever a new employee is added

    It creates a list of all the possible pairs and all the current pairs.

    Then compares the two lists and used the diff to create the missing pairs.
    :return:
    """

    employees_set = Employee.objects.all().values_list("id", flat=True)
    all_pairs_iter = itertools.combinations(employees_set, 2)

    current_pairs = []
    for pair in Pair.objects.all():
        current_pairs.append(set((pair.employee_one.id, pair.employee_two.id)))

    for pair in all_pairs_iter:
        if not set(pair) in current_pairs:
            Pair.objects.create(employee_one_id = pair[0], employee_two_id = pair[1])

def is_same_team(emp_one, emp_two):
    return emp_one.team == emp_two.team

def create_timelapse_for_pair(emp_one, emp_two, is_same_team, time_lapse_in_days):
    """
    For ease of filtering, every pair will be stored twice
    """
    TimeLapse.objects.create(primary_employee=emp_one, secondary_employee=emp_two,
                             is_same_team=is_same_team, time_lapse_in_days=time_lapse_in_days)
    TimeLapse.objects.create(primary_employee=emp_two, secondary_employee=emp_one,
                             is_same_team=is_same_team, time_lapse_in_days=time_lapse_in_days)


def find_pair(emp_one, emp_two):
    pl = Pair.objects.filter(employee_one__in = [emp_one, emp_two],
                             employee_two__in = [emp_one, emp_two])

    if pl:
        return pl[0]
    else:
        return None


def populate_timelapse_table():
    """
    Delete the table and re-populate it
    """

    TimeLapse.objects.all().delete()

    for pair in Pair.objects.all():
        emp_one = pair.employee_one
        emp_two = pair.employee_two
        pc_list = PairCall.objects.filter(pair=find_pair(emp_one, emp_two)).order_by('-date')
        if not pc_list:
            create_timelapse_for_pair(emp_one, emp_two, is_same_team(emp_one, emp_two), -1)
        else:
            time_lapse_in_days = ((datetime.date.today() - pc_list[0].date).days)
            create_timelapse_for_pair(emp_one, emp_two, is_same_team(emp_one, emp_two), time_lapse_in_days)


def generate_new_pairs():

    """
    Generate all the missing pairs

    Delete the TimeLapse table and re-populate it

    Choose an employee at random

    Select a non-team member at random with whom he has never spoken before

    If none, select a team member at random with whom he has never spoken before

    Find out the max_time_lapse for that employee

    Select a non-team member at random with the max_time_lapse

    If none, Select a team member at random with the max_time_lapse

    """

    populate_new_pairs()

    populate_timelapse_table()

    employees_list = list(Employee.objects.all())
    random.shuffle(employees_list)

    #coming Monday
    new_paircall_date = datetime.date.today()
    while new_paircall_date.weekday() != 0:
        new_paircall_date += datetime.timedelta(1)

    for emp_one in employees_list:
        #Select a non-team member at random with whom he has never spoken before
        tl_list = TimeLapse.objects.filter(primary_employee=emp_one, secondary_employee__in = employees_list,
                                           is_same_team=False, time_lapse_in_days=-1)
        if tl_list:
            emp_two = random.choice(tl_list).secondary_employee
        else:
            #select a team member at random with whom he has never spoken before
            tl_list = TimeLapse.objects.filter(primary_employee=emp_one, secondary_employee__in=employees_list,
                                               is_same_team=True, time_lapse_in_days=-1)
            if tl_list:
                emp_two = random.choice(tl_list).secondary_employee
            else:
                max_timelapse = TimeLapse.objects.filter(primary_employee=emp_one).order_by('-time_lapse_in_days')[0]\
                                .time_lapse_in_days
                #Select a non-team member with whom TimeLapse is greatest
                tl_list = TimeLapse.objects.filter(primary_employee=emp_one, secondary_employee__in=employees_list,
                                           is_same_team=False, time_lapse_in_days=max_timelapse)
                if tl_list:
                    emp_two = random.choice(tl_list).secondary_employee
                else:
                    # Select a team member with whom TimeLapse is greatest
                    tl_list = TimeLapse.objects.filter(primary_employee=emp_one, secondary_employee__in=employees_list,
                                                       is_same_team=True, time_lapse_in_days=max_timelapse)
                    emp_two = random.choice(tl_list.filter(is_same_team=True)).secondary_employee

        PairCall.objects.create(pair=find_pair(emp_one, emp_two), is_done=False, date=new_paircall_date)
        employees_list.remove(emp_one)
        employees_list.remove(emp_two)








