@user_login_required   
def membershipform(request):

    # member = []
    data = {}
    url = '/membershipform/'
    content={}
    content.update(csrf(request))
    user = request.session['user']
    # MemberFormObj = MemberForm()
    if 'emid' in request.GET:
        emid = request.GET['emid']
        mem_obj = member.objects.get(id=emid)
        data['name'] = mem_obj.name
        data['first_name_1'] = mem_obj.first_name_1
        data['first_name_2'] = mem_obj.first_name_2
        data['first_name_3'] = mem_obj.first_name_3
        data['initials'] = mem_obj.initials
        data['member_uid'] = mem_obj.member_uid
        data['residencelocation'] = mem_obj.residencelocation
        data['nationality'] = mem_obj.nationality
        data['office_fax_no'] = mem_obj.office_fax_no
        data['cont_type'] = mem_obj.cont_type
        data['cont_term_reason'] = mem_obj.cont_term_reason
        data['cont_expiry_date'] = mem_obj.cont_expiry_date
        data['No_of_dependents'] = mem_obj.No_of_dependents
        # company = associatecompany.objects.get(id=mem_obj.associatecompany)
        data['associatecompany'] = mem_obj.associatecompany
        data['maritalstatus'] = mem_obj.maritalstatus
        data['mobileno'] = mem_obj.mobileno
        data['gender'] = mem_obj.gender
        # data['emailid'] = mem_obj.emailid
        data['dob'] = mem_obj.dob
        data['member_uid'] = mem_obj.member_uid
        # print data['photo']
        data['date_of_joining'] = mem_obj.date_of_joining
        data['date_of_expiry'] = mem_obj.date_of_expiry
        data['rfidcardno'] = mem_obj.rfidcardno       
        data['extract_run_date'] = mem_obj.extract_run_date       
        data['pos_desc'] = mem_obj.pos_desc       
        data['worklocation'] = mem_obj.worklocation       
        li=[]
        l = mem_obj.clubsallowed
       
        clubs = []
        clubs_list = club.objects.all()

        for i in clubs_list:
            clubs.append(i.name)

        for i in clubs:
            if i in l:                
                li.append(i)
        data['clubsallowed'] = club.objects.filter(name__in=li)        
        data['status'] = mem_obj.status
        data['department'] = mem_obj.department
        data['membership_grade'] = mem_obj.membership_grade
        data['membership_category'] = mem_obj.membership_category
        data['organization'] = mem_obj.organization
        data['attachment'] = mem_obj.attachment
        data['qpuser'] = mem_obj.qpuser
        data['datetime'] = mem_obj.datetime
        form=MemberForm(initial=data)

        content = {'form':form,'mid':emid,'photo':mem_obj.photo,'IMAGE_URL':conf_settings.IMAGE_URL}
        
        if str(user.role) == 'Steward':
            return render_to_response('Steward/membershipform.html',content, context_instance=RequestContext(request))
        return render_to_response('membershipform.html', content,context_instance=RequestContext(request))


    if 'mid' in request.POST:   
        emid = request.POST['mid']
        if emid:
            
            member_form = MemberForm(request.POST)        
            if member_form.is_valid():
                memberedit = member.objects.get(id=emid)
                if 'Imagefile' in request.FILES:
                    f = request.FILES['Imagefile']
                    # print 'File',f
                    #f = open(settings.IMAGE_ROOT,"ListingImages\\Customer-%s.%s" %(cid,flist[1]), "wb")
                    file_name = f.name
                    flist = file_name.split(".")
                    data = f.read()
                    f.close()
                    f = open(conf_settings.IMAGE_ROOT + "%s.%s" %(memberedit.member_uid,flist[1]),"wb")
                    # size = (100,100)
                    # f.thumbnail(size, Image.ANTIALIAS)
                    # f.save(outfile, "JPEG")
                    f.write(data)
                    f.close()
                    imageUrl  = "%s.%s" %(memberedit.member_uid,flist[1])
                    # memberedit.photo =  imageUrl
                member_form = MemberForm(request.POST, instance = memberedit)
                member_form.save()
                if 'Imagefile' in request.FILES:
                    f = request.FILES['Imagefile']
                    if f:
                        memobj = member.objects.get(id=emid)
                        memobj.photo = imageUrl
                        memobj.save()
                if 'attachment' in request.FILES:
                    # f = request.FILES['Imagefile']
                    # file_name = f.name
                    # flist = file_name.split(".")
                    # data = f.read()
                    # # print data
                    # f.close()
                    # f = open(os.path.join(conf_settings.MEDIA_ROOT, "%s.%s" %(member_uid,flist[1])), "wb")
                    # f.write(data)
                    # f.close()
                    memobj = member.objects.get(id=emid)
                    memobj.attachment = request.FILES['attachment']
                    memobj.save()
                return HttpResponseRedirect('/members/')
    if 'mid' in request.GET:
        mid = request.GET['mid']
        mem_obj = member.objects.get(id=mid)
        sus_obj = suspension()
        sus_obj.member_id = mem_obj.id
        li=[]
        l = mem_obj.clubsallowed
       
        clubs = []
        clubs_list = club.objects.all()

        for i in clubs_list:
            clubs.append(i.name)

        for i in clubs:
            if i in l:                
                li.append(i)
        cl_list = club.objects.filter(name__in=li)


        if 'app' in request.GET:
            sus_obj.status = mem_obj.status = 'Active'
            sus_obj.clubsallowed = cl_list

        if 'can' in request.GET:
            if str(user.role) == 'Supervisor':
                mem_obj.status = 'Inactive'
                sus_obj.status = 'Membership-Cancelled'
                sus_obj.clubsallowed = cl_list
            else:
                sus_obj.status = mem_obj.status = 'Pending-Cancel'
                sus_obj.clubsallowed = cl_list

            if 'Supervisor' not in str(user.role):

                qpuser_lst = qpuser.objects.all()
                email_lst = []
                user_name = []
                for user in qpuser_lst: 
                    if user.role.rolename == 'Supervisor' or user.role.rolename =='supervisor':
                        user_name.append(user.name)
                        # lst = []
                        uni_code = user.clubsallowed
                        clubs = ['DRC','JRC','DWS','DGC','DFC','ASRC','MGC']  
                        # for club in clubs:
                        #     if club in clubs:
                        #         lst.append(club)
                        for mem_club in li:
                            if mem_club in clubs:
                                if user.emailid in email_lst:
                                    pass
                                else:
                                    email_lst.append(user.emailid)
                subject = 'Qp Club Cancel Notification'
                message = ''
                message += 'Hello %s\n\n\n'%user_name[0]
                message += 'Cancel request for the %s Club \n\n\n'%str(li[0])
                message += 'The Member  Mr/Ms %s  '%mem_obj.name
                message += 'His\Her Member ID  %s \n\n\n'%mem_obj.member_uid
                message += 'has been requested to Cancel for %s Club \n \n'%str(li[0])
                # message += 'The following club member has been requested to suspend'
                from_email = 'venugopal@techanipr.com'
                # to_list = ['ashok@indiadens.com']
                send_mail(subject, message, from_email, email_lst, fail_silently = True)
                messages.success(request, 'Hello Qp Club Membership Holders ')
        if 'd1' in request.GET:
            d1 = request.GET['d1']
            if d1:
                # date =  d1.split('-')
                # sdate = datetime.date(int(date[2]),int(date[0]),int(date[1]))
                # print "sdate
                sus_obj.fromdate = d1

        if 'd2' in request.GET:
            d2 = request.GET['d2']
            if d2:
                # date =  d2.split('-')
                # sdate1 = datetime.date(int(date[2]),int(date[0]),int(date[1]))
                sus_obj.todate = d2
        if 'ren' in request.GET:
            renewal_obj = renewal()
            if str(user.role) == 'Supervisor':
                renewal_obj.status = mem_obj.status = 'Active'
            else:
                renewal_obj.status = mem_obj.status = 'Pending-Renewal'
            renewal_obj.date_of_renewal = d1
            renewal_obj.date_of_expiry = d2
            renewal_obj.renewalby = user
            renewal_obj.member_id = mid
            # renewal_obj.renewaldate2 = sdate1
            renewal_obj.save()

        if 'sus' in request.GET:
            if str(user.role) == 'Supervisor':
                sus_obj.status = mem_obj.status = 'Suspend'
                sus_obj.clubsallowed = cl_list
            else:
                sus_obj.status = mem_obj.status = 'Pending-Suspension'
                sus_obj.clubsallowed = cl_list
            if 'Supervisor' not in str(user.role):
                qpuser_lst = qpuser.objects.all()
                email_lst = []
                user_name = []
                for user in qpuser_lst: 
                    if user.role.rolename == 'Supervisor' or user.role.rolename =='supervisor':
                        user_name.append(user.name)
                        # lst = []
                        uni_code = user.clubsallowed
                        clubs = ['DRC','JRC','DWS','DGC','DFC','ASRC','MGC']  
                        # for club in clubs:
                        #     if club in clubs:
                        #         lst.append(club)
                        for mem_club in li:
                            if mem_club in clubs:
                                if user.emailid in email_lst:
                                    pass
                                else:
                                    email_lst.append(user.emailid)
                subject = 'Qp Club Suspend Notification'
                message = ''
                message += 'Hello %s\n\n\n'%user_name[0]
                message += 'Suspend request for the %s Club \n\n\n'%str(li[0])
                message += 'The Member  Mr/Ms %s  '%mem_obj.name
                message += 'His\Her Member ID  %s \n\n\n'%mem_obj.member_uid
                message += 'has been requested to suspended for %s Club \n \n'%str(li[0])
                # message += 'The following club member has been requested to suspend'
                from_email = 'venugopal@techanipr.com'
                # to_list = ['ashok@indiadens.com']
                send_mail(subject, message, from_email, email_lst, fail_silently = True)
                messages.success(request, 'Hello Qp Club Membership Holders ')

        if 'rev' in request.GET:
            if str(user.role) == 'Supervisor':
                mem_obj.status = 'Active'
                sus_obj.status = 'Suspension-Revoke'
                sus_obj.clubsallowed = cl_list
            else:
                sus_obj.status = mem_obj.status = 'Pending-Suspension-Revoke'
                sus_obj.clubsallowed = cl_list
            if 'Supervisor' not in str(user.role):
                qpuser_lst = qpuser.objects.all()
                email_lst = []
                user_name = []
                for user in qpuser_lst: 
                    if user.role.rolename == 'Supervisor' or user.role.rolename =='supervisor':
                        user_name.append(user.name)
                        # lst = []
                        uni_code = user.clubsallowed
                        clubs = ['DRC','JRC','DWS','DGC','DFC','ASRC','MGC']  
                        # for club in clubs:
                        #     if club in clubs:
                        #         lst.append(club)
                        for mem_club in li:
                            if mem_club in clubs:
                                if user.emailid in email_lst:
                                    pass
                                else:
                                    email_lst.append(user.emailid)
                subject = 'Qp Club Revoke Notification'
                message = ''
                message += 'Hello %s\n\n\n'%user_name[0]
                message += 'Revoke request for the %s Club \n\n\n'%str(li[0])
                message += 'The Member  Mr/Ms %s  '%mem_obj.name
                message += 'His\Her Member ID  %s \n\n\n'%mem_obj.member_uid
                message += 'has been requested to Revoke for %s Club \n \n'%str(li[0])
                # message += 'The following club member has been requested to suspend'
                from_email = 'venugopal@techanipr.com'
                # to_list = ['ashok@indiadens.com']
                send_mail(subject, message, from_email, email_lst, fail_silently = True)
                messages.success(request, 'Hello Qp Club Membership Holders ')
        if 'r' in request.GET:
            reason = request.GET['r']
            sus_obj.reason = reason
        else:
            sus_obj.reason = ''

        sus_obj.save()

        mem_obj.save()
        family_obj = family.objects.filter(member_id=mem_obj.id)
        for i in family_obj:
            i.status = mem_obj.status
            i.save()
        memobj = member.objects.get(id=mid)
        li = []
        clubs = club.objects.all()
        sus_obj = suspension.objects.filter(member_id=mem_obj.id).order_by('-id')
        sus_obj = sus_obj[0]
        li=[]
        l = sus_obj.clubsallowed
       
        clubs = []
        clubs_list = club.objects.all()

        for i in clubs_list:
            clubs.append(i.name)

        for i in clubs:
            if i in l:                
                li.append(i)
        new_cl = club.objects.filter(name__in=li)

        for i in new_cl:

            status_obj = clubstatus.objects.filter(member_id=mem_obj.id,club_id=i.id)
            status_obj = status_obj[0]

            if str(sus_obj.status) == 'Suspension-Revoke':
                status_obj.status = 'Active'

            if str(sus_obj.status) == 'Membership-Cancelled':
                mem_obj.status = 'Inactive'
                mem_obj.save()

            if str(sus_obj.status) == 'Active':
                status_obj.status = 'Active'
                mem_obj.status = 'Active'
                mem_obj.save()   

            else:
                status_obj.status = sus_obj.status
            status_obj.save()
        return HttpResponseRedirect('/members/')
    else:
        if request.method == 'POST':
            form=MemberForm(request.POST)
            print 'ERRORS',form.errors
            if form.is_valid():
                member_uid = form.cleaned_data['member_uid']
                clubs = form.cleaned_data['clubsallowed']
                print clubs
                obj = form.save(commit=False)
                if str(user.role) == 'Supervisor':
                    obj.status = 'Active'
                # obj.user_id = user.id
                if 'Imagefile' in request.FILES:
                    f = request.FILES['Imagefile']
                    file_name = f.name
                    flist = file_name.split(".")
                    data = f.read()
                    # print data
                    f.close()
                    f = open(os.path.join(conf_settings.IMAGE_ROOT, "%s.%s" %(member_uid,flist[1])), "wb")
                    f.write(data)
                    f.close()
                if 'Imagefile' in request.FILES:
                    if f:
                        # memObj = member.objects.latest('id')
                        imageUrl  = "%s.%s" %(member_uid,flist[1])
                        obj.photo =  imageUrl
                if 'Imagefile' not in request.FILES:
                    imageUrl  = 'People.jpg'
                    obj.photo =  imageUrl
                #     # customer.save()
                if 'attachment' in request.FILES:
                    # f = request.FILES['Imagefile']
                    # file_name = f.name
                    # flist = file_name.split(".")
                    # data = f.read()
                    # # print data
                    # f.close()
                    # f = open(os.path.join(conf_settings.MEDIA_ROOT, "%s.%s" %(member_uid,flist[1])), "wb")
                    # f.write(data)
                    # f.close()
                    obj.attachment = request.FILES['attachment']
                obj.save()
                memobj = member.objects.filter(qpuser=user.id).latest('id')
                memobj.member_uid = '9000000' + str(memobj.id)
                # memobj = member.objects.filter(qpuser=userid.id).latest('id')
                clubstatus_obj = clubstatus()

                # memship = membership()
                clubstatus_obj.member_id = memobj.id
                li=[]
                # l = mem_obj.clubsallowed

                clubs = []
                clubs_list = club.objects.all()

                for i in clubs_list:
                    clubs.append(i.name)

                for i in clubs:
                    if i in memobj.clubsallowed:
                        li.append(i)

                for i in li:
                    c_obj = club.objects.get(name=i)
                    memship = clubstatus(member_id=memobj.id,club_id=c_obj.id,status=memobj.status)

                    memship.save()
                memobj.save()
                return HttpResponseRedirect('/members/')

    organization1 = organization.objects.all().exclude(name="QP")
    
    form=MemberForm(initial={'qpuser':user.id, 'status':'Pending', 'organization': organization1[0].id})


    content = {'username':user.name,'form':form, 'url':url}

    if str(user.role) == 'Steward':
         return render_to_response('Steward/membershipform.html',content,context_instance=RequestContext(request))
    return render_to_response('membershipform.html',content,context_instance=RequestContext(request))