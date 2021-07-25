import numpy as np
import random
def solve(ssh, bclass=8, id=1, min_fr=0.98, timelimit=10, strategy="bsg", home="/home/iaraya/clp", nsample=0, seed=0):
    if seed==0: seed=random.randint(0,10000)
    print(home+"/BSG_B "+home+"/problems/clp/benchs/BR/BR"+str(bclass)+".txt -i " \
                         +str(id)+" --min_fr="+str(min_fr)+" -t "+str(timelimit)+" -s "+strategy+" -f BR --print --nsample=" \
                            +str(nsample) + " --seed="+str(seed))
    stdin, stdout, stderr = ssh.exec_command(home+"/BSG_B "+home+"/problems/clp/benchs/BR/BR"+str(bclass)+".txt -i " \
                         +str(id)+" --min_fr="+str(min_fr)+" -t "+str(timelimit)+" -s "+strategy+" -f BR --print --nsample=" \
                            +str(nsample) + " --seed="+str(seed))
    
    sol=0
    sol_vector = []
    for line in stdout.readlines():
        if line.strip() == "best_solution:": 
            sol=1
        elif sol==1: #eval
            eval = np.fromstring(line, sep=',', dtype=float)
            sol=2
        elif sol==2: #cont_dim
            cont_dim = np.fromstring(line, sep=',', dtype=int)
            sol=3
        elif sol==3:
            #print(line)
            box = np.fromstring(line, sep=',', dtype=int)
            if len(box)>1:
                sol_vector.append(box)
    
    return eval, cont_dim, np.array(sol_vector)
