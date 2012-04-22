# Create your views here.
from django.shortcuts import render_to_response
from django.utils.html import conditional_escape as esc
from django.utils.safestring import mark_safe
from itertools import groupby
from calendar import HTMLCalendar, monthrange
import calendar
from datetime import datetime,date
from mysite.cal.models import Event,User

class EventCalendar(HTMLCalendar):
    def __init__(self, events):
        super(EventCalendar, self).__init__()
        self.events = self.group_by_day(events)
    def __init__(self, weekday,events):
        super(EventCalendar, self).__init__(weekday)
        self.events = self.group_by_day(events)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.events:
                cssclass += ' filled'
                body = ['<ul>']
                for event in self.events[day]:
                    body.append('<li>')
                    body.append('<a href="%s">' % event.url)
                    body.append(esc(event.event))
                    body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '<div class="dayNumber">%d</div> %s' % (day, ''.join(body)))
            return self.day_cell(cssclass,'<div class="dayNumber">%d</div>' % day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(EventCalendar, self).formatmonth(year, month)

    def group_by_day(self, events):
        field = lambda event: event.day.day
        return dict(
            [(day, list(items)) for day, items in groupby(events, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)


def named_month(pMonthNumber):
    """
    Return the name of the month, given the month number
    """
    return date(1900, pMonthNumber, 1).strftime('%B')

def event_filter(events,lYear,lMonth):
    lCalendarFromMonth = datetime(lYear, lMonth, 1)
    lCalendarToMonth = datetime(lYear, lMonth, monthrange(lYear, lMonth)[1])
    return events.filter(day__gte=lCalendarFromMonth, day__lte=lCalendarToMonth)

def make_dict(pYear,pMonth):
    lYear = int(pYear)
    lMonth = int(pMonth)
    lPreviousMonth = lMonth - 1
    lPreviousYear=lYear
    if lPreviousMonth == 0:
        lPreviousMonth = 12
        lPreviousYear  = lYear-1
    lNextMonth = lMonth + 1
    lNextYear  = lYear
    if lNextMonth == 13:
        lNextMonth = 1
        lNextYear  = lYear+1
    lYearAfterThis = lYear + 1
    lYearBeforeThis = lYear - 1

    return {'Month' : lMonth,
            'MonthName' : named_month(lMonth),
            'Year' : lYear,
            'PreviousMonth' : lPreviousMonth,
            'PreviousMonthName' : named_month(lPreviousMonth),
            'PreviousYear' : lPreviousYear,
            'NextMonth' : lNextMonth,
            'NextMonthName' : named_month(lNextMonth),
            'NextYear' : lNextYear,
            'YearBeforeThis' : lYearBeforeThis,
            'YearAfterThis' : lYearAfterThis,
            }
def getWeekday(wd):
    ret=calendar.MONDAY
    if wd=='Mon':
        ret=calendar.MONDAY
    elif wd=='Tue':
        ret=calendar.TUESDAY
    elif wd=='Wed':
        ret=calendar.WEDNESDAY
    elif wd=='Thu':
        ret=calendar.THURSDAY
    elif wd=='Fri':
        ret=calendar.FRIDAY
    elif wd=='Sat':
        ret=calendar.SATURDAY
    elif wd=='Sun':
        ret=calendar.SUNDAY
    else:
        pass
    return ret
def index_all(request):
    """
    Show calendar of events this month
    """
    lToday = datetime.now()
    return calendar_all(request, lToday.year, lToday.month)

def calendar_all(request, pYear, pMonth):
    """
    Show calendar of events for specified month and year
    """
    lYear = int(pYear)
    lMonth = int(pMonth)
    lEvents = event_filter(Event.objects.all(),lYear,lMonth)
    lCalendar = EventCalendar(lEvents).formatmonth(lYear, lMonth)
    
    dict=make_dict(pYear,pMonth)
    dict['Calendar']=mark_safe(lCalendar)
    return render_to_response('cal/month.html',dict)

def index_user(request, user_name):
    """
    Show calendar of events this month
    """
    lToday = datetime.now()
    return calendar_user(request, lToday.year, lToday.month, user_name)

def calendar_user(request, pYear, pMonth, user_name):
    """
    Show calendar of events for specified month and year
    """
    lYear = int(pYear)
    lMonth = int(pMonth)
    luser=User.objects.get(name=user_name)
    userEvents=luser.events.all()
    lEvents = event_filter(userEvents,lYear,lMonth)
    lCalendar = EventCalendar(getWeekday(luser.start_weekday),lEvents).formatmonth(lYear, lMonth)
    dict=make_dict(lYear,lMonth)
    dict['Calendar']=mark_safe(lCalendar)
    dict['user_name']=user_name
    return render_to_response('cal/month_user.html',dict)
