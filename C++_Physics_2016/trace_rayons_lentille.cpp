#include <iostream>
#include <string>
#include <cmath>
#include <fstream>

using namespace std;

int main(void) {
    ofstream fichier1("lentille.res");
    int R=1;
    double f, i, t, d, delta;
    double n=1.5;   // indice de la lentille
    d=0;
    for (d=0; d<=R/n; d=d+0.01) {
        t = asin(n*d/R);
        i = asin(d/R);
         delta = t - i;
         f = R*cos(i) + d/tan(t-i);

         fichier1<<d<<" "<<i<<" "<<delta<<" "<<f<<endl;
    }
    fichier1.close();

    return 0;
}

// Les conditions de Gauss sont bien vérifiées pour d, i ou delta très petits.