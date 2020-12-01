import paramiko
import getpass
import numpy as np
home = "/home/iaraya/ibexmop3"

ssh = None
def connect(host):
    global ssh
    port = 22
    username = input("login:")
    password = getpass.getpass("pass:")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    return ssh

ssh = connect("158.251.88.197")

stdin, stdout, stderr = ssh.exec_command(home+"/__build__/plugins/optim-mop/ibexmop "+ home + \
                "/plugins/optim-mop/benchs/viennet2.txt --print-nds -t 0.1 --nb_sol=n --ub=ub1")

xdata=[]; ydata=[]; zdata=[]
iter=0
selected_box_id = {}; feasible_solutions= {}; new_boxes_id = {}; boxes = dict()
flag=None
for line in stdout.readlines():
    if line.strip()=="NDS:": flag="nds"; continue
    if line.strip()=="left_boxes:": flag="boxes"; continue
    if line.strip()=="end": flag=None; continue 
                
    if flag=="nds":
        x, y, z = line.split()
        xdata.append(float(x))
        ydata.append(float(y))
        zdata.append(float(z))
    elif flag==None:
        sp_line = line.split(':')
        if sp_line !=  None:
            if sp_line[0]=='erase':
                if iter in feasible_solutions: 
                    feasible_solutions[iter] = np.array(feasible_solutions[iter])
                iter += 1
                selected_box_id[iter] = int(sp_line[1])
            elif sp_line[0]=='feasible_solution':
                if iter not in feasible_solutions: feasible_solutions[iter] = []
                feasible_solutions[iter].append( np.fromstring(sp_line[1], sep=' '))
            elif sp_line[0]=='insert':
                if iter not in new_boxes_id: new_boxes_id[iter] = []
                idbox = int(sp_line[1])
                boxes[idbox] =  np.fromstring(sp_line[2], sep=' ')
                new_boxes_id[iter].append( idbox )        
                
if iter in feasible_solutions: 
    feasible_solutions[iter] = np.array(feasible_solutions[iter])
    
xdata=np.array(xdata)
ydata=np.array(ydata)
zdata=np.array(zdata)
print("number of points:",len(xdata))

from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt

xx = feasible_solutions[8][:,0]
yy = feasible_solutions[8][:,1]
zz = feasible_solutions[8][:,2]

xx2 = feasible_solutions[15][:,0]
yy2 = feasible_solutions[15][:,1]
zz2 = feasible_solutions[15][:,2]

fig = plt.figure()

ax = plt.axes(projection='3d')

#ax.view_init(5,5 )
ax.scatter3D(xdata, ydata, zdata, c='g');
ax.scatter3D(xx, yy, zz, c='r');
ax.scatter3D(xx2, yy2, zz2, c='y');
plt.show()