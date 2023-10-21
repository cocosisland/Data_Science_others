


#include <iostream>
#include <string>
#include <fstream>
#include <cmath>
#define w0 1
#define tmax 100
#define v0 0
#define tau 0.5
#define gamma 0.5
#define vf 0.1

using namespace std;

// cas sans frottement et fixer v0=0 cad pas de translation, juste des oscillations

void deriv_patin(int n, double t, double y[], double dy[]) {
    dy[0] = y[1];                   // derivee de x(t)
    dy[1] = w0*w0*(v0*t-y[0]);      // derivee de x'(t)
}


double sign(double x) {
    int a;
    if (x>0) a=1;
    else if (x<0) a=-1;
    else a=0;
    return a;
}


// cas avec frottements

void frott(int n, double t, double y[], double dy[]) {
    dy[0] = y[1];
    dy[1] = w0*w0*(v0*t-y[0]) - y[1]/tau - gamma*sign(y[1])*exp(-fabs(y[1]/vf));
}


// fonction rk4 contenant l'algorithme permettant de resoudre l'equation differentielle :

void rk4(int n, double x, double y[], double dx, void deriv(int, double, double[], double[])) {
    int i;
    double ddx;
    double d1[n], d2[n], d3[n], d4[n], yp[n];

    ddx = dx/2;

    deriv(n, x, y, d1);
    for (i=0; i<n; i++) {
        yp[i] = y[i] + d1[i]*ddx;
    }
    deriv(n, x+ddx, yp, d2);

    for (i=0; i<n; i++) {
        yp[i] = y[i] + d2[i]*ddx;
    }
    deriv(n, x+ddx, yp, d3);

    for (i=0; i<n; i++) {
        yp[i] = y[i] + d3[i]*ddx;
    }
    deriv(n, x+ddx, yp, d4);

    for (i=0; i<n; i++) {
        y[i] = y[i] + dx*(d1[i] + 2*d2[i] + 2*d3[i] + d4[i]) /6;
    }
}



int main(void) {
    ofstream fi1("variance.res");
    int n=2;
    double p=-3, y[n], t;
    int N=100;
    y[0]=1;
    y[1]=0.;

    fi1<<0<<" "<<y[0]<<" "<<y[1]<<endl;     // on place les points initiaux

    for (double p=-5; p<=1; p+=0.5) {
        double dt = pow(10, p);
        int compteur=0;
        double energie;     // energie du systeme
        double sommenergie=0;
        double sommenergie2=0;
        double variance=0;
    
        for (int i=1; i<=N; i++) {          // boucle sur le temps - on appelle a chaque fois rk4
            t=i*dt;
            rk4(n, t, y, dt, deriv_patin);        // sans frottement
            //rk4(n, t, y, dt, frott);                // avec frottements

            energie = 0.5*y[0]*y[0] + 0.5*y[1]*y[1] -0.5;
            sommenergie += energie;
            sommenergie2 += energie*energie;
            compteur++;
            //cout<<t<<" "<<y[0]<<" "<<y[1]<<endl;    // t:temps , y[0]:position , y[1]:vitesse
        }

        double moyenne = sommenergie/compteur;
        double moyenne2 = sommenergie2/compteur;
        variance = moyenne2 - moyenne*moyenne;
        fi1<<p<<" "<<variance<<endl;
        cout<<p<<" "<<variance<<endl;
    }

    fi1.close();

    return 0;
}

/*
En comparant les courbes obtenues avec et sans frottements, on voit que :
- sans frottement, on obtient une sinusoide, en fonction du temps, ce qui decrit le mouvement d'un oscillateur
harmonique -> pas d'amortissement
- avec frottements, la courbe regresse exponentiellement au cours du temps, jusqu'a une valeur limite de la vitesse du patin
qui est differente de zero, donc elle ne s'arrete pas, mais qui reste constante (vitesse ~= 0.27 m/sec). */