/* MECANIQUE QUANTIQUE
Le but est de resoudre l'equation de Schrodinger par la methode des differences finies, qui consiste en la discretisation du probleme :
on discretise une fonction continue en un nombre fini de points n. Pour ce faire, on doit donner un intervalle de definition suppose
fini a cette fonction. Par ex, une droite de longueur L discretisee en n parts egales de longueur dx -> L = n*dx
Et lorsqu'il s'agit de coordonnees, on remplace la variable x par n variables discretes xi -> xi = (i-1)*dx , i E [1,n] , i E Z
Cette simulation permet de visualiser l'amplitude de la fonction d'onde du puits de potentiel.
*/

#include <iostream>
#include <string>
#include <fstream>
#include <cmath>

using namespace std;

/* Fonction tridiag qui fait appel a la bibli LaPack et au sous-programme 'dsteqr' ecrite en Fortran et qui permettra de resoudre notre systeme d'equations.*/

extern "C"
void dsteqr_(char *, int *, double [], double [], double [], int *, double[], int *);

void tridiag(int n, double d[], double e[], double z[]) {
/* Appel du sous-programme dsteqr de LaPack : calcul des valeurs et vecteurs propres d'une matrice tridiagonale symetrique.*/

    int info;   //diagnostic
    double work[2*n-2];     //espace de travail
    char compz='v';     //mettre 'n' pour n'avoir que les valeurs propres

    dsteqr_(&compz, &n, d, e, z, &n, work, &info);      //scalaires pointeurs
    if (info==0) cout<<"La diagonalisation s'est bien passee"<<endl;
    else cout<<"Attention ! DQTEQR : info = "<<info<<endl;

}


double potentiel(double x) {
    //double v=x*x;     //potentiel harmonique
    double v=0;         //potentiel puits infini
    return v;
}


int main(void) {

    int i, j, p, n=100;
    double L=5;
    double dx, x[n], v[n], z[n*n], d[n], e[n-1];
    double a=1, r1=-2, r2=-0.5, r3=0, r4=2;

    ofstream fi("vap.res");                 //fichier contenant les VAP donc les energies calculees
    ofstream fi2("vep.res");                //fichier contenant les VEP calcules    
    ofstream fi3("energie_theo.res");       //fichier contenant les energies theoriques
    ofstream fi4("fct_onde.res");           //fichier contenant les fonctions d'onde theoriques
    ofstream fi5("energie_theo_harm.res");

    dx = L/(n+1);

    for (i=0; i<n; i++) {
        x[i] = -L/2.+(i+1)*dx;
        //v[i] = potentiel(x[i]);       //puits infini
        //v[i] = 0.5*x[i]*x[i];         //harmonique
        v[i] = a*(x[i]-r1)*(x[i]-r2)*(x[i]-r3)*(x[i]-r4);       //double puits
        d[i] = 2./pow(dx,2)+v[i];       //elements diagonaux de H
        if (i<n-1) e[i]=-1./pow(dx,2);  //elements sous-diagonaux de H
    }

    for (i=0; i<n; i++) {       //matrice identite (en entree)
        for (j=0; j<n; j++) {
            if (i==j) z[i+n*j]=1;
            else z[i+n*j]=0;
        }
    }


    // Pour rechercher les valeurs et vecteurs propres, on appelle la fonction tridiag.

    tridiag(n,d,e,z);

    for (i=0; i<n; i++) {
        fi<<i<<" "<<d[i]<<endl;     // Valeurs propres
        fi2<<x[i];
        for (j=0; j<n; j++) {
            fi2<<" "<<z[i+n*j];     // Vecteurs propres
        }
        fi2<<endl;
    }


    // ENERGIE theorique

    double Ep_theo, Ep_theoh, y, t;
    for (p=1; p<n; p++) {
        Ep_theo = pow(M_PI*p/L, 2);
        //Ep_theoh = sqrt(2.)*(p+0.5);
        fi3<<p<<" "<<Ep_theo<<endl;
        //fi5<<p<<" "<<Ep_theoh<<endl;
    }


    // FONCTIONS D'ONDE theorique

    for (p=1; p<5; p++) {       // 4 premieres fonctions d'onde
        for (t=-L/2.; t<=L/2.; t+=dx) {
            if (p%2==1) y=sqrt(2./L)*cos(p*M_PI*t/L);
            else y=sqrt(2./L)*sin(p*M_PI*t/L);
            fi4<<t<<" "<<y<<endl;
        }
    fi4<<t<<" "<<y<<endl;
    }

    fi.close();
    fi2.close();
    fi3.close();
    fi4.close();
    fi5.close();

    return 0;

}

