#ifndef mesureH_
#define mesureH_

#include "liste.h"

/* Structure */

typedef struct Mesure
{
    int cout;
    ListeArc efficacite;
    int id;
    ListeArc arcApplicables;
}Mesure;

typedef struct Mesures
{
    int nbMesure;
    int nbMesuresTotales;
    Mesure* tabMesure;
}Mesures;

/* Creation */
Mesures consMesuresVide();
Mesure consMesureVide();
Mesure consMesureManuel(int nbArc, int id);
Mesures consMesuresManuel(int nbArc);

/* Construction */

/* Affichage */
void afficherMesure(Mesure mesure);
void afficherMesures(Mesures mesures);

/* Utilitaires */
void supprimerMesures(Mesures *mesures);
void supprimerMesure(Mesure* mesure);


#endif
