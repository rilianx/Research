import training as t 
import sys

samples_file = sys.argv[1]
model_outputfile = sys.argv[2]
heur1_file = sys.argv[3]
heur2_file = sys.argv[4]

t.training(samples_file,model_outputfile,heur1_file, heur2_file)