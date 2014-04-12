#ifndef listeH_
#define listeH_

#include "utils.h"

typedef struct ElementListeArc
{
    int numeroArc;
    struct ElementListeArc* psuivant;
}ElementListeArc;

typedef struct ListeArc
{
	ElementListeArc* pdebut;
	ElementListeArc* pfin;
}ListeArc;

/* Creation */
ElementListeArc* consElementListeArc(int numeroArc);
ListeArc consListeVide();

/* Affichage */
void afficherListeArc(ListeArc liste);

/* Ajout */
ListeArc ajoutListeFin(ListeArc liste, int numeroArc);

/* Utilitaires */
void supprimerListe(ListeArc* liste);
bool estVideListe(ListeArc liste);
ListeArc copieListeArc(ListeArc liste);


#endif
