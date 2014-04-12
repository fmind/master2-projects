#include "liste.h"
#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>

/*Construction*/
ElementListeArc* consElementListeArc(int numeroArc)
{
    ElementListeArc* nouvelElement = (ElementListeArc*)malloc(sizeof(ElementListeArc));
    if(nouvelElement == NULL)
    {
        perror("Allocation du maillon de chaine(consElementListeArc) impossible");
        exit(-1);
    }

    nouvelElement->numeroArc = numeroArc;
    nouvelElement->psuivant = NULL;
    return nouvelElement;
}

ListeArc consListeVide()
{
    ListeArc nouvelleListe;
	nouvelleListe.pdebut = NULL;
	nouvelleListe.pfin = NULL;
	return nouvelleListe;
}

/*Ajout*/
ListeArc ajoutListeFin(ListeArc liste, int numeroArc)
{
    if(estVideListe(liste))
    {
        liste.pfin = consElementListeArc(numeroArc);
        liste.pdebut = liste.pfin;
    }
    else
    {
        liste.pfin->psuivant = consElementListeArc(numeroArc);
        liste.pfin = liste.pfin->psuivant;
    }

    return liste;
}


/*Affichage*/
void afficherListeArc(ListeArc liste)
{
    ElementListeArc* temp = liste.pdebut;

    if(estVideListe(liste))
    {
        printf("Liste vide");
    }

    while(temp != NULL)
    {
        printf("-> %d ", temp->numeroArc);
        temp = temp -> psuivant;
    }
}

/*Utilitaires*/
bool estVideListe(ListeArc liste)
{
    return liste.pdebut == NULL;
}

void supprimerListe(ListeArc* liste)
{
    ElementListeArc* temp;

    if(!estVideListe(*liste))
    {
        while(liste->pdebut != NULL)
        {
            temp = liste->pdebut;
            liste->pdebut = liste->pdebut->psuivant;
            free(temp);
        }
    }
    liste->pdebut = liste->pfin = NULL;
}

ListeArc copieListeArc(ListeArc liste)
{
    ListeArc copie = consListeVide();
    ElementListeArc* temp = liste.pdebut;
    ElementListeArc* tempcopie = liste.pdebut;
    if(estVideListe(liste))
    {
        return copie;
    }
    else
    {
        copie.pdebut = copie.pfin = consElementListeArc(temp->numeroArc);
        temp = temp->psuivant;
        while(temp != NULL)
        {
            tempcopie = consElementListeArc(temp->numeroArc);
            copie.pfin->psuivant = tempcopie;
            copie.pfin = tempcopie;
            temp = temp->psuivant;
        }
    }
    return copie;
}
