#include "genetique.h"

/* Construction */
Alele consAleleVide()
{
    Alele nouvelleAlele;
    nouvelleAlele.mesure = consMesureVide();
    nouvelleAlele.numeroArc = -1;
    nouvelleAlele.actif = false;

    return nouvelleAlele;
}

Individu consIndividuVide()
{
    Individu nouvelIndividu;
    nouvelIndividu.genome = NULL;
    nouvelIndividu.id = -1;
    nouvelIndividu.nbAlele = -1;
    nouvelIndividu.score = -1;
    nouvelIndividu.lenght = -1;
    nouvelIndividu.budget = -1;

    return nouvelIndividu;
}

ListePopulation consListePopulationvide()
{
    ListePopulation nouvelleListe;
    nouvelleListe.pdebut = NULL;
    nouvelleListe.pfin = NULL;

    return nouvelleListe;
}

Population consPopulationVide()
{
    Population nouvellePopulation;
    nouvellePopulation.taillePopulation = 0;
    nouvellePopulation.listePopulation = consListePopulationvide();

    return nouvellePopulation;
}

ElementListePopulation* consElementListePopulation(Individu individu)
{
    ElementListePopulation* nouvelElement = (ElementListePopulation*)malloc(sizeof(ElementListePopulation));
    if(nouvelElement == NULL)
    {
        perror("Allocation du maillon de chaine(consElementListePopulation) impossible");
        exit(-1);
    }
    nouvelElement->individu = individu;
    nouvelElement->psuivant = NULL;

    return nouvelElement;
}

ListePopulation ajoutListePopulationFin(ListePopulation liste, Individu individu)
{
    if(estVideListePopulation(liste))
    {
        liste.pfin = consElementListePopulation(individu);
        liste.pdebut = liste.pfin;
    }
    else
    {
        liste.pfin->psuivant = consElementListePopulation(individu);
        liste.pfin = liste.pfin->psuivant;
    }

    return liste;
}

Individu genererIndividu(int id, Mesures mesures, Graphe graphe)
{
    int i, j;
    ElementListeArc* temp;
    Alele alele = consAleleVide();
    Individu nouvelIndividu = consIndividuVide();
    nouvelIndividu.id = id;
    nouvelIndividu.nbAlele = mesures.nbMesuresTotales;
    nouvelIndividu.genome = (Alele*)malloc(mesures.nbMesuresTotales*(sizeof(Alele)));
    if(nouvelIndividu.genome == NULL)
    {
        perror("Allocation du genome(genererIndividu) impossible");
        exit(-1);
    }

    for(i = 0; i < nouvelIndividu.nbAlele; i++)
    {
        nouvelIndividu.genome[i] = consAleleVide();
    }

    j = 0;
    for(i = 0; i < mesures.nbMesure; i++)
    {
        temp = mesures.tabMesure[i].arcApplicables.pdebut;
        while(temp != NULL)
        {
            alele.mesure = mesures.tabMesure[i];
            alele.numeroArc = temp->numeroArc;
            alele.actif = rand()%2;
            nouvelIndividu.genome[j] = alele;
            temp = temp->psuivant;
            j++;
        }
    }
    nouvelIndividu.score = -1;
    nouvelIndividu.lenght = -1;
    nouvelIndividu.budget = -1;

    return nouvelIndividu;
}

Individu consIndividuFonctionnel(int nbAlele)
{
    int i;
    Individu individu = consIndividuVide();
    individu.genome = (Alele*)malloc(nbAlele*(sizeof(Alele)));
    individu.nbAlele = nbAlele;
    if(individu.genome == NULL)
    {
        perror("Allocation du genome(ConsIndividuFonctionnel) impossible");
        exit(-1);
    }
    for(i = 0; i < individu.nbAlele; i++)
    {
        individu.genome[i] = consAleleVide();
    }
    individu.score = -1;
    individu.lenght = -1;

    return individu;
}


/* Utilitaires */
void supprimerIndividu(Individu* individu)
{
    if(individu->genome != NULL)
    {
        free(individu->genome);
        individu->genome = NULL;
    }
    individu->id = -1;
    individu->nbAlele = -1;
    individu->score = -1;
    individu->genome = NULL;
}


/* Affichage */
void afficherIndividu(Individu individu)
{
    int i;
    printf("id de l'individu: %d\n", individu.id);
    printf("Nombre d'alele: %d\n\n", individu.nbAlele);
    printf("Score de l'individu: %f\n", individu.score);
    printf("Lenght de l'individu: %f\n", individu.lenght);
    printf("cout de l'individu: %f\n\n", individu.budget);

    for(i = 0; i < individu.nbAlele; i++)
    {
        printf("Alele numero: %d\n", i);
        afficherAlele(individu.genome[i]);
        printf("\n\n");
    }
}

void afficherAlele(Alele alele)
{
    afficherMesure(alele.mesure);
    printf("Numero arc %d  |%d", alele.numeroArc, alele.actif);
}

void afficherListePopulation(ListePopulation liste)
{
    if(estVideListePopulation(liste))
    {
        printf("Liste vide");
    }
    else
    {
        ElementListePopulation* temp = liste.pdebut;
        while(temp != NULL)
        {
            afficherIndividu(temp->individu);
            printf("\n------------------------------------------------------\n");
            temp = temp -> psuivant;
        }
    }
}

void afficherPopulation(Population population)
{
    printf("Taille de la population: %d\n",population.taillePopulation);
    afficherListePopulation(population.listePopulation);
}


void afficherIndividuFinal(Individu individu)
{
    int i;
    ElementListeArc* tempEffi = NULL;
    ElementListeArc* tempArc = NULL;
    printf("\n\nid de l'individu: %d\n", individu.id);
    printf("Nombre d'alele: %d\n\n", individu.nbAlele);
    printf("Score de l'individu: %f\n", individu.score);
    printf("Lenght de l'individu: %f\n", individu.lenght);
    printf("cout de l'individu: %f\n\n", individu.budget);
    printf("\nMesures finales a faire:\n");

    for(i = 0; i < individu.nbAlele; i++)
    {
        if(individu.genome[i].actif)
        {
            tempEffi = individu.genome[i].mesure.efficacite.pdebut;
            tempArc = individu.genome[i].mesure.arcApplicables.pdebut;
            while(tempArc->numeroArc != individu.genome[i].numeroArc)
            {
                tempArc = tempArc->psuivant;
                tempEffi = tempEffi->psuivant;
            }
            printf("Appliquer mesure %d sur arc %d\n", individu.genome[i].mesure.id, individu.genome[i].numeroArc);
        }
    }
}

/* Utilitaires */
bool estVideListePopulation(ListePopulation liste)
{
    return liste.pdebut == NULL;
}

void supprimerListePopulation(ListePopulation* liste)
{
    ElementListePopulation* temp = liste->pdebut;

    if(!estVideListePopulation(*liste))
    {
        while(liste->pdebut != NULL)
        {
            temp = liste->pdebut;
            supprimerIndividu(&temp->individu);
            liste->pdebut = liste->pdebut->psuivant;
            free(temp);
        }
    }

    liste->pdebut = liste->pfin = NULL;
}

void supprimerPopulation(Population* population)
{
    if(!estVideListePopulation(population->listePopulation))
    {
        supprimerListePopulation(&(population->listePopulation));
    }
    population->taillePopulation = 0;
}

Individu dupliquerIndividu(Individu individu)
{
    Individu clone;
    int i;
    clone = individu;
    clone.genome = (Alele*)malloc(individu.nbAlele*(sizeof(Alele)));
    if(clone.genome == NULL)
    {
        perror("Clone impossible (dupliquerIndividu)");
        exit(-1);
    }
    for(i = 0; i < individu.nbAlele; i++)
    {
        clone.genome[i] = individu.genome[i];
    }
    return clone;
}


/* Genetique */
Population croisements(Population population, float crossesRate, int idBegin)
{
    int i, j, k;
    int cross_rate = (int)(ceil(population.taillePopulation*crossesRate/2));
    Individu fils = consIndividuVide();
    Individu fille = consIndividuVide();
    int pere = -1;
    int mere = -1;
    int nbAllele = -1;
    ListeArc listeTempTransformation = consListeVide();
    ListeArc listeTempTransformation2 = consListeVide();
    ElementListeArc* suppression1 = NULL;
    ElementListeArc* position1 = NULL;
    ElementListeArc* suppression2 = NULL;
    ElementListeArc* position2 = NULL;
    ElementListePopulation* pPere = NULL;
    ElementListePopulation* pMere = NULL;
    int cpt = -1;
    int random1, random2;
    random1 = random2 = -1;

    if(population.taillePopulation < 2)
    {
        perror("La population doit avoir au moins deux individus(croisements)");
        exit(-1);
    }

    nbAllele = population.listePopulation.pdebut->individu.nbAlele;

    for(i = 0; i < cross_rate; i++)
    {
        pere = random_number(0,population.taillePopulation - 1);
        //on vérifique que le pere et la mere sont pas les memes
        do
        {
            mere = random_number(0,population.taillePopulation - 1);
        }while(pere == mere);

        //On vas chercher pere et mère dans la liste de la population
        pPere = population.listePopulation.pdebut;
        for(j = 0; j < pere; j++)
        {
            pPere = pPere->psuivant;
        }

        pMere = population.listePopulation.pdebut;
        for(j = 0; j < mere; j++)
        {
            pMere = pMere->psuivant;
        }

        //creation du fils et de la fille
        //On passe par une liste d'entier pour l'aléatoire pour éviter de tourner en rond trop longtemps
        //partie temporaire des listes
        for(j = 0; j < nbAllele; j++)
        {
            listeTempTransformation = ajoutListeFin(listeTempTransformation, j);
            listeTempTransformation2 = ajoutListeFin(listeTempTransformation2, j);
        }

        //on met a zero les compteurs pour les fils
        cpt = 0;

        //On construit les enfants
        fils = consIndividuFonctionnel(nbAllele);
        fille = consIndividuFonctionnel(nbAllele);

        fils.id = idBegin;
        idBegin++;
        fille.id = idBegin;
        idBegin++;

        //on croise toutes les alleles
        for(k = 0; k < nbAllele; k++)
        {
            //on tire au hasard le numero de la liste
            random1 = random_number(0,nbAllele - cpt - 1);
            random2 = random_number(0,nbAllele - cpt - 1);

            //on s'y rend en ayant la position precedente pour supprimer le maillon
            position1 = suppression1 = listeTempTransformation.pdebut;
            for(j = 0; j < random1; j++)
            {
                suppression1 = position1;
                position1 = position1 ->psuivant;
            }

            position2 = suppression2 = listeTempTransformation2.pdebut;
            for(j = 0; j < random2; j++)
            {
                suppression2 = position2;
                position2 = position2->psuivant;
            }

            if(k%2 == 0)
            {
                //on croise
                fils.genome[cpt] = pPere->individu.genome[position1->numeroArc];

                fille.genome[cpt] = pMere->individu.genome[position2->numeroArc];
            }
            else
            {
                //on croise
                fils.genome[cpt] = pMere->individu.genome[position1->numeroArc];

                fille.genome[cpt] = pPere->individu.genome[position2->numeroArc];
            }
            cpt++;

            //On supprime les maillons
            if(position1 == listeTempTransformation.pdebut)
            {
                listeTempTransformation.pdebut = listeTempTransformation.pdebut->psuivant;
            }
            else
            {
                suppression1->psuivant = position1->psuivant;
            }
            free(position1);
            position1 = suppression1 = NULL;

            if(position2 == listeTempTransformation2.pdebut)
            {
                listeTempTransformation2.pdebut = listeTempTransformation2.pdebut->psuivant;
            }
            else
            {
                suppression2->psuivant = position2->psuivant;
            }
            free(position2);
            position2 = suppression2 = NULL;
        }
        supprimerListe(&listeTempTransformation);
        supprimerListe(&listeTempTransformation2);

        //ajout a la population
        population.listePopulation = ajoutListePopulationFin(population.listePopulation,fils);
        population.taillePopulation++;
        population.listePopulation = ajoutListePopulationFin(population.listePopulation,fille);
        population.taillePopulation++;
    }
    return population;
}

Population mutations(Population population, float mutationRate)
{
    int i, j, k, n, m, random;
    Individu* aMuter = NULL;
    int nbAllele = -1;
    ListeArc listeTempIndividu = consListeVide();
    ListeArc listeTempAlelle = consListeVide();
    ElementListeArc* positionIndividu = NULL;
    ElementListeArc* positionAllele = NULL;
    ElementListeArc* supprimerIndividu = NULL;
    ElementListeArc* supprimerAllele = NULL;
    ElementListePopulation* pIndividu = NULL;

    if(population.taillePopulation < 1)
    {
        perror("La population doit avoir au moins un element(mutation)");
        exit(-1);
    }

    //On recupere le nombre d'alleles
    nbAllele = population.listePopulation.pdebut->individu.nbAlele;

    //Calcul des taux de mutations
    n = (int)(ceil(population.taillePopulation*mutationRate));
    m = (int)(ceil(population.listePopulation.pdebut->individu.nbAlele*mutationRate));

    //On initialise la liste temporaire des individus (pour eviter les doublons)
    for(i = 0; i < population.taillePopulation; i++)
    {
        listeTempIndividu = ajoutListeFin(listeTempIndividu, i);
    }

    //Boucle qui choisi les individu au hasard sans doublons
    for(i = 0; i < n; i++)
    {
        //On recuperer l'individu
        random = random_number(0, population.taillePopulation - i - 1);
        pIndividu = population.listePopulation.pdebut;
        positionIndividu = supprimerIndividu = listeTempIndividu.pdebut;
        for(j = 0; j < random; j++)
        {
            supprimerIndividu = positionIndividu;
            positionIndividu = positionIndividu->psuivant;
            pIndividu = pIndividu->psuivant;
        }

        //On lui assigne son pointeur
        aMuter = &pIndividu->individu;

        //On initialise la liste sans doublon pour les alleles
        for(j = 0; j < nbAllele; j++)
        {
            listeTempAlelle = ajoutListeFin(listeTempAlelle, j);
        }

        for(j = 0; j < m; j++)
        {
            random = random_number(0, nbAllele - 1 - j);
            positionAllele = supprimerAllele = listeTempAlelle.pdebut;
            for(k = 0; k < random; k++)
            {
                supprimerAllele = positionAllele;
                positionAllele = positionAllele->psuivant;
            }

            //On inverse le gene
            aMuter->genome[positionAllele->numeroArc].actif = !aMuter->genome[positionAllele->numeroArc].actif;

            //On supprime le maillon

            if(positionAllele == listeTempAlelle.pdebut)
            {
                listeTempAlelle.pdebut = listeTempAlelle.pdebut->psuivant;
            }
            else
            {
                supprimerAllele->psuivant = positionAllele->psuivant;
            }
            free(positionAllele);
            positionAllele = supprimerAllele = NULL;
        }
        supprimerListe(&listeTempAlelle);

        //On supprime le maillon
        if(positionIndividu == listeTempIndividu.pdebut)
        {
            listeTempIndividu.pdebut = listeTempIndividu.pdebut->psuivant;
        }
        else
        {
            supprimerIndividu->psuivant = positionIndividu->psuivant;
        }
        free(positionIndividu);
        positionIndividu = supprimerIndividu = NULL;
    }
    supprimerListe(&listeTempIndividu);
    return population;
}

Graphe appliquerIndividu(Individu individu, Graphe graphe)
{
    int i;
    ElementListeArc* tempEffi = NULL;
    ElementListeArc* tempArc = NULL;
    int numArcApplicable;
    for(i = 0; i < individu.nbAlele; i++)
    {
        if(individu.genome[i].actif)
        {
            numArcApplicable = individu.genome[i].numeroArc;
            tempEffi = individu.genome[i].mesure.efficacite.pdebut;
            tempArc = individu.genome[i].mesure.arcApplicables.pdebut;
            while(numArcApplicable != tempArc->numeroArc)
            {
                tempArc = tempArc->psuivant;
                tempEffi = tempEffi->psuivant;
            }
            graphe.tabArcs[individu.genome[i].numeroArc].ponderation += tempEffi->numeroArc;
            graphe.tabArcs[individu.genome[i].numeroArc].cout += individu.genome[i].mesure.cout;
        }
    }
    return graphe;
}
Graphe retirerIndividu(Individu individu, Graphe graphe)
{
    int i;
    ElementListeArc* tempEffi = NULL;
    ElementListeArc* tempArc = NULL;
    int numArcApplicable;
    for(i = 0; i < individu.nbAlele; i++)
    {
        if(individu.genome[i].actif)
        {
            numArcApplicable = individu.genome[i].numeroArc;
            tempEffi = individu.genome[i].mesure.efficacite.pdebut;
            tempArc = individu.genome[i].mesure.arcApplicables.pdebut;
            while(numArcApplicable != tempArc->numeroArc)
            {
                tempArc = tempArc->psuivant;
                tempEffi = tempEffi->psuivant;
            }
            graphe.tabArcs[individu.genome[i].numeroArc].ponderation -= tempEffi->numeroArc;
            graphe.tabArcs[individu.genome[i].numeroArc].cout -= individu.genome[i].mesure.cout;
        }
    }
    return graphe;
}

float score(GeneticSolver geneticSolver, Individu individu)
{
    return geneticSolver.ratioPriority * individu.lenght + (1 - geneticSolver.ratioPriority) * (100 - individu.budget / geneticSolver.targetBudget * 100);
}

Individu majIndividu(GeneticSolver geneticSolver, Individu individu)
{
    int i, somme;
    if(individu.genome != NULL)
    {
        somme = 0;
        for(i = 0; i < individu.nbAlele; i++)
        {
            somme += individu.genome[i].actif * individu.genome[i].mesure.cout;
        }
        individu.budget = somme;
    }
    individu.score = score(geneticSolver, individu);
    return individu;
}

Population selection(Population population, int n)
{
    ElementListePopulation* tabTemp[population.taillePopulation];
    bool tabMarq[population.taillePopulation];
    ElementListePopulation* temp = population.listePopulation.pdebut;
    ListePopulation nouvellePopulation = consListePopulationvide();
    int i = 0;
    int j;
    float scoreMax;
    int max;
    while(temp != NULL)
    {
        tabTemp[i] = temp;
        tabMarq[i] = false;
        temp = temp->psuivant;
        i++;
    }
    //On détache la liste de la population
    population.listePopulation = consListePopulationvide();
    population.taillePopulation = n;
    for(i = 0; i < n; i++)
    {
        scoreMax  = -1;
        max = 0;
        for(j = 0; j < population.taillePopulation; j++)
        {
            if(tabTemp[j]->individu.score > scoreMax && tabMarq[j] == false)
            {
                max = j;
                scoreMax = tabTemp[j]->individu.score;
            }
        }
        tabMarq[max] = true;
        nouvellePopulation = ajoutListePopulationFin(nouvellePopulation, tabTemp[max]->individu);
    }

    for(i = 0; i < n; i++)
    {
        if(tabMarq[i] == false)
        {
            supprimerIndividu(&tabTemp[i]->individu);
            free(tabTemp[i]);
        }
    }
    population.listePopulation = nouvellePopulation;
    return population;
}

Individu selectionONE(Population population)
{
    ElementListePopulation* temp = population.listePopulation.pdebut;
    Individu garde = temp->individu;
    while(temp != NULL)
    {
        if(temp->individu.score > garde.score)
        {
            garde = temp->individu;
        }
        temp = temp->psuivant;
    }

    return garde;
}
