#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int* criarVetor(int n);
void imprimirVetor(int *vetor, int n);
void liberarVetor(int *vetor);

int pesquisaBinaria(int *vetor, int n, int chave, int *comparacoesBin);
int pesquisaBinariaRecursiva(int *vetor, int inicio, int fim, int chave, int *comparacoesBin);

int pesquisaSequencial(int *vetor, int n, int chave, int *comparacoesSeq);

int main() {
    int tamanhos[] = {60, 100, 200, 300, 400, 800, 1000, 1500, 2000, 3000, 5000, 7500, 10000};
    int numTamanhos = sizeof(tamanhos)/sizeof(tamanhos[0]);
    int numChaves = 50;

    FILE *arquivo = fopen("resultados.csv", "w");
    if (!arquivo) {
        printf("Erro ao criar arquivo!\n");
        return 1;
    }

    fprintf(arquivo, "Tamanho,Binaria,Sequencial\n");

    srand(time(NULL));

    for (int t = 0; t < numTamanhos; t++) {
        int tamanho = tamanhos[t];
        int *vetor = criarVetor(tamanho);

        int somaBin = 0, somaSeq = 0;

        for (int c = 0; c < numChaves; c++) {
            int chaveIndex = rand() % tamanho;      // índice aleatório
            int chave = vetor[chaveIndex];          // chave do vetor

            int comparacoesBin = 0, comparacoesSeq = 0;

            pesquisaBinaria(vetor, tamanho, chave, &comparacoesBin);
            pesquisaSequencial(vetor, tamanho, chave, &comparacoesSeq);

            somaBin += comparacoesBin;
            somaSeq += comparacoesSeq;
        }

        double mediaBin = (double)somaBin / numChaves;
        double mediaSeq = (double)somaSeq / numChaves;

        fprintf(arquivo, "%d,%.2f,%.2f\n", tamanho, mediaBin, mediaSeq);

        liberarVetor(vetor);
    }

    fclose(arquivo);
    printf("Testes concluídos! Arquivo resultados.csv gerado.\n");
    return 0;
}

int* criarVetor(int n) {
    int *vetor = (int*) malloc(n * sizeof(int));
    if (vetor == NULL) {
        printf("Erro ao alocar memoria!\n");
        exit(1);
    }

    srand(time(NULL));

    for (int i = 0; i < n; i++) {
        if(i > 0) {
            vetor[i] = vetor[i-1] + rand() % 10;
        } else {
            vetor[i] = rand() % 10;
        }
    }

    return vetor;
}

void imprimirVetor(int *vetor, int n) {
    printf("Vetor:\n");
    for (int i = 0; i < n; i++) {
        printf("%d ", vetor[i]);
    }
    printf("\n");
}

void liberarVetor(int *vetor) {
    free(vetor);
}

int pesquisaBinaria(int *vetor, int n, int chave, int *comparacoesBin) {
    return pesquisaBinariaRecursiva(vetor, 0, n - 1, chave, comparacoesBin);
}

int pesquisaBinariaRecursiva(int *vetor, int inicio, int fim, int chave, int *comparacoesBin) {
    if (inicio > fim) return -1;

    int meio = (inicio + fim) / 2;
    (*comparacoesBin)++;

    if (vetor[meio] == chave) {
        return meio;
    } else if (vetor[meio] > chave) {
        return pesquisaBinariaRecursiva(vetor, inicio, meio - 1, chave, comparacoesBin);
    } else {
        return pesquisaBinariaRecursiva(vetor, meio + 1, fim, chave, comparacoesBin);
    }
}

int pesquisaSequencial(int *vetor, int n, int chave, int *comparacoesSeq) {
    for (int i = 0; i < n; i++) {
        (*comparacoesSeq)++;
        if (vetor[i] == chave) {
            return i;
        }
    }
    return -1;
}