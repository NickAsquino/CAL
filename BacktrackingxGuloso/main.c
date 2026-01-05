#include <stdio.h>
#include <stdlib.h>

#define N 25

int graph[N][N];
int color[N];

int isSafe(int v, int c) {
    for (int i = 0; i < N; i++) {
        if (graph[v][i] && color[i] == c) {
            return 0;
        }
    }
    return 1;
}

int graphColoringBT(int v, int m) {
    if (v == N) return 1;

    for (int i = 1; i <= m; i++) {
        if (isSafe(v, i)) {
            color[v] = i;
            if (graphColoringBT(v + 1, m)) return 1;
            color[v] = 0;
        }
    }
    return 0;
}

void solveBacktracking() {
    int m = 1;
    while (1) {
        for (int i = 0; i < N; i++) color[i] = 0;
        if (graphColoringBT(0, m)) {
            printf("\n[Backtracking] Minimo de cores usadas: %d\n", m);
            for (int i = 0; i < N; i++) {
                printf("Vertice %d -> Cor %d\n", i, color[i]);
            }
            break;
        }
        m++;
    }
}

void guloso() {
    for (int i = 0; i < N; i++) {
        color[i] = -1;
    } 
    color[0] = 0;

    int available[N];
    for (int k = 1; k < N; k++) {
        for (int i = 0; i < N; i++) {
            available[i] = 1;
        } 

        for (int i = 0; i < N; i++) {
            if (graph[k][i] && color[i] != -1) {
                available[color[i]] = 0;
            }
        }

        int menorCor = 0;
        while(!available[menorCor] && menorCor < N) {
            menorCor++;
        }

        color[k] = menorCor;
    }

    int maxColor = 0;
    for (int i = 0; i < N; i++) {
        if (color[i] > maxColor) maxColor = color[i];
    }

    printf("\n[Guloso] Numero de cores usadas: %d\n", maxColor + 1);
    for (int i = 0; i < N; i++) {
        printf("Vertice %d -> Cor %d\n", i, color[i] + 1);
    }
}

void imprimeCores(char* filename) {
    FILE *fp = fopen(filename, "w");
        for(int i = 0; i < N; i++) {
            fprintf(fp, "%d\n", color[i]);
        }
    fclose(fp);
}

void loadCSV(const char* filename) {
    FILE *fp = fopen(filename, "r");
    if (!fp) {
        printf("Erro ao abrir o arquivo!\n");
        exit(1);
    }

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            fscanf(fp, "%d,", &graph[i][j]);
        }
    }
    fclose(fp);
}

int main() {
    loadCSV("grafo_25nos.csv");

    solveBacktracking();
    imprimeCores("coresbk.txt");

    guloso();
    imprimeCores("coresguloso.txt");

    return 0;
}
