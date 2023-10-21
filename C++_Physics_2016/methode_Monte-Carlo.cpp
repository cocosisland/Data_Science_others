/* MARCHE ALEATOIRE
Le but est de simuler une marche aleatoire, point de depart de nombreuses modelisations physiques decrivant le mouvement brownien, 
la diffusion, les polymeres etc. Le modele de base est celui d'une particule se trouvant sur une ligne, sur laquelle elle se deplace
par pas discrets qui s'effectuent au hasard a droite ou a gauche pendant chaque unite de temps. La particule part de l'origine x=0 et
la marche s'arrete au bout de n pas.
Afin de determiner les proprietes stats de ce modele, il est necessaire d'effectuer un grand nombre de marches (toutes de meme n),
et de calculer la position moyenne du marcheur, la variance, la distance moyenne de l'origine a la fin de la marche etc.
Nous pouvons egalement visualiser a quoi ressemblerait 1 marche.
*/

#include <iostream>
#include <string>
#include <fstream>
#include <cmath>
#include <cstdlib>      // pour generer des nombres aleatoires en appelant rand et srand
#include <ctime>        // pour appeler time(NULL)
#define pas 1000
#define NMARCHES 100
//#define NMARCHES 1

using namespace std;

// fonction qui genere une coordonee aleatoire comprise dans [0;1[
double alea(void) {
    double x = rand()/(RAND_MAX+1.0);
    return x;
}


int main(void) {
    ofstream fichier1("1marche.res");       // resultats d'une seule marche pour pouvoir la visualiser graphiquement
    ofstream fichierN("Nmarches.res");      // resultats d'un grand nb de marches pour les statistiques
    srand(time(NULL));

    int compteur_distances=0;   //compteur qui additionne toutes les distances finales
    double moyenne_distance;    //calcule la distance finale en moyenne
    int origine=0;              //compte le nb de fois qu'il revient a l'origine
    double moyenne_origine;     //calcule en moyenne le nb de fois ou il revient a l'origine
    double tot_dfinal_carre=0;  //distance finale au carre (quadratique)
    double dist_quad=0;         //distance quadratique moyenne


    if (NMARCHES>1) {
        for (int n=1; n<=NMARCHES; n++) {
            int dist;
            int x=0;
            //cout<<0<<" "<<x<<endl;
            //fichierN<<0<<" "<<x<<endl;
            for (int t=1; t<=pas; t++) {
                double i=alea();
                if (i<0.5) x+=-1;
                else x+=1;          // 1/2 chance que +1 et 1/2 chance que -1
                if (x==0) origine++;
                //cout<<t<<" "<<x<<endl;
                //fichierN<<t<<" "<<x<<endl;
            }
            dist = fabs(x);
            //cout<<"Distance finale a l'origine : "<<dist<<endl;   //valeur absolue car distance est positive
            compteur_distances = compteur_distances + dist;
            tot_final_carre += x*x;
            cout<<"distance : "<<compteur_distances<<endl;
        }

        moyenne_distance = compteur_distances/NMARCHES;
        moyenne_origine = origine/NMARCHES;
        dist_quad = tot_dfinal_carre/NMARCHES;
        cout<<"distance moyenne : "<<moyenne_distance<<endl;
        cout<<"moyenne du nb de fois ou il revient a l'origine : "<<moyenne_origine<<endl;
        cout<<"distance quadratique moyenne : "<<dist_quad<<endl;

        fichierN.close();
    }


    else {
        for (int n=1; n<=NMARCHES; n++) {
            int dist;
            int x=0, y=0;
            //cout<<x<<" "<<y<<endl;
            //fichier1<<x<<" "<<y<<endl;
            for (int t=1; t<=pas; t++) {
                double i=alea();

                if (i>=0 && i<0.25) x+=0.1;
                if (i>=0.25 && i<0.5) x-=0.1;
                if (i>=0.5 && i<0.75) y+=0.1;
                if (i>=0.75 && i<1) y-=0.1;

/*
                int s;
                if (i>=0 && i<0.25) s==1;
                if (i>=0.25 && i<0.5) s==2;
                if (i>=0.5 && i<0.75) s==3;
                if (i>=0.75 && i<1) s==4;

                switch(s) {
                    case 1:
                        x+=0.1; break;
                    case 2:
                        x-=0.1; break;
                    case 3:
                        y+=0.1; break;
                    case 4:
                        y-=0.1; break;
                }
*/

                if (x==0 && y==0) origine++;
                //cout<<x<<" "<<y<<endl;
                fichier1<<x<<" "<<y<<endl;
            }

        dist = sqrt(x*x + y*y);
        cout<<"Distance finale a l'origine : "<<dist<<endl;
        dfinal_carre = pow(dist, 2);
        cout<<"distance quadratique : "<<dfinal_carre<<endl;
    }

    cout<<"nb de fois ou il revient a l'origine : "<<origine<<endl;
    fichier1.close();
    return 0;

}