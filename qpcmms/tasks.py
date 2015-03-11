# from celery.registry import task
# from celery.task import Task
from __future__ import absolute_import
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mass_mail

from qpcmms.models import *

from celery.decorators import task
from celery import Celery
import logging
log = logging.getLogger(__name__)
from celery.task.schedules import crontab
from celery.decorators import periodic_task
# from myapp.utils import scrapers
from celery.utils.log import get_task_logger
# from datetime import datetime
from datetime import datetime,timedelta,date
from collections import deque
from django.db.models import Q


app = Celery('tasks', backend='amqp', broker='amqp://')


@app.task
def UserMail(uobj,pwd):

    email_lst = []
    # subject,from_email, to = 'Welcome to QP', 'Venugopal<venu@gmail.com>' ,uobj.emailid
    # # print uobj.userid

    # html_content = render_to_string('PasswordReset.html',{'user':uobj.name,'emailid':uobj.userid,'password':uobj.password})
    # text_content = strip_tags(html_content)
    # msg = EmailMultiAlternatives(subject,text_content,from_email,[to])
    # msg.attach_alternative(html_content,'text/html')
    # msg.send()
    subject = 'Request to Change/Reset Password for QP-Club Membership Management System'
    message = 'Dear User,\n'
    message += 'As per the request initiated for Change/Reset in your password, please find your new password below.\n\n\n'
    message += 'Your Username: %s \n'%(uobj.userid)
    message += 'Your Password: %s\n\n\n'%(pwd)
    message += 'Thanks,\n'
    message += 'QPECMMS\n'
    email_lst.append(uobj.emailid)
    datatuple = (
        (subject, message, 'venugopal@techanipr.com', email_lst),
        )

    send_mass_mail(datatuple, fail_silently = True)


@app.task
def NotifySupervisor(datatuple):
    send_mass_mail(datatuple, fail_silently = True)



'''Cron for Near Renewal Members'''
# A periodic task that will run every minute (the symbol "*" means every)
# @periodic_task(run_every=(timedelta(seconds=5)))
@periodic_task(run_every=crontab(hour=02, minute=01,day_of_week='*'))
def mytask():
    # log.debug("Executing task")
    expires = clubstatus.objects.filter(date_of_expiry__isnull=False)
    supervisor = role.objects.get(rolename='Supervisor')
    qpuser_lst = qpuser.objects.filter(role_id=supervisor.id)
    email_lst = []
    member_mails = []
    mems = []
    

    ren_list = deque()

    for i in expires:
        if i.date_of_expiry != None:
            if (i.date_of_expiry.year==date.today().year) and (i.date_of_expiry.month==date.today().month) and date.today().day-i.date_of_expiry.day<=15:
                member_mails.append(i.member.emailid)
                i.status = 'Pending-Renewal'

                mems.append(i.member.member_uid)

                for u in qpuser_lst:
                    if u.role.rolename == 'Supervisor' or u.role.rolename =='supervisor':
                        l = u.clubsallowed
                        clubs = []
                        li = []
                        clubs_list = club.objects.all()

                        for j in clubs_list:
                            clubs.append(j.name)


                        for k in clubs:
                            if k in l:                
                                li.append(k)
                        new_cl = club.objects.filter(name__in=li)
                        for l in new_cl:
                            # for j in clubs_list:
                                if l.id == i.club.id:
                                    email_lst.append(u.emailid)
                i.save()


    # datatuple = (
    #               ('Test', 'Test', 'venugopal@techanipr.com', email_lst),
    #               )
    if email_lst:
        mems = list(set(mems))
        email_lst = list(set(email_lst))
        subject = 'Alert for renewal of expiring membership.'
        message = 'Dear Recipient,\n\n\n'
        message += 'This mail is to inform you that a single or multiple QP Club membership/s with following details are near to their expiration, \n\n\n'
        # name = mem_obj.name+' '+mem_obj.first_name_1
        message += 'Members List: %s \n\n\n '%mems
        message += 'Please take required action for renewal if intended.\n\n\n'
        # message += 'Regards,QP Club Management\n \n'
        # message += 'Click http://localhost:8000/common/?mid=%s to take any action.'%(str(mem_obj.id))
        from_email = 'venugopal@techanipr.com'

        member_message = 'This mail is to inform you that your QP Club membership is near to its expiration.'
        member_message += 'Please take required action for renewal if intended.'
        datatuple = (
        (subject, message, 'venugopal@techanipr.com', email_lst),
        (subject, member_message, 'venugopal@techanipr.com', member_mails),
        )

        send_mass_mail(datatuple, fail_silently = True)


    print 'Renewal Alert',email_lst
    return True


# @periodic_task(run_every=(timedelta(seconds=30)))
# @periodic_task(run_every=crontab(hour=12, minute=05,day_of_week='*'))
@periodic_task(run_every=crontab(hour=03, minute=05,day_of_week='*'))
def childern_age_expiry():

    ''' Cron for Child Age Expiry '''

    obj_listf=family.objects.filter(age__range=(19,23))
    today=date.today()
    difference = timedelta(days=15)
    dif=timedelta(days=21*365.245)

    obj_list=deque()
    supervisor = role.objects.get(rolename='Supervisor')
    qpuser_lst = qpuser.objects.filter(role_id=supervisor.id)

    email_lst = []
    children = []

    member_mails = []

    # print 'im der',obj_listf

    com_date = today +difference
    for l in obj_listf:
        for u in qpuser_lst:
            if u.role.rolename == 'Supervisor' or u.role.rolename == 'Steward':
                l1 = u.clubsallowed
                clubs = []
                li = []
                clubs_list = club.objects.all()

                for j in clubs_list:
                    clubs.append(j.name)


                for k in clubs:
                    if k in l1:                
                        li.append(k)
                new_cl = club.objects.filter(name__in=li)
                mem = clubstatus.objects.filter(member_id=l.member_id)
                # print mem
                for m in new_cl:
                    for j in mem:
                        if m.id == j.club.id:
                            email_lst.append(u.emailid)
                            member_mails.append(l.member.emailid)

        if l.status=="Active":
            exp_date=l.dob+dif
              
            dic = {}
            age=int((com_date.year-l.dob.year)/1.0+(com_date.month-l.dob.month)/12.0+(com_date.day-l.dob.day)/365.0)
            if age==21 and today<=exp_date and (l.status != 'Cancelled-Age21' or l.status != 'Pending-Crossed-Age 21'):
                    if l.date_of_expiry:
                        if l.date_of_expiry < today:

                            email_lst.append(l.member.emailid)
                            children.append(l.family_uid)

                            l.status = 'Pending-Crossed-Age 21'
                            l.save()
                    email_lst.append(l.member.emailid)
                    children.append(l.family_uid)

                    l.status = 'Pending-Crossed-Age 21'
                    l.save()

    if children:

        children = list(set(children))

        print 'child age expiry',children

        subject = 'Alert for maturation of child memberships'
        message = 'Dear Steward/Supervisor,\n\n\n'
        message += 'This mail is to inform you that single or multiple QP Club Child membership/s with following details are near to their maturation., \n\n\n'

        message += 'Child List: %s \n\n\n '%children

        message += 'As the membership holder/s will be considered as an adult after maturation date. Please request for a renewal if intended to continue membership.\n \n'
        
        member_message = 'Dear Parent,\n\n\n'
        member_message += 'This mail is to inform you that your QP Club Child membership  is near to its maturation.\n\n'

        member_message += 'As the membership holder will be considered as an adult after maturation date, a renewed membership will be needed. Please request for renewal if intended to continue membership.'
        
        from_email = 'venugopal@techanipr.com'
        datatuple = (
        (subject, message, 'venugopal@techanipr.com', email_lst),
        (subject, member_message, 'venugopal@techanipr.com', member_mails),
        )

        send_mass_mail(datatuple, fail_silently = True)

# @periodic_task(run_every=(timedelta(seconds=40)))
@periodic_task(run_every=crontab(hour=04, minute=01,day_of_week='*'))
def member_revoke():
    ''' Cron for Revoking Suspended Members'''

    print 'Revoking Members'

    expirations = suspension.objects.filter(todate=date.today(),status='Suspended')
    mems = deque()
    clubs = deque()
    for i in expirations:

        mems.append(i.member_id)

        clubs.append(i.club_id)

    cls = clubstatus.objects.filter(member_id__in=mems,status='Suspended',club_id__in=clubs)

    for i in cls:
        i.status = 'Pending-Suspension-Revoke'
        i.save()


    return True


# @periodic_task(run_every=crontab(minute='*/1'))
# @periodic_task(run_every=crontab(hour=11, minute=59,day_of_week='*'))
@periodic_task(run_every=(timedelta(seconds=10)))
def test():

    print 'test mail'

    datatuple = (
                  ('Test', 'Test', 'venugopal@techanipr.com', ['venugopal@anipr.in']),
                  )

    send_mass_mail(datatuple, fail_silently = True)

    return True