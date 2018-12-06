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
 
//    while((ch = fgetc(fp)) != EOF)
//       printf("%c", ch);

    printf("Hello World!\nA second line!\n\n\nsome text:\nLorem ipsum dolor sit amsd consectetuer adipiscing elit. Integer\neu lsdus accumsan arcu fermentum euismod. Donec pulvinar porttitor\ntellus. Aliquam venenatis. Donec facilisis pharefgdra tortor.  In nec\nmauris eget magna consequat convallis. Nam sed sem vitae odio");
 
   fclose(fp);
   return 0;
}
