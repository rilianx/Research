import paramiko
import getpass
import numpy as np

print("Cargando ibex...")

home = "/home/iaraya/ibex/ibex-lib"

def connect(host):
    port = 22
    username = input("login:")
    password = getpass.getpass("pass:")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    return ssh


#llama al solver para encontrar frontera de pareto
def solve(ssh, instance, prec=1e-1):
    cmd = home+"/__build__/plugins/optim-mop/ibexmop "+ home + \
                "/plugins/optim-mop/benchs/" + instance + " --eps=" + str(prec) + \
                " --eps-contract --cy-contract-full --ub=ub1 --verbose"

    #print(cmd) 
    stdin, stdout, stderr = ssh.exec_command(cmd)
    
    flag = False; y1 = None; y2 = None
    i = 0
    
    for line in stdout.readlines():
        if "number of solutions:" in line:
            aux, n = line.strip().split(':')
            sols = int(n)
            y1 = np.zeros(sols); y2 = np.zeros(sols)
            
        if line==" solutions:\n":
            flag=True; continue
        if flag:
            #print(line.strip())
            a,b = line.strip().split()
            y1[i] = float(a); y2[i] = float(b)
            i += 1
    
    return y1, y2


def get_instances(ssh):
    cmd = "ls "+home+"/plugins/optim-mop/benchs/*.txt  | xargs -n 1 basename"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    for line in stdout.readlines():
        print(line.strip(), end=' ')