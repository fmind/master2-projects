#include "utils.h"


void purger()
{
    int c;

    while ((c = getchar()) != '\n' && c != EOF)
    {}
}

void clean (char *buffer)
{
    char *p = strchr(buffer, '\n');

    if (p)
    {
        *p = 0;
    }

    else
    {
        purger();
    }
}

int secure_INT()
{
    char chaine[MAX_LENGHT];
    int nombre;
    bool ret;
    do
    {
        fgets(chaine, MAX_LENGHT, stdin);
        clean(chaine);
        ret = sscanf(chaine, "%d", &nombre);

        if(ret != 1)
        {
            printf("\nCe n'est pas un entier\n");
        }
    } while (ret != 1);
    return nombre;
}

int secure_INTMin(int min)
{
    char chaine[MAX_LENGHT];
    int nombre;
    bool ret;

    do
    {
        fgets(chaine, MAX_LENGHT, stdin);
        clean(chaine);
        ret = sscanf(chaine, "%d", &nombre);

        if(nombre < min)
        {
            printf("\nL'entier doit etre superieur a %d: ", min);
        }

        if(ret != 1)
        {
            printf("\nCe n'est pas un entier valide: ");
        }
    } while ((ret != 1) || (nombre < min));
    return nombre;
}

int secure_INTMax(int max)
{
    char chaine[MAX_LENGHT];
    int nombre;
    bool ret;

    do
    {
        fgets(chaine, MAX_LENGHT, stdin);
        clean(chaine);
        ret = sscanf(chaine, "%d", &nombre);

        if(nombre > max)
        {
            printf("\nL'entier doit etre inferieur ou egal a %d: ", max);
        }

        if(ret != 1)
        {
            printf("\nCe n'est pas un entier valide: ");
        }
    } while ((ret != 1) || (nombre > max));
    return nombre;
}

int secure_INTMinMax(int min, int max)
{
    char chaine[MAX_LENGHT];
    int nombre;
    bool ret;

    do
    {
        fgets(chaine, MAX_LENGHT, stdin);
        clean(chaine);
        ret = sscanf(chaine, "%d", &nombre);

        if(nombre < min)
        {
            printf("\nL'entier doit etre superieur a %d: ", min);
        }

        if(nombre > max)
        {
            printf("\nL'entier doit etre inferieur ou egal a %d: ", max);
        }

        if(ret != 1)
        {
            printf("\nCe n'est pas un entier valide: ");
        }

    } while ((ret != 1) || (nombre < min) || (nombre > max));
    return nombre;
}

int random_number(int a, int b)
{
    b++;
    return rand()%(b-a) +a;
}
