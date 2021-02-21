import paramiko
import getpass
import numpy as np

def connect(host):
    port = 22
    username = input("login:")
    password = getpass.getpass("pass:")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    return ssh

import ast 
import copy
class imrt:
    def init_instance(self, files, max_voxels=500, targeted=True, min_impr=0.05, vsize=0.002):
        transport = self.ssh.get_transport()
        self.channel = transport.open_session(timeout=3600)
        if targeted == True:
            cmd = "killall DAO_ILS; "+self.home+"/DAO_ILS "+"--files-dep="+files[0]+ \
                             " --file-coord="+files[1]+" --tabu-size=200 --setup=5 --seed=3 --min_impr="+ \
                            str(min_impr)+" --maxeval=1000" + \
                             " --vsize="+str(vsize)+" --max_voxels="+str(max_voxels) +" --path="+self.home + " --port="+str(self.port)
        else:
            cmd = "killall DAO_ILS; "+self.home+"/DAO_ILS "+"--files-dep="+files[0]+ \
                             " --file-coord="+files[1]+" --tabu-size=200 --setup=5 --seed=3 --min_impr=5 --maxeval=1000" + \
                             " --vsize=0.0001 --max_voxels="+str(max_voxels) +" --path="+self.home + " --port="+str(self.port)
        
        print(cmd)
        self.channel.exec_command(cmd)
        
        print("echo start | netcat localhost "+ str(self.port))
        stdin, stdout, stderr = self.ssh.exec_command("echo start | netcat localhost "+ str(self.port))
        print(stdout.readlines()[0])
        
    def __init__(self, home, files, ssh, max_voxels=500, port=8080, targeted=True, min_impr=0.05, vsize=0.002):
        self.home = home
        self.ssh = ssh
        self.port = port
        self.init_instance(files, max_voxels=max_voxels, targeted=targeted, min_impr=min_impr, vsize=vsize)
        self.init_data()
    
    def init_data(self):
        stdin, stdout, stderr = self.ssh.exec_command("echo get_info | netcat localhost "+ str(self.port))
        lines = stdout.readlines()
        #print(lines)
        self.nvoxels = np.fromstring(lines[0], dtype=int, sep=' ')
        self.angles = np.fromstring(lines[1], dtype=int, sep=' ')
        self.angle2nbeamlets = ast.literal_eval(lines[2])
        xdim,ydim = int(lines[3].split(' ')[0]), int(lines[3].split(' ')[1])
        
        self.shape = dict()
        i=4
        for angle in self.angle2nbeamlets:
            self.shape[angle] = np.fromstring(lines[i], dtype=int, sep=' ').reshape(xdim,ydim); i += 1

    def init_fluence_map(self, fluence_map, bac):
        self.bac = copy.copy(bac)
        bac_str = [str(y) for y in bac]
        fmap_str = [str(y) for y in fluence_map]
        print("echo init_fluence_map "+ str(len(bac)) + " " + " ".join(bac_str) + \
                                                      " " + " ".join(fmap_str) + " | netcat localhost "+ str(self.port))
        stdin, stdout, stderr = self.ssh.exec_command("echo init_fluence_map "+ str(len(bac)) + " " + " ".join(bac_str) + \
                                                      " " + " ".join(fmap_str) + " | netcat localhost "+ str(self.port))
        return float(stdout.readlines()[0])
    
    def local_search(self, type, maxeval):
        stdin, stdout, stderr = self.ssh.exec_command("echo local_search "+type+" "+ str(maxeval) +"  | netcat localhost "+ str(self.port))
        ev, nevals = stdout.readlines()[0].split(' ')
        return float(ev), int(nevals)
    
    def get_fluence_map(self):
        stdin, stdout, stderr = self.ssh.exec_command("echo get_fluence_map | netcat localhost "+ str(self.port))
        fluence_map = []
        lines = stdout.readlines()
        for i in range(len(lines)):
            fluence_map.append (np.fromstring(lines[i], sep=' ', dtype=int))

        return fluence_map
    
    def get_impact_map(self):
        stdin, stdout, stderr = self.ssh.exec_command("echo get_impact_map | netcat localhost "+ str(self.port))
        impact_map = []
        lines = stdout.readlines()
        for i in range(len(lines)):
            #print(lines[i])
            impact_map.append (np.fromstring(lines[i], sep=' ', dtype=float))

        return impact_map

    def fm2matrix(self, fm, angle, dtype=int):
        x,y = self.shape[angle].shape
        Y = np.zeros((x,y), dtype=dtype)

        k=0
        for i in range(x):
            for j in range(y):
                if self.shape[angle][i][j]==1: 
                    Y[i][j] = fm[k]
                    k += 1
                else: Y[i][j] = -1
        return Y
    
    def matrix2fm(self, Y, angle):
        x,y = Y.shape

        k=0
        _fm = np.zeros(self.angle2nbeamlets[angle], dtype=int)
        for i in range(x):
            for j in range(y):
                if self.shape[angle][i][j]==1 and Y[i][j] != -1:
                    _fm[k] = Y[i][j] 

                if self.shape[angle][i][j] == 1: k += 1

        return _fm
        
    
    
    def get_dose_vectors(self):
        stdin, stdout, stderr = self.ssh.exec_command("echo get_dose_vector | netcat localhost "+ str(self.port))
        lines=stdout.readlines()
        len(lines)
        vectors = []
        for i in range(len(self.nvoxels)):
            vectors.append(np.fromstring(lines[i], sep=' '))
        return vectors
    
    def iterated_local_search(self, maxeval=0):
        best_eval = np.inf
        no_improvements = 0
        tot_evals = 0
        while no_improvements < 2: #4 para evitar que converja debido a tabu_list
            if maxeval>0 and maxeval-tot_evals <=0: break
            ev, evals = self.local_search("beam_intensity", maxeval-tot_evals)
            tot_evals += evals
            if ev < best_eval: best_eval = ev; no_improvements = 0
            else: no_improvements += 1

            if no_improvements == 2: break
                
            if maxeval>0 and maxeval-tot_evals <=0: break
            ev, evals = self.local_search("level_intensity", maxeval-tot_evals)
            tot_evals += evals
            if ev < best_eval: best_eval = ev; no_improvements = 0
            else: no_improvements += 1
        return best_eval, tot_evals
        
    def get_deposition_matrix(self, organ, angle):
        stdin, stdout, stderr = self.ssh.exec_command("echo get_deposition_matrix "+str(organ)+" "+str(angle)+ \
                                                      " | netcat localhost "+ str(self.port))
        lines = stdout.readlines()
        matrix = []
        for i in range(0,self.nvoxels[organ]):
            matrix.append(np.fromstring(lines[i], dtype=float, sep=' '))
        return np.array(matrix)