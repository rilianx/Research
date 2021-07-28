
#include <map>
#include <set>
#include <vector>
#include <list>
#include <iterator>
#include <cmath>
#include <iostream>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <stdexcept>
#include <unordered_map>
#include <functional> //for std::hash
#include <typeinfo> // para testing
#include <algorithm>


#ifndef _LAYOUT_
#define _LAYOUT_

using namespace std;


namespace cpmp { 

class Layout {
    public:
        vector <vector <int>> stacks;

        vector<int> sorted_elements; /*for each stack*/
        int total_elements;
        int unsorted_stacks = 0;
        int unsorted_elements = 0;
        int steps = 0;
        int full_stacks = 0;
        int lb;
        list <int> bsg_moves;
        set <int> dismantled_stacks;
        list < pair<int,int> > seq;

        //multimap <int ,int> gv2index; //for the beamsearch (type:SDPP)
        int last_sd =-1; /*last dismantled stack*/

        static int H;

    public:

        Layout(string filename);

        int move(int i, int j);

        //Return false if it detect an unrelated move symmetry
        bool validate_move(int s1, int s2){
            if (s1 < s2) return true;

            int h1= stacks[s1].size(); int h10=h1;
            int h2= stacks[s2].size(); int h20=h2;

            //se desea saber si el mov: s1->s2 se puede realizar antes,
            //si es así: return False
            for(auto ss : seq){
                int so = ss.first;
                int sd = ss.second;
                if (so==s1) h1+=1; else if (sd==s1) h1-=1;
                if (so==s2) h2+=1; else if (sd==s2) h2-=1;
                if (h2==H) return true;
                if (h2<h20 || h1<h10) return true; //stacks variantes
                if (h20==h2 && h10==h1) return false; //stacks invariantes
            }
            return true; //first move
        }

        bool validate_move2(int st, int sd){
            vector<int> h(stacks.size());
            for (int i=0; i<stacks.size();i++) h[i]=stacks[i].size();
            vector<bool> variant_stacks(stacks.size(), false);

            for(auto ss : seq){
                int so = ss.first;
                int sdd = ss.second;
                
                if (sdd==st && !variant_stacks[so]){
                    if (stacks[so].size()==h[so] && stacks[st].size()==h[st] && stacks[sd].size()==h[sd]) 
                        return false;
                }
                h[so]+=1; h[sdd]-=1;
                if (h[sdd]<stacks[sdd].size()){ //variant stack
                    if (sdd==st || sdd==sd) return true;
                    variant_stacks[sdd]=true;
                }
            }
            return true; //first move
        }



        bool is_sorted(int j) const{
            return (stacks[j].size() == sorted_elements[j]);
        }

        // Optimal: O(1)
        int capacity(int s_o, int s_d=-1){
            int n=1;
            int len=stacks[s_o].size();
            if(s_d!=-1) {len+=stacks[s_d].size(); n++;}

            return ( (Layout::H) * (size()-n) - (total_elements-len) );
        }

        int sum_stack(int i) const{
            int sum =0;
            for(int c : stacks[i]) sum+=c;
            return sum;
        }

        //reachable height of stack i by only performing BG moves
        int reachable_height(int i) const;

        int size() const {return stacks.size();}


        static int compute_sorted_elements(vector<int>& stack){
            if (stack.size()==0) return 0;
            int sorted_elements=1;
            while(sorted_elements<stack.size() && stack[sorted_elements] <= stack[sorted_elements-1] )
                sorted_elements++;
            

            return sorted_elements;
        }

        static int gvalue(vector<int> stack){
            if (stack.size()==0) return 100;
            else return stack.back();
        }

        void print() const{
            for(auto s : stacks){
                cout << "[" ;
                for(auto e : s) cout << e << " ";
                cout << "]\n";
            }
        }

        //Its dangerous to go alone hash this
        auto hash() -> int
        {
            std::string hash = "";


            for (auto s : stacks)
            {
                for (auto e : s)
                {
                    hash += to_string(e);
                    hash +=".";
                } //cout << e << " ";
                hash+="-";
            }

            //cout << hash;
            //printf("\n");
            //printf("\n");

            std::hash<std::string> hasher;
            auto hashed = hasher(hash);
            //cout << "habemus hash:  ";
            //cout << hashed << '\n';
           return hashed;
        }


        float promedio()
        {
            int l =stacks.size();
            float suma=0;
            for (int i = 0;i<l;i++)
            {
                //Saco el largo del stack
                int stack_size = stacks[i].size();
                //Lo paso al vector
                vector<int> v = stacks[i];

                int flag = 0;
                for (int j = 0;j<stack_size-1;j++)
                {
                    if (flag == 1 )
                    {
                        suma += v[j+1];
                    }
                    else
                    {
                         if (v[j]<v[j+1])
                        {
                            suma += v[j+1];
                            flag = 1;
                        }
                    }
                }
                //cout << suma << "\n";

            }
            
            return suma/unsorted_elements;
        }
        float desordenados()
        {
            int l =stacks.size();
            float suma=0;
            for (int i = 0;i<l;i++)
            {
                //Saco el largo del stack
                int stack_size = stacks[i].size();
                //Lo paso al vector
                vector<int> v = stacks[i];

                int flag = 0;
                for (int j = 0;j<stack_size-1;j++)
                {
                    if (flag == 1 )
                    {
                        suma += 1;
                    }
                    else
                    {
                         if (v[j]<v[j+1])
                        {
                            suma += 1;
                            flag = 1;
                        }
                    }
                }
                //cout << suma << "\n";

            }
            
            return suma;
        }
        int min_nx()
        {
            int l =stacks.size();
            float suma=0;
            vector <int> valores;
            for (int i = 0;i<l;i++)
            {
                suma = 0;
                //Saco el largo del stack
                int stack_size = stacks[i].size();
                //Lo paso al vector
                vector<int> v = stacks[i];

                int flag = 0;
                for (int j = 0;j<stack_size-1;j++)
                {
                    if (flag == 1 )
                    {
                        suma += 1;
                    }
                    else
                    {
                         if (v[j]<v[j+1])
                        {
                            suma += 1;
                            flag = 1;
                        }
                    }
                }
                //cout << suma << "\n";
                valores.push_back(suma);
            }

            int min_value = *std::min_element(valores.begin(),valores.end());
            return min_value;
        }

        int suma()
        {
            int l =stacks.size();
            float suma=0;
            for (int i = 0;i<l;i++)
            {
                //Saco el largo del stack
                int stack_size = stacks[i].size();
                //Lo paso al vector
                vector<int> v = stacks[i];

                int flag = 0;
                for (int j = 0;j<stack_size-1;j++)
                {
                    if (flag == 1 )
                    {
                        suma += v[j+1];
                    }
                    else
                    {
                         if (v[j]<v[j+1])
                        {
                            suma += v[j+1];
                            flag = 1;
                        }
                    }
                }
                //cout << suma << "\n";

            }
            
            return suma;
        }


        

        vector<int> valores_demanda()
        {
            int l =stacks.size();
            vector <int> valores;
            for (int i = 0;i<l;i++)
            {
                //Saco el largo del stack
                int stack_size = stacks[i].size();
                //Lo paso al vector
                vector<int> v = stacks[i];

                int flag = 0;
                for (int j = 0;j<stack_size-1;j++)
                {
                    if (flag == 1 )
                    {
                        valores.push_back(v[j+1]);
                    }
                    else
                    {
                         if (v[j]<v[j+1])
                        {
                            valores.push_back(v[j+1]);
                            flag = 1;
                        }
                    }
                }
                //cout << suma << "\n";

            }
            
            //Una vez obtenidos los valores se eliminan los repetidos con un set

            

            //cout << "Valores:\n";   

            /*for (int h=0; h<valores.size();h++)
            {
                cout << valores[h] << endl;
            }*/
            return valores;

        }

        vector<int>filtro(vector<int> valores)
        {
            set<int> s( valores.begin(), valores.end() );
            valores.assign( s.begin(), s.end() );
            return valores;
        }

        vector<int>demanda(vector<int> valores,vector <int> filtro)
        {
            vector<int> demanda;
            
            for (int i=0;i<filtro.size();i++)
            {
                int contador = 0;
                int k = filtro[i];
                for (int j=0;j<valores.size();j++)
                {   
                    //Si es mayor o igual al valor requerido
                    if (valores[j]>=k)
                    {
                        contador += 1;
                    }
                }

                //Al terminar con un numero, pushback no mas
                demanda.push_back(contador);
            }

            return demanda;
        }

        vector<int> av_slots(vector<int> valores)
        {
            int l =stacks.size();
            vector<int> slots;
 
            for (int h=0;h<valores.size();h++)
            {
                int suma=0;
                int key = valores[h];
                for (int i = 0;i<l;i++)
                {
                    //Saco el largo del stack
                    int stack_size = stacks[i].size();
                    //Lo paso al vector
                    vector<int> v = stacks[i];

                    int flag = 0;
                    for (int j = 0;j<stack_size-1;j++)
                    {
                        //Aqui se desordena la columna
                        if (v[j]<v[j+1])
                        {
                            flag = 1;

                            //Si hay slots
                            if (v[j]>=key)
                            {
                                /*//Se suman todos los posibles slots de la columna
                                //ALTURA MAXIMA - LA UBICACION DEL ULTIMO CONTENEDOR BIEN PUESTO [altura total-(j+1)]
                                cout << "\nStack ";
                                cout << i;
                                cout << " evaluado en ";
                                cout << key;
                                cout << " obtuvo: ";
                                cout << H-(j+1);
                                cout << " EN J= ";
                                cout << j+1;
                                cout << " Y H= ";
                                cout << H;
                                cout << "\n";*/
                                suma += H-(j+1);
                            }
                        }
                    }
                    //Esto es si no se desordena
                    /*if (flag == 0)
                    {
                        //Si esta ordenada se ve si se puede lograr algo
                        if (v[v.size()-1]>=key)
                        {
                            suma += H-v.size();
                        } 
                    }*/
                    //cout << suma << "\n";
                    
                }
                slots.push_back(suma);
            }
            return slots;
        }

        int lowb()
        {
            
            int bx = unsorted_elements;
            int Nbx = bx+min_nx();
            //SIMPLE RETORNAR AQUI
                //SIMPLE HERE
            lb= bx+steps;
            return lb;
            //return bx+steps;

            
            //Hasta aqui esta bien

            vector <int> valores=valores_demanda();
            vector <int> valores_filtrados=filtro(valores);


            //cout << "\valores demanda:\n";
            //printVector(valores_filtrados);
            //cout << "\nFIN demanda\n";
            vector <int> demand=demanda(valores,valores_filtrados);

            //cout << "\nDEMANDA:\n";
            //printVector(demand);
            //cout << "\nFin demanda\n";

            //HASTA AQUI TODO BIEN Y BONITO


            vector <int> slots =av_slots(valores_filtrados);
            //cout << "\nSLOTS:\n";
            //printVector(slots);
            //cout << "\nFin de Slots\n";

            //Se calcula la carencia
            vector <int> carencia;

            //cout << valores.size();
            //cout << "\n";
            for (int i=0;i<valores.size();i++)
            {
                carencia.push_back((demand[i]-slots[i]));
            }

            

            //Se busca la mayor carencia dentro del vector carencia y su ubicacion
            int aux=0;
            int may=-1;
            for (int i = 0;i<valores.size();i++)
            {
                if (carencia[i]>aux)
                {
                    aux=carencia[i];
                    may=i;
                }
            }

            //cout <<"EO\nMAYOR CARENCIA ";
            //cout << aux;

            //cout << "\n";
            //Cuantos stacks necesito al menos para hacer la magia
            int ns=(ceil(H)/aux);
            //Finally, el LB es 
            //cout << Nbx+ns; 
            lb = Nbx+ns+steps;

            //cout << lb;
        }

        int bigSlot()
        {
            int l =stacks.size();
            int aux=0;
            for (int i = 0;i<l;i++)
            {
                //Saco el largo del stack
                int stack_size = stacks[i].size();
                //Lo paso al vector
                vector<int> v = stacks[i];

                int flag = 0;
                for (int j = 0;j<stack_size-1;j++)
                {

                    if (v[j]<v[j+1])
                    {
                        flag = 1;
                    }
                }
                //En caso que flag sea igual a 0, significa que esta ordenado
                if (flag == 0)
                {
                    int slots = H-v.size();
                    //Si los slots disponibles son mas grandes en aux queda eso
                    if (aux <= slots)
                    {
                        aux = slots;
                    }
                }

            }
            
            return aux;
        }


        
        void printVector(vector <int> valores)
        {
            for (int h=0; h<valores.size();h++)
            {
                cout << valores[h] << endl;
            }
        }
        struct compare
        {
            int key;
            compare(int const &i): key(i) {}
        
            bool operator()(int const &i) {
                return (i == key);
            }
        };



};
}


#endif