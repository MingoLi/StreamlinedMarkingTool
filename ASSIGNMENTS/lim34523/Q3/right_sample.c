#include <stdio.h>
#include <stdlib.h>
 
int main(int argc, char **argv)
{
   char ch;
   FILE *fp;

   char *file_name = argv[1];
 
   fp = fopen(file_name, "r"); // read mode
 
   if (fp == NULL)
   {
      perror("Error while opening the file.\n");
      exit(EXIT_FAILURE);
   }
 
   while((ch = fgetc(fp)) != EOF)
      printf("%c", ch);
 
   fclose(fp);
   return 0;
}