#include<stdio.h>
#include<stdlib.h>


#define foreach(a, b, c) for (int a = b; a < c; a++)
#define for_i foreach(i, 0, n)
#define for_j foreach(j, 0, n)
#define for_ij for_i for_j

int multiply(int num1, int num2)
{
    return num1 * num2;
}

int trace(int **a, int n)
{
    for_i{
        for_j printf("%d ", a[i][j]);
        printf("\n");
    }
    int trace=0;
    for_i trace+=a[i][i];
    return trace;
}

int main()
{
    int **m;
    int n=4;
    m=malloc(sizeof(int *)*n);
    m[0]=malloc(sizeof(int)*n*n);
    for_i m[i]=m[0]+n*i;
    for_ij m[i][j]=i+j;
    printf("%d", trace(m,n));
    return 0;
}
