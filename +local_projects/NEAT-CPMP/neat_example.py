from __future__ import print_function
import numpy as np
import copy
import Greedy as gr
from Greedy import greedy_solve
import Layout
import os
import neat
import copy
import Pixie as px


def generate_ann_state_stack(layout, s, H):
    layout=copy.deepcopy(layout)
    max_item=max(set().union(*layout.stacks))
    
    #SF variables
    sf_possible = gr.SF_move_(layout)[0]!=False
    is_sorted = layout.is_sorted_stack(s)
    
    min_dif = 2*max_item
    for i in range(len(layout.stacks)):
        if i==s or len(layout.stacks[s])==0: continue
        c = layout.stacks[s][-1]
        dif = Layout.gvalue(layout.stacks[i]) - c
        
        if layout.is_sorted_stack(i) and len(layout.stacks[i]) < H and (dif >= 0) and (dif < min_dif):
            min_dif=dif    
    min_dif/=max_item     
    top = Layout.gvalue(layout.stacks[s])/max_item
    
    #SD variables
    size = len(layout.stacks[s])/H
    if size==0: mean = 0
    else: mean = np.mean(layout.stacks[s])/max_item
    if not is_sorted: rh=0
    else: rh = Layout.reachable_height(layout, s)/H
    sd_active = len(layout.moves)>0  and (layout.prev!="bg" and layout.moves[-1][0]==s)
    sorted_elements = layout.sorted_elements[s]/H
    
    return np.array([sf_possible,is_sorted,min_dif,top,size,mean,rh,sd_active, sorted_elements])



def generate_initial_layouts():
    global layouts
    return copy.deepcopy(layouts)


def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    layouts=generate_initial_layouts()

    fitness=0.0

    for layout in layouts: 
        best_ev=-1.0
        lay_copy = copy.deepcopy(layout)
        max_steps = greedy_solve(lay_copy, max_steps=100)

        for i in range(int(1.2*max_steps)):
            max_value=-np.inf
            for s in range(len(layout.stacks)):
                output = net.activate(generate_ann_state_stack(layout, s, 7))
                value = output[0]
                if value>max_value: 
                    max_value=value
                    s_o=s

            s_d,_=Layout.select_destination_stack(layout, s_o)
            if s_d==None: break 
            layout.move(s_o,s_d)

            lay_copy = copy.deepcopy(layout)
            steps = greedy_solve(lay_copy, max_steps=1.2*max_steps)
            if steps == None: break

            ev = -float(steps)/float(max_steps) + 0.01*i
            if ev > best_ev: best_ev=ev
        fitness+=best_ev

    fitness/=5.0
    return fitness

def eval_genomes(genomes, config):
    
    for genome_id, genome in genomes:
        genome.fitness=eval_genome(genome, config)
        
        
"""
Runs evaluation functions in parallel subprocesses
in order to evaluate multiple genomes at once.
"""
from multiprocessing import Pool

class ParallelEvaluator(object):
    def __init__(self, num_workers, eval_function, timeout=None):
        """
        eval_function should take one argument, a tuple of
        (genome object, config object), and return
        a single float (the genome's fitness).
        """
        self.num_workers = num_workers
        self.eval_function = eval_function
        self.timeout = timeout
        self.pool = Pool(num_workers)

    def __del__(self):
        self.pool.close() # should this be terminate?
        self.pool.join()


    def evaluate(self, genomes, config):
        jobs = []
        for ignored_genome_id, genome in genomes:
            jobs.append(self.pool.apply_async(self.eval_function, (genome, config)))

        # assign the fitness back to each genome
        for job, (ignored_genome_id, genome) in zip(jobs, genomes):
            genome.fitness = job.get(timeout=self.timeout)
            
evaluator = ParallelEvaluator(3, eval_genome)




def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(50))

    # Run for up to 5000 generations.
    winner = p.run(eval_genomes, 5000)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    #node_names = {-1:'A', -2: 'B', 0:'A XOR B'}
    #visualize.draw_net(config, winner, True, node_names=node_names)
    #visualize.plot_stats(stats, ylog=False, view=True)
    #visualize.plot_species(stats, view=True)

    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    #p.run(eval_genomes, 10)

layouts = []
layouts.append(px.read("Instancias/CVS/5-5/data5-5-1.dat"))
layouts.append(px.read("Instancias/CVS/5-5/data5-5-2.dat"))
layouts.append(px.read("Instancias/CVS/5-5/data5-5-3.dat"))
layouts.append(px.read("Instancias/CVS/5-5/data5-5-4.dat"))
layouts.append(px.read("Instancias/CVS/5-5/data5-5-1.dat"))
layouts.append(px.read("Instancias/CVS/5-5/data5-5-2.dat"))
layouts.append(px.read("Instancias/CVS/5-5/data5-5-3.dat"))
layouts.append(px.read("Instancias/CVS/5-5/data5-5-4.dat"))

for lay in range(4):
    gr.greedy_solve(layouts[lay],20)


# Determine path to configuration file. This path manipulation is
# here so that the script will run successfully regardless of the
# current working directory.
local_dir = os.path.dirname(".")
config_path = os.path.join(local_dir, 'neat-config.txt')
run(config_path)
        




