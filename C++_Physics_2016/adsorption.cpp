/* ADSORPTION
Le but est de modeliser le phenomene d'adsorption de particules sur une surface de dimension determinee.
Le phenomene etant aléatoire, pour le modeliser correctement, plusieurs contraintes sont imposees.
Pour le visualiser, nous ferons appel aux bibliotheques g2.
*/

#include <iostream>
#include <string>
#include <g2.h>
#include <g2_X11.h>     // bibliotheques graphiques g2
#include <unistd.h>     // bibli necessaire pour l'appel de usleep
#include <cstdlib>      // pour l'appel de rand
#include <cmath>
#define L 20.0          // longueur coté du carre
#define R 0.4           // rayon du disque
#define MAX_TRIES 1000  // nombre max d'echecs consecutifs possibles pour placer 1 particule
#define kmax 1000.0     // nombre d'experiences

using namespace std;

void graphe(int n_atom, double x[], double y[]) {
    int h=g2_open_X11(400,400);
    char c;
    g2_rectangle(h,0,0,L*20,L*20);
    for (int i=0; i<n_atom; i++) {
        for (int j=0; j<n_atom; j++) {
            g2_pen(h,2);
            g2_filled_circle(h, x[i]*20, y[i]*20, 10);
            // faire R*20 pour rester a l'echelle
        }
    }
    cin>>c;
}

/*
x et y sont les coordonnees prises aleatoirement afin de placer une particule sur la surface de dimension predefinie (L)
Les valeurs autorisees de x et y sont comprises dans l'intervalle [R; L-R]
Lorsque 2 particules se chevauchent, (x,y) etant les coordonnees d'une particule adsorbee et (x',y') les coordonnes
de la nouvelle particule a placer, alors : 
sqrt(x²+y²) + sqrt(x'²+y'²) <= 2*R
*/

double coord(void) {    // genere et renvoie nombre aleatoire dans (R; L-R)
    double nb_alea = rand()/(RAND_MAX+1.0)*(L-2*R) + R;
    return nb_alea;
}


/*
xnew et ynew sont les nouvelles coordonnes. On poursuit tous les elements des tableaux x[N] et y[N]
qui contiennent les coordonnees de toutes les autres particules deja adsorbees. Si les particules
se chevauchent, la fonction renvoie 0, sinon 1, a la fonction adsorption.
En gros on teste s'il y a ou pas de la place libre pour une nouvelle particule.
*/


int place_libre(double x[], double y[], double xnew, double ynew, int n_atom) {
    for (int i=0; i<n_atom; i++) {
        if ((xnew-x[i])*(xnew-x[i]) + (ynew-y[i])*(ynew-y[i]) < 4*R*R) {
            return 0;   // la nouvelle particule chevauche une ancienne
        }
    }
    return 1;   // place libre, aucun chevauchement
}


int adsorption(double x[], double y[], int *n_atom) {
    double xnew=coord();
    double ynew=coord();
    if (place_libre(x, y, xnew, ynew, *n_atom) == 1) {
        x[*n_atom] = xnew;
        y[*n_atom] = ynew;
        (*n_atom)++;
        return 1;
    }
    else return 0;
}


int main(void) {
    int NMAX = floor(L*L/(M_PI*R*R));   // nombre max de particules adsorbees esperé
    double x[NMAX];
    double y[NMAX];
    int somme = 0;
    double surf_total_disques_ec1 = 0;
    for (int k=1; k<=kmax; k++) {   // faire l'experience 1000x
        for (int i=0; i<NMAX; i++) {    // initialisation tableaux
            x[i] = 0;
            y[i] = 0;
        }

        init n_atom = 0;
        int echecs = 0;
        while (echecs<=MAX_TRIES) {
            int a = adsorption(x, y, &n_atom);
            if (a==0) echecs++;
            else echecs = 0;
        }

        /*
            if (k==1) graphe(n_atom, x, y);     
            // visualiser graphiquement poour 1 seule experience
            // on aurait pu seulement changer la valeur de k en macro
        cout<<"nombre d'atomes adsorbés : "<<n_atom<<endl;
        */

        somme += n_atom;

        surf_total_disques_ec1 += pow(n_atom*M_PI*pow(R,2), 2);     // somme des X²
        
    }


    // en moyenne sur 1000 experiences :

    int moyenne=somme/kmax;     // moyenne du nb de particules adsorbées
    cout<<moyenne<<endl;
    double surf_total_disques = moyenne*M_PI*pow(R,2);      // surface totale occupee par les particules
    cout<<surf_total_disques<<endl;
    double rapport = surf_total_disques/pow(L,2);       // surf tot occupee / surf²
    cout<<rapport<<endl;
    double ideal = NMAX*M_PI*pow(R,2)/pow(L,2);     // surf tot occupee ideale (theorique) / surf²
    cout<<ideal<<endl;
    double compare = rapport/ideal*100.;        // comparaison
    cout<<compare<<endl;

    double ec1 = surf_total_disques/kmax;       // <X²>
    double ec2 = pow(rapport,2);                // <X>²
    double ecartype = sqrt(ec1 - ec2);
    cout<<ecartype<<endl;

    /*
    On trouve qu'en moyenne, sur 1000 experiences, on a :
    373 particules adsorbees.
    0.468726 est le rapport surface totale occupee par tous les disques / surface du carre.
    Plus de la moitie de la surface du carre reste donc vide.
    Si les particules etaient placees de ma niere ordonnee, on aurait un rapport d'environ 0.999.
    Ici on n'occupe qu'environ 47 % de la surface ideale qu'on pourrait occuper.
    En doublant L (L=40), la moyenne de la fraction occupee de la surface du carre n'evolue que tres peu.
    Elle a pour valeur 0.466212 donc elle baisse un tout petit peu, de facon quasi negligeable.
    Ca peut s'expliquer par le fait qu'en doublant la surface du carre, il y a plus de particules
    qui n'auront pas pu etre adsorbés car ils debordent du carre, en comparaison du carre plus petit.
    Donc plus de particules "rejetées" pour le grand carre que pour le petit, dû aux debordements.
    */

   return 0;

}




/*
Appel de la bibliotheque g2 pour creer une surface sur laquelle on pourrait envoyer nos particules.

#include <iostream>
#include <g2.h>
#include <g2_X11.h>     // bibliotheques servant a declarer les fonctions g2_open/line/circle etc.

using namespace std;

int main(void) {

    char c;

    int h = g2_open_X11(400,400);       // cree une fenetre nommee h de taille 400x400

    g2_line(h, 20,20, 380,380);

    g2_pen(h, 3);
    g2_circle(h, 200,200, 150);

    g2_pen(h, 25);
    g2_filled_rectangle(h, 0,0, 200,100);

    g2_pen(h, 19);
    g2_filled_circle(h, 300,300, 150);

return 0;
}

*/
