#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

// Given matrix
int matrix1 [4][5] = {
    {1, 2, 3, 4 , 5},
    {6, 7, 8, 9, 10},
    {11, 12, 13, 14, 15},
    {16, 17, 18, 19, 20}
};

int matrix2 [5][2] = {
    {1, 2},
    {3, 4},
    {5, 6},
    {7, 8},
    {9, 10}
};

#define m1Row  (sizeof(matrix1) / sizeof(matrix1[0]))
#define m1Col  (sizeof(matrix1[0]) / sizeof(matrix1[0][0]))
#define m2Row  (sizeof(matrix2) / sizeof(matrix2[0]))
#define m2Col  (sizeof(matrix2[0]) / sizeof(matrix2[0][0]))

// result of m1 * m2
int resultMatrix[m1Row][m2Col];

void printMatrix() {
    int i, j;
    for(i = 0; i < m1Row; i++) {
        for(j = 0; j < m2Col; j++)
            printf("%d ", resultMatrix[i][j]);
        
        printf("\n");
    }
}

void *threading_task(void* coord) {
    int row = ((int*)coord)[0];
    int col = ((int*)coord)[1];
    int i;

    resultMatrix[row][col] = 0;
    for(i = 0; i < m1Col; i++) {
        resultMatrix[row][col] += matrix1[row][i]*matrix2[i][col];
    }
    pthread_exit(0);
}

int main(int argc, const char * argv[]) {
    // Validate input matrix
    if(m1Col != m2Row) {
        printf("Invalid input matrix\n");
        return 0;
    }
 
    // Creating threads
    pthread_t threads[m1Row * m2Col];
    int threadCount = 0;
    int **coords = (int**) malloc(sizeof(int*) * m1Row * m2Col);
    int i, j, k;
    
    for(i = 0; i < m1Row; i++) {
        for (j = 0; j < m2Col; j++) {
            coords[threadCount] = (int*) malloc(sizeof(int)*2);
            coords[threadCount][0] = i;
            coords[threadCount][1] = j;
            pthread_create(&threads[threadCount], NULL, threading_task, (void*)coords[threadCount]);
            threadCount++;
        }
    }

    for(k = 0; k < m1Row * m2Col; k++) {
        pthread_join(threads[k], NULL);
    }
    
    for(k = 0; k < m1Row * m2Col; k++) {
        free(coords[threadCount]);
    }
    free(coords);
    
    printMatrix();
    
    printf("Done\n");
    
    return 0;
}





