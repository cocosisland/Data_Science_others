/* RECHERCHE DE SOLUTION(S) D'UNE FONCTION
Le but ici est d'implémenter la méthode par dichotomie (algorithme permettant de trouver les zeros d'une fonction), 
et de l'appliquer à des fonctions.
*/


#include <iostream>
#include <string>
#include <fstream>
#include <cmath>
#define imax 200        // plus on augmente le nb d'itérations, plus on gagne en precision

using namespace std;

double f(double x) {

    // TEST SUR UNE FONCTION QUELCONQUE
    /*
    double y = x - cos(x);
    //double y = pow(x,2) - 4;
    //double y = cos(x);
    */


    // TEST SUR DIAPASON
    
    //double y = cosh(M_PI*x)*cos(M_PI*x)+1;
    double y = 1./cosh(M_PI*x) + cos(M_PI*x);   // meilleur car 1/cosh s'annule a l'infini, il nous reste que le cos,
                                                // bcp plus facile a exploiter et voir ses zeros. Vu que c'est la meme 
                                                // fonction sous 2 expressions differentes, cela donne bien les memes solutions.

    return y;
}

double dichotomie(double a, double b, double eps, bool *convergence) {
    double x;
    int compteur=0;
    f(x);
    if (f(a)*f(b) > 0) {
        cout<<"error : f ne s'annule pas dans l'intervalle donné"<<endl;
        return 0;
    }
    else {
        while (fabs(f(a)) > eps && fabs(f(b)) > eps) {
            for (int i=0; i<imax; i++) {
                if (f(a)*f(b) < 0) {
                    double moy = (a+b)/2.;
                    if f((a)*f(moy) < 0) b=moy;
                    if f((a)*f(moy) < 0) a=moy;
                    compteur++; cout<<compteur<<endl;
                }
                else break;
            }
        }
    double zero = (a+b)/2.;
    return zero;
    }
}



int main(void) {

// TEST SUR UNE FONCTION QUELCONQUE
/*
    bool convergence;       / teste la convergence. renvoie 1 si ca convergence
    cout<<dichotomie(0, 5, 0.01, &convergence)<<" "<<convergence<<endl;
*/
/*
Il faut judicieusement choisis a et b grace au tracé de la courbe, afin que (a) et f(b) soient de signes opposés
et qu'il n'y ait qu'une seule solution dans cet intervalle.
Pour la fonction y=x*x-4 par exemple, on a pour solutions :
Avec imax~2 on trouve -1.99707 (resultat approximatif car pas assez d'iterations)
Avec imax>20 on trouve -2 (resultat exact).
*/


// TEST SUR DIAPASON

double sol1, sol2, sol3, n1, n2, n3;
double R=7874; E=196e9, l=0.126, k=0.0025;

sol1 = dichotomie(0,, 1, 0.001);
n1 = M_PI/(2*l*l)*sqrt(E*k*k/R)*sol1*sol1;
cout<<n1<<endl;     // donne 439.643 Hz (frequence fondamentale du diapason ù1=440 Hz donc bon!)

sol2 = dichotomie(1, 2, 0.01);
n2 = M_PI/(2*l*l)*sqrt(E*k*k/R)*sol2*sol2;
cout<<n2<<endl;     // donne 2755.2 Hz (ù2~6*ù1)

sol3 = dichotomie(2, 3, 0.01);
n3 = M_PI/(2*l*l)*sqrt(E*k*k/R)*sol3*sol3;
cout<<n3<<endl;     // donne 7714.63 Hz (ù3~18*ù1)


return 0;

}