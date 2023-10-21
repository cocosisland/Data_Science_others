/* THERMODYNAMIQUE
Le but est de modeliser les transitions de phase (i.e. changements d'etat : fusion, changement de structure de la matiere).
L'un des modeles les plus importants de transitions de phase est celui de Landau dans lequel l'energie d'un systeme est exprimee comme
un polynome. Un modele mecanique avec une bille se deplacant dans un tube en verre recourbe vers le bas et de rayon de courbure l
vise a produire un comportement similaire dans un systeme plus simple.
Nous implementons ici la methode de Newton, qui est plus simple, celle de Landau se trouvant sur transitions_de_phase_methode_Landau.cpp.
*/

#include <iostream>
#include <string>
#include <fstream>
#include <cmath>