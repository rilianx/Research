
from io import SEEK_CUR


def loadData():

    file_=open("D:\Investigacion\interactivemcts\\results.txt","r") 
    simulations = []
    linea = file_.readlines()
    
    j= 0
    for i in range (0, len(linea)):
        
        candidates = []
        #print("for")
        if not linea: 
            break
        else:
        
            while j < len(linea):
                selectedNodes = []
                #print("while")
                #print("j: ", j)
                data = linea[j].rstrip().split(',')
                print(data)
                semicolon_pos = len(data) - 1
                #Si es la lista de nodos seleccionados
                if data[semicolon_pos] == ";":
                    print("semicolon")
                    x = 0
                    while x < len(data):
                        if data[x] != ";":
                            node = str(data[x])
                            print(node)
                            print(data[semicolon_pos])
                            selectedNodes.append(node)
                        x = x + 1

                    print("\n")
                    print("selectedNodes: ", selectedNodes)
                    

                if len(data) == 4:

                    id = 0
                    parent = 0
                    actions = 0
                    currentEvaluation = 0
                    
                    id = data[0]
                    parent = data[1]
                    actions = data [2]
                    currentEvaluation = data[3]

                    print("Simulated node: ", id, " ", parent, " ", actions, " ", currentEvaluation, "\n")

                if data[0] == "-":
                    print("next")


                j= j+1
    file_.close()
    return simulations   

loadData()