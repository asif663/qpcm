import socket

hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)
print IP

insert into qpcmms_qpuser(name,userid,password,residencelocation,clubsallowed,emailid,status,role_id,officephone,mobileno) VALUES('Admin','admin','admin','Hyd','ABC','venugopal@techanipr.com','Active','1','0255788825','88856622223');