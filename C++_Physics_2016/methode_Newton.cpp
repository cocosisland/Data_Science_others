/* RECHERCHE DE SOLUTION(S) D'UNE FONCTION
Le but ici est d'implémenter la méthode de Newton-Raphson (algorithme permettant de trouver les zeros d'une fonction), 
et de l'appliquer à des fonctions.
Nous verrons que nous avons nettement moins d'iterations a faire que pour la methode par dichotomie.

Methode de Newton : x(n+1) = x(n) - f(x(n))/f'(x(n))

*/


#include <iostream>
#include <string>
#include <fstream>
#include <cmath>
#define imax 2000        // plus on augmente le nb d'itérations, plus on gagne en precision

using namespace std;

double f(double x) {

    // TEST SUR UNE FONCTION QUELCONQUE

    //double y = x - cos(x);
    //double y = 0.5 - tanh(x-1);
    //double y = sinx);
    double y = 1./cosh(M_PI*x) + cos(M_PI*x);

    return y;
}


void fonction(double x, double *y, double *dy) {    // fonction qui renvoie la valeur et la derivee d'une fonction en un point
    float h=0.01;       // ca ne serait pas aussi precis que si j'avais donne la valeur de la derivee sous sa fformule precise, 
                        // a cause de la precision que j'ai donne a h, mais ca permet de calculer la derivee de n'importe quelle
                        // fonction de maniere generale, contenue dans la fonction f.
    *y = f(x);
    *dy = (f(x+h) - f(x))/h;
}


// a est la point de depart, eps est la precision

double newton(double a, double eps) {
    int i=0;
    int compteur=0;
    double x=a, y, dy;
    fonction(a, &y, &dy);

    while (fabs(y)>eps) {
        x = x-(y/dy);
        compteur++; cout<<compteur<<endl;   // 3-4 iterations seulement..contre presque 200 avec la methode par dichotomie
        i++;

        if (i>imax) break;
        fonction(x, &y, &dy);
    }
    return x;
}



int main(void) {

cout<<newton(1.4, 0.001)<<endl;
// Pour y = x-cos(x), en partant de x=0, le 1er zero se trouve a 0.739137.
// Graphiquement on verifie que c'est correct.

/* Pour sin(x), avec x0=0.01 je ne fais qu'1 seule iteration (?) et trouve le zero en 0.
Tandis qu'avec x0=1.55, je fais 5 iterations et trouve le zero en -63 = -20pi.
On a donc deux solutions differentes. Sin(x) est periodique et possede une infinite de solutions, newton renvoie celle la plus
proche du point de depart.*/

/* Pour 0.5-tanh(x), quelque soit le nombre d'iterations, newton ne trouve pas de zero. Car cette methode qui se sert des tangentes
rend ces tangentes toujours de +en+ plates (horizontales), ce qui n'aboutit jamais au zero. On pourrait trouver ce zero en donnant
x0 tres proche de la solution, dans ce cas la methode des tangentes fonctionne. Donc pour x0=1.4 je trouve le zero en 1.55.
Cela marche avec la methode par dichotomie egalement.*/


// TEST SUR DIAPASON

double sol1, sol2, sol3, n1, n2, n3;
double R=7874; E=196e9, l=0.126, k=0.0025;

sol1 = dichotomie(0,, 1, 0.001);
n1 = M_PI/(2*l*l)*sqrt(E*k*k/R)*sol1*sol1;
cout<<n1<<endl;     // donne 439.643 Hz (frequence fondamentale du diapason ù1=440 Hz donc bon!)
                    // 2 iterations seulement !

sol2 = dichotomie(1, 2, 0.01);
n2 = M_PI/(2*l*l)*sqrt(E*k*k/R)*sol2*sol2;
cout<<n2<<endl;     // donne 2754.91 Hz (ù2~6*ù1)
                    // 2 iterations seulement !

sol3 = dichotomie(2, 3, 0.01);
n3 = M_PI/(2*l*l)*sqrt(E*k*k/R)*sol3*sol3;
cout<<n3<<endl;     // donne 7714.63 Hz (ù3~18*ù1)
                    // 3 iterations seulement !


return 0;

}

/*
CONCLUSION:
Le methode de Newton est un algorithme tres efficace, avec tres peu d'iterations necessaires comparé a la methode par dichotomie 
(facteur ~80 en moins!), pour une precisions quasi egale.
Cependant, cette methode reste fragile lorsqu'ona  des fonctions telles que tanh(x-1) comme on vient de le voir, car elle ne parvient pas
a trouver la solution. Il faut donc, avant de se lancer a la recherche de zeros d'une fonction, bien choisir la methode appropriee.
*/