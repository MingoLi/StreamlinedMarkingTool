#define _XOPEN_SOURCE       /* See feature_test_macros(7) */
#define _GNU_SOURCE

#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <crypt.h>

const int NUMTHREAD = 6;     // number of threads will be used to do the crack
const int MAXLENGTH = 20;    // max length of the password

const int A = 97;   // ascii of 'a'
const int Z = 122;  // ascii of 'z'

const int BUFFSIZE = 255; // buff size for fgets

bool signaled = false;
bool done = false;  // indicate if all hashes have been cracked
bool workDataFetched = false;
int hashCount;  // to track the number of hashes need to be cracked
int threadsAvailable;  // indicate number of available threads

pthread_mutex_t signalLock, printLock, workDataLock;
pthread_cond_t signalAvailable, crack_start, crack_complete;

// Function Declarations
char* crack_helper(char *password, char *hash, int *count);
bool same(char* pass, char* hash);
void* crack_thread_task(void* arg);
bool crack_implement(char *password);
bool same(char* password, char* hash);

// adapted from from the GNU libc manual
// https://www.gnu.org/software/libc/manual/html_node/crypt.html
bool same(char* pass, char* hash)
{
    char *result;
//    int ok;
    
    struct crypt_data data;
    data.initialized = 0;
    
    result = crypt_r(pass, hash, (struct crypt_data*)&data);
    /* Test the result. */
    return strcmp (result, hash) == 0;
}

void* crack_thread_task(void* arg) {
    char *hash;
    int count;
    char *password;
    
    while(!done) {
        // Waiting for signal
        pthread_mutex_lock(&signalLock);
        while(!signaled){
            pthread_cond_wait(&signalAvailable, &signalLock);
            if(done) {
                pthread_mutex_unlock(&signalLock);
                pthread_exit(NULL);
            }
        }
        threadsAvailable--;
        signaled = false;
        pthread_mutex_unlock(&signalLock);
        
        // Fetch data
        pthread_mutex_lock(&workDataLock);
        hash = malloc(strlen(arg) + 1);
        strcpy(hash, arg);
        workDataFetched = true;
        pthread_cond_signal(&crack_start);
        pthread_mutex_unlock(&workDataLock);
        
        // Start cracking
        count = 0;
        password = malloc((MAXLENGTH + 1) * sizeof(char));
        password = crack_helper(password, hash, &count);

        // Print result
        pthread_mutex_lock(&printLock);
        printf("%s plaintext %s took %d comparisons\n", hash, password, count);
        pthread_mutex_unlock(&printLock);
        
        free(password);
        free(hash);
        
        // Signal main thread cracking complete
        pthread_mutex_lock(&signalLock);
        hashCount--;
        threadsAvailable++;
        pthread_cond_signal(&crack_complete);
        pthread_mutex_unlock(&signalLock);
    }
    
    pthread_exit(NULL);
}

// Helper method for generating permutations
char* crack_helper(char *password, char *hash, int *count) {
    bool found = false;
    int i, j;
    
    for(i = 1; i <= MAXLENGTH && !found; i++) {
        for(j = 0; j < i; j++)
            password[j] = (char)A;
        password[i] = 0;
        do {
            if(same(password, hash)) {
                found = true;
                break;
            }
            (*count)++;
        } while (crack_implement(password));
    }
    
    return password;
}

// Recursivly generate permutations
bool crack_implement(char *password) {
    if(password[0] == 0)
        return 0;
    if(password[0] == (char)Z) {
        password[0] = (char)A;
        return crack_implement(password + sizeof(char));
    }
    password[0]++;
    return true;
}




int main(int argc, const char * argv[]) {
    int i;
    char* newLinePos;   // the index of new line character \n
    FILE *fp;
    char buff[BUFFSIZE];
    
    // Initialize variables
    pthread_t threads[NUMTHREAD];
    pthread_cond_init(&signalAvailable, NULL);
    pthread_cond_init(&crack_complete, NULL);
    pthread_cond_init(&crack_start, NULL);
    pthread_mutex_init(&signalLock, NULL);
    pthread_mutex_init(&printLock, NULL);
    pthread_mutex_init(&workDataLock, NULL);
    
    hashCount = 0;
    threadsAvailable = 0;
    
    for(i = 0; i < NUMTHREAD; i++) {
        pthread_create(&threads[i], NULL, crack_thread_task, buff);
        threadsAvailable++;
    }

    fp = fopen("./passwords.txt", "r");

    while(fgets(buff, BUFFSIZE, (FILE*)fp)) {
        // Remove the new line character \n
        if ((newLinePos=strchr(buff, '\n')) != NULL)
            *newLinePos = '\0';
        
        pthread_mutex_lock(&signalLock);
        while(threadsAvailable < 1) {
            // Wait until workers available
            pthread_cond_wait(&crack_complete, &signalLock);
        }
        
        signaled = true;
        pthread_cond_signal(&signalAvailable);
        pthread_mutex_unlock(&signalLock);
        
        // Wait until workData has been fetched
        pthread_mutex_lock(&workDataLock);
        while(!workDataFetched) {
            pthread_cond_wait(&crack_start, &workDataLock);
        }
        workDataFetched = false;
        pthread_mutex_unlock(&workDataLock);

        hashCount++;
    }
    fclose(fp);
    
    // Wait until done cracking all the hashes
    pthread_mutex_lock(&signalLock);
    while (hashCount > 0) {
        pthread_cond_wait(&crack_complete, &signalLock);
    }
    
    // Broadcast thar we are done
    done = true;
    pthread_cond_broadcast(&signalAvailable);
    pthread_mutex_unlock(&signalLock);

    for(i = 0; i < NUMTHREAD; i++) {
        pthread_join(threads[i], NULL);
    }

    pthread_cond_destroy(&signalAvailable);
    pthread_cond_destroy(&crack_complete);
    pthread_cond_destroy(&crack_start);
    pthread_mutex_destroy(&signalLock);
    pthread_mutex_destroy(&printLock);
    pthread_mutex_destroy(&workDataLock);
    
    printf("Done\n");
    return 0;
}
