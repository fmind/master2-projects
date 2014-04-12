#include "mesure.h"

/* Creation */
Mesures consMesuresVide()
{
    Mesures nouvelleMesures;
    nouvelleMesures.tabMesure = NULL;
    nouvelleMesures.nbMesure = 0;
    nouvelleMesures.nbMesuresTotales = 0;

    return nouvelleMesures;
}

Mesure consMesureVide()
{
    Mesure nouvelleMesure;
    nouvelleMesure.cout = -1;
    nouvelleMesure.id = -1;
    nouvelleMesure.arcApplicables = consListeVide();
    nouvelleMesure.efficacite = consListeVide();

    return nouvelleMesure;
}

/* Construction */
Mesure consMesureManuel(int nbArc, int id)
{
    Mesure nouvelleMesure = consMesureVide();
    ElementListeArc* temp = NULL;
    nouvelleMesure.id = id;
    int i, cptArc, efficacite;
    bool same;

    //Cout
    printf("\nVeuiller saisir le cout de la mesure n°%d: ", id);
    nouvelleMesure.cout = secure_INTMin(0);

    //Nombre d'arc applicables
    printf("\nVeuillez saisir le nombre d'arcs (0-%d) sur lesquels la mesure s'applique (-1 = partout): ", nbArc);
    cptArc = secure_INTMinMax(-1, nbArc);

    //L'efficacite est la meme?
    printf("\nL'efficacite de la mesure est partout la meme ? (0 non, 1 oui): ");
    same = secure_INTMinMax(0,1);

    //Si la meme efficacite
    if(same)
    {
        printf("\nDonner l'efficacite de la mesure: ");
        efficacite = secure_INTMin(0);
    }

    //Si utilisateur sais pas lire
    if(cptArc == nbArc)
    {
        cptArc = -1;
    }

    //Si pas tous les arcs
    if(cptArc != -1)
    {
        for(i = 0; i < cptArc; i++)
        {
            printf("\nDonner le numero du %de arc sur lequel la mesure s'applique: ", i + 1);
            nouvelleMesure.arcApplicables = ajoutListeFin(nouvelleMesure.arcApplicables, secure_INTMinMax(0,nbArc));
        }

        if(!same)
        {
            temp = nouvelleMesure.arcApplicables.pdebut;
            for(i = 0; i < cptArc; i++)
            {
                printf("\nDonner l'efficacite de la mesure pour l'arc %d: ", temp->numeroArc);
                nouvelleMesure.efficacite = ajoutListeFin(nouvelleMesure.efficacite, secure_INTMin(0));
                temp = temp->psuivant;
            }
        }
        else
        {
            for(i = 0; i < cptArc; i++)
            {
                nouvelleMesure.efficacite = ajoutListeFin(nouvelleMesure.efficacite, efficacite);
            }
        }
    }

    //Si tout les arcs
    if(cptArc == -1)
    {
        for(i = 0; i < nbArc; i++)
        {
            nouvelleMesure.arcApplicables = ajoutListeFin(nouvelleMesure.arcApplicables,i);
        }

        if(!same)
        {
            temp = nouvelleMesure.arcApplicables.pdebut;
            for(i = 0; i < nbArc; i++)
            {
                printf("\nDonner l'efficacite de la mesure pour l'arc %d: ", temp->numeroArc);
                nouvelleMesure.efficacite = ajoutListeFin(nouvelleMesure.efficacite, secure_INTMin(0));
                temp = temp->psuivant;
            }
        }
        else
        {
            for(i = 0; i < nbArc; i++)
            {
                nouvelleMesure.efficacite = ajoutListeFin(nouvelleMesure.efficacite, efficacite);
            }
        }
    }
    return nouvelleMesure;
}

Mesures consMesuresManuel(int nbArc)
{
    int i;
    Mesures nouvelleMesures = consMesuresVide();
    ElementListeArc* temp = NULL;
    printf("Saisir le nombre de mesures : ");
    nouvelleMesures.nbMesure = secure_INTMin(0);
    nouvelleMesures.tabMesure = (Mesure*)malloc(nouvelleMesures.nbMesure*(sizeof(Mesure)));
    if(nouvelleMesures.tabMesure == NULL)
    {
        perror("Erreur d'allocation de mesures(consMesuresManuel)");
        exit(-1);
    }
    for(i = 0; i < nouvelleMesures.nbMesure; i++)
    {
        nouvelleMesures.tabMesure[i] = consMesureManuel(nbArc,i);
    }
    nouvelleMesures.nbMesuresTotales = 0;
    for(i = 0; i < nouvelleMesures.nbMesure; i++)
    {
        temp = nouvelleMesures.tabMesure[i].arcApplicables.pdebut;
        while(temp != NULL)
        {
            nouvelleMesures.nbMesuresTotales ++;
            temp = temp->psuivant;
        }
    }

    return nouvelleMesures;
}

/* Affichage */
void afficherMesure(Mesure mesure)
{
    printf("Mesure numero: %d, cout: %d",mesure.id, mesure.cout);
    printf("\nListe arc applicables:");
    afficherListeArc(mesure.arcApplicables);
    printf("\nListe efficacite:");
    afficherListeArc(mesure.efficacite);
    printf("\n");
}

void afficherMesures(Mesures mesures)
{
    int i;

    if(mesures.nbMesure == 0)
    {
        printf("Aucune mesure\n");
    }
    else
    {
        for(i = 0; i < mesures.nbMesure; i++)
        {
            afficherMesure(mesures.tabMesure[i]);
        }
    }
}

/* utilitaires*/
void supprimerMesures(Mesures* mesures)
{
    int i;
    if(mesures->tabMesure != NULL)
    {
        for(i = 0; i < mesures->nbMesure; i++)
        {
            supprimerMesure(&(mesures->tabMesure[i]));
        }
        free(mesures->tabMesure);
        mesures->tabMesure = NULL;
        mesures->nbMesure = 0;
        mesures->nbMesuresTotales = 0;
    }
}

void supprimerMesure(Mesure* mesure)
{
    mesure->cout = -1;
    mesure->id = -1;
    if(mesure->arcApplicables.pdebut != NULL)
    {
        supprimerListe(&(mesure->arcApplicables));
    }

    if(mesure->efficacite.pdebut != NULL)
    {
        supprimerListe(&(mesure->efficacite));
    }

    mesure->arcApplicables = consListeVide();
    mesure->efficacite = consListeVide();
}
