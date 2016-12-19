from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=200)
    team = models.ForeignKey(Team)
    availability = models.BooleanField(default=True) #For employees who are on leave or who left
    profile_pic = models.ImageField(blank=True, upload_to='profile')

    def __str__(self):
        return self.name


class Pair(models.Model):
    employee_one = models.ForeignKey(Employee, related_name='employee_one')
    employee_two = models.ForeignKey(Employee, related_name='employee_two')

    def __str__(self):
        return "%s <> %s" % (self.employee_one.name, self.employee_two.name)

class PairCall(models.Model):
    pair = models.ForeignKey(Pair)
    """is_done is True when pair call is done. It's False for all other scenarious - Pair call is not done, pair call
    is yet to be done
    """
    is_done = models.BooleanField(default=False)
    date = models.DateField() #date when pair call has happened
    picture = models.ImageField(blank=True, upload_to='paircall')
    caption = models.CharField(max_length=400, blank=True)

    def __str__(self):
        return "%s <> %s - %s" % (self.pair.employee_one.name, self.pair.employee_two.name,
                                  self.date.strftime("%b %d, '%y"))



class TimeLapse(models.Model):
    """
        This is mainly used to Generate Pairs
    """

    primary_employee = models.ForeignKey(Employee, related_name='tl_employee_one')
    secondary_employee = models.ForeignKey(Employee, related_name='tl_employee_two')
    is_same_team = models.BooleanField() #Are the two employees from the same team
    time_lapse_in_days = models.IntegerField() # -1 if never, in days


