
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

using namespace std;
using namespace cpmp;




class Nodo
{
    Layout * actual;
    Nodo * padre;
    list <Nodo *> hijos;
    static list <Nodo *> pa;

    int nivel;

    //Para niveles inferiores
    Nodo::Nodo(Layout l, int lvl, Nodo * padre)
    {
        //Se copypastea el layout
        this->actual= new Layout(*l);
        //Se adjunta su nivel
        this->nivel =lvl;
        //Se guarda el padre
        this->padre = padre;
    }
    //Para nivel 0
    Nodo::Nodo(Layout l,int lvl)
    {
        //Se copypastea el layout
        this->actual= new Layout(*l);
        //Se adjunta su nivel
        this->nivel =lvl;
    }
    /*************************************************************/
    ///////////////////////Funciones///////////////////////////////
    /*************************************************************/

    public:
        void busqueda()
        {
            Nodo * temp;
            
            list::iterator iter = this->pa.begin();
            int flag = 0;
            while (iter != this->pa.end())
            {
                temp = *iter;
                //if los layout son equals.
                //se queda con el de menos nivel y cambia el flag 
                iter++;
            }

            //Si flag es igual, se agrega con su nivel actual
            if (flag == 0)
            {
                this->pa.insert()
            }
        }
        void generarHijos(int limite)
        {
            int stacks = this->actual->stacks.size();
            int i,j;

            //Por cada stack
            for (i=0;i<stacks;i++)
            {
                //Se mueve al resto
                for (j=0;j<stacks;j++)
                {
                    //Si no es el mismo stack
                    if (i != j)
                    {
                        //Si la columna objetivo no esta llena
                        if (stacks[j].size() != this->actual::H)
                        {
                            //DeepCopy del anterior
                            Layout * nuevo = new Layout(*this->actual);
                            //Se realiza el movimiento
                            nuevo.move(i,j);
                            //Se crea un nuevo nodo
                            Node * niu = new Nodo(nuevo,this->level+1,this);
                            //Si nivel es menor al limite que siga creando hijos
                            if (niu->level <limite)
                            {
                                //Crea sus hijos
                                niu.generarHijos(limite);
                                //Esto deberia generar hijos y ligarlos a los hijos anteriores hasta el limite
                            }
                            //Se inserta el nodo nuevo
                            hijos.insert(*niu);
                        }
                    }
                }
            }

        }
}

class Tree
{
    Nodo * base;
    int limite;

    //Constructores
    Tree::Tree(Layout l, int lvl)
    {
        //Se aprovecha el constructor del nodo
        this->base = new Nodo(l,lvl);

        //Se generan los hijos, porque si
        base.generarHijos(this->limite);

    }
    /*************************************************************/
    ///////////////////////Funciones///////////////////////////////
    /*************************************************************/


}


//**************************************************************

int main(int argc, char * argv[])
{

    //se define el layout
    Layout::H = std::atoi ("12");
    string path("..\\Instancias\\CVS\10-6\\data10-6-10.dat");
    int beams = std::atoi ("0");
    Layout L(path), best_lay(path);
    const clock_t begin_time = clock();
    int steps;

    

    
}
