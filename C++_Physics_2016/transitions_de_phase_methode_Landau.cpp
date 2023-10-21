/* THERMODYNAMIQUE
Le but est de modeliser les transitions de phase (i.e. changements d'etat : fusion, changement de structure de la matiere).
L'un des modeles les plus importants de transitions de phase est celui de Landau dans lequel l'energie d'un systeme est exprimee comme
un polynome.
*/

#include <iostream>
#include <string>
#include <fstream>
#include <cmath>
//#define T=Tc/2      // a T fixe (mettre en commentaire si T varie)
// T non fixee : on veut tracer la courbe des differents angles x sur lesquels la bille se trouve, en fontion de la temperature T.
 

using namespace std;


void landau(double T, double x, double *y, double *dy) {
    double n, R, l, m, gamma, w0, g, T, Tc, S, x0, P;
    g=9.81; l=0.1; m=0.006; R=8.32; x0=1; S=0.0001; P=200;
    n=P*S*l*2/(R*300);      // calcul du nb de moles avec PV=nRT
    Tc=m*g*l*x0*x0/(2*n*R);
    T=Tc/2;
    gamma=2*n*R/m/l/l;
    w0=sqrt(g/l);

    *y = sin(x)/x*(x0*x0-x*x) - gamma*T/w0/w0;
    *dy = cos(x)/x*(x0*x0-x*x) - sin(x)*(x0*x0+x*x)/x/x;
}


double newton(double T, int f, double x0, double eps) {
    double x=x0, y, dy;     // x0 le point de depart
    int i=0;
    int imax=100;

    if (f==4) {
        landau(x, &y, &dy);
        while (fabs(y)>eps) {
            landau(T, x, &y, &dy);
            x = x-(y/dy);
            i++;
            if (i>imax) {
                break;
            }
        }
    }
    return x;
}



int main(void) {

    // a T fixee :
    //cout<<newton(4, 1, 0.01)<<endl;     // pour x=0.677899 radian on a un 0 de l'equation
    // a T=Tc/2, on a la bille a l'equilibre situee a un angle x=0.677899 rad


    // a T non fixee :
    // ofstream fichier("temperature.res");
    double T;
    double Tc=220.7;
    for (int i=0; i<=Tc; i++) {
        newton(T, 4, 1, 0.01);

    }
    // fichier.close();

    cout<<newton(T, 4, 1, 0.01)<<endl;

    return 0;
}



