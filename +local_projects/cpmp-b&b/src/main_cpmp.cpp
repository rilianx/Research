
#include <map>
#include <vector>
#include <list>
#include <iterator>
#include <cmath>
#include <iostream>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <stdexcept>
#include<ctime>
#include "dirent.h"
#include "Layout.h"
#include "Greedy.h"
#include "Bsg.h"
#include <queue>
#include <stack>

using namespace std;
using namespace cpmp;


//DEJAR DENTRO DEL LAYOUT
    
class Nodo
{
    public:
        Layout * actual;
        Nodo * padre;
        list <Nodo *> hijos;
        int nivel;
        bool greedy_child;
        int score = 0;

    /*************************************************************/
    ///////////////////////BOB EL CONSTRUCTOR//////////////////////
    /*************************************************************/
    
    //HACER UN DESTRUCTOR
        Nodo(Layout * l, int lvl, Nodo * padre=NULL) : actual(new cpmp::Layout(*l)), 
        greedy_child(false), nivel(lvl), padre(padre)
        {
            
        }
    /*************************************************************/
    ///////////////////////Funciones///////////////////////////////
    /*************************************************************/

        ~Nodo()
        {
            delete(actual);
        }

         void get_children(list <Nodo*> &children)
        {
            int stacks = this->actual->stacks.size();
            int i,j;
            int h = this->actual->H;
            //Por cada stack
            for (i=0;i<stacks;i++)
            {
                //Se mueve al resto
                for (j=0;j<stacks;j++)
                {
                    //Si no es el mismo stack
                    //+
                    //Si la columna actual no tiene tamaño 0 y Si la columna objetivo no esta llena
                    if (i != j && actual->stacks[i].size() != 0 && actual->stacks[j].size() != h && 
                                        actual->validate_move(i,j) &&  actual->validate_move2(i,j))
                    {
                        //Se crea un nuevo nodo
                        Nodo * niu = new Nodo(actual,(nivel)+1,this);
                        //Se realiza el movimiento
                        niu->actual->move(i,j);

                        //Se inserta en LA COLA
                        children.push_back(niu);
                            
                    }
                }
            }
           // return pendientes;
        }       
    //****************************************************************************
        
        
};

class compare_nodes2
{

public:
  bool operator() (const Nodo* lhs, const Nodo* rhs) const
  {
    if (lhs->actual->lb >= rhs->actual->lb) return (true);
    else return (false);
  }
};

class Tree
{
    public:
        Nodo * base;
        int limite;
        //stack <Nodo*> S;
        priority_queue<Nodo*, vector<Nodo*>, compare_nodes2> S;

        int contador=0;
        int nivel;
        Nodo * mejor;
        //Constructores
    
        Tree(Layout * l, int lvl)
        {
            search2(l, lvl);
            //cout << "FINISH HIM\n";
        }
    /*************************************************************/
    ///////////////////////Funciones///////////////////////////////
    /*************************************************************/
    //DICE LOS PASOS TOTALES
    int greedy(Layout *  L, int u=1000)
        {
            int steps;
            int type=ATOMIC_MOVE;
            bool PIXIE=true;
            int beams=0;
            Layout h = *L;
            Layout * nuevo = new Layout(h);
            Layout sol = *nuevo;
            if(PIXIE) steps = pixie_solve(sol,u);
            else steps = greedy_solve(sol,u);
            
            delete(nuevo);
            
            return steps;
        }


    
    /*************************************************************/

    float eva(Nodo * n,int lower)
        {
            Layout * L = n->actual;
            //int l = (L->lb)-lower;
            //return l;
            return L->lb;
        }

    // comparison, not case sensitive.
    static bool compare_nodes (const Nodo* n1, const Nodo* n2)
    {
        return ( (*n1).score < (*n2).score );
    }


    void search2(Layout* l, int lvl)
    {
        map <int,int> lbs;
        Nodo* root = new Nodo(l,lvl,NULL);

        //Adjunto la base al stack
        root->actual->lowb();
        lbs[root->actual->lb]=1; 
        
        S.push(root);
            
        int L = root->actual->lb;
        int U = greedy(root->actual);
        
        
        Nodo * temp;
        Nodo * aux;
        
        //IMPRIMIR CANTIDAD DE NODOS QUE TARDA EN LLEGAR A LA MEJOR SOLUCION

        temp = S.top();

        int contadorDeNodos = 0;
        while (S.size()!=0)
        {
            //Se obtiene el elemento top del stack
            temp = S.top(); S.pop();
            //cout << temp->actual->steps << "," << temp->greedy_child << endl;
            int l = temp->actual->lb;
            

            lbs[l]--;
            if(lbs[l]==0) lbs.erase(l);
            
            if (l >= U){
                if (L == U){
                    cout << U << " " << contadorDeNodos << " ";
                    return;
                }
                delete(temp);
                continue;
            }
            int u=-1;

            if (l-temp->actual->steps < 10)
                u = greedy(temp->actual, temp->actual->steps+10);

            if (temp->actual->unsorted_stacks==0) u=temp->actual->steps;

            

            if (u==-1) u=1000;

            if (u < U)
            {
                cout << temp->actual->steps << ";" <<   temp->actual->lb << ";" << L << ";" << u << endl;
                cout << u;cout << "\nNodos hasta el momento: ";cout << contadorDeNodos;cout << "\n\n";
                U = u;
                if (l >= U){
                    delete(temp);
                    continue;
                }
            }


            
            if (L == U)
            {
                cout << U << " " << contadorDeNodos << " ";
                return;
            }

            contadorDeNodos ++;
            //Obtiene los hijos
            list <Nodo*> children;
            temp->get_children(children);

            //diving
            /*if(children.size()>0){
                Layout lay= *temp->actual;
                iter_greedy(lay);
                if (lay.steps < U){
                    lay.lowb();
                    if(lay.lb < U){
                        Nodo * n = new Nodo(&lay,lay.steps,temp);
                        n->greedy_child=true;
                        S.push(n);
                        lbs[lay.lb]++;
                    }
                }
            }*/

            //Evaluo y Ordeno (for stack only)
            //for (auto& n:children) n->score = eva(n,L);
            //children.sort(compare_nodes);


            for (auto& aux:children)
            {
                aux->actual->lowb();
                if(aux->actual->lb < U){
                    S.push(aux);
                    lbs[aux->actual->lb]++;
                }else delete aux;
            }

            children.clear();
            delete(temp);

            //actualizar el menor l de los nodos del stack
            L = lbs.begin()->first;
        }

        cout << U << " " << contadorDeNodos << " ";


        
    }
     /*************************************************************/
};

int main(int argc, char * argv[]){
    Layout::H = atoi (argv[1]);
    string path(argv[2]);
    int beams = atoi (argv[3]);
    Layout L(path), best_lay(path);
    const clock_t begin_time = clock();
    int steps;
    //if (beams==0) steps = greedy_solve(L,1000);
    int type=ATOMIC_MOVE;
    bool PIXIE=true;
    if(argc>=5 && string(argv[4])== "--FEG") PIXIE=false;
    if(argc>=6 && string(argv[5])== "--compound_moves") type=SD_MOVE;

    //AQUI EMPIEZA EL ALGORITMO DEL PROFE, aqui saco una copia de lo que hace actualmente
    
    Layout * nuevo = new Layout(L);

    nuevo->lowb();
    //ELIMINAR ESTO LUEGO
    //return 0;
    //ELIMINAR ESTO LUEGO

    if (beams==0){
        if(PIXIE) steps = pixie_solve(L,1000);
        else steps = greedy_solve(L,1000);
    }
    else steps = BSG(L, beams, type, best_lay, PIXIE);
    cout << steps <<"\t" << (float( clock () - begin_time ) /  CLOCKS_PER_SEC) << endl;
    

    const clock_t begin_tree = clock();
    Tree * arbolTest= new Tree(nuevo,0);
    cout << (float( clock () - begin_tree ) /  CLOCKS_PER_SEC) << endl;
    delete arbolTest;
    //for(int m: best_lay.bsg_moves) cout << m  << " ";
    //cout << endl;
    //recreate(L,best_lay.bsg_moves);
    return 0;    

}

