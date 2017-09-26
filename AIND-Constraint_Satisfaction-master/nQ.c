/*
 *  0 1 2 3 4 5 6 7
 *7 - Q - - - - - -
 *6 - - - Q - - - -
 *5 - - - - - - Q -
 *4 Q - - - - - - -
 *3 - - Q - - - - -
 *2 - - - - - Q - -
 *1 - - - - - - - Q
 *0 - - - - Q - - -
 *  5 8 4 7 1 3 6 2
 * The encoding of above is 
 * sol[] = {5,8,4,7,1,3,6,2}
 */
#include <stdio.h>
void displaySolution(int sol[], int n) {
  printf("  0 1 2 3 4 5 6 7\n");
  for (int i=0; i<n; ++i) {
    int board_row = n-1-i;
    printf(" %d", board_row);
    for (int j=0; j<n; ++j) {
      if (sol[j]==n-i) printf(" Q");
      else printf(" -");
    }
    printf("\n");
  } 

  printf ("  "); 
  for(int v=0; v<n; ++v)
     printf (" %d", sol[v]); 
  printf ("\n");
}

void displaySolution_ut() {

  int sol[] = {5,8,4,7,1,3,6,2};
  int n = 8;
  displaySolution(sol, n);
}

unsigned getStdSig(int n) {
  /* a valid sol[] contains int 1 ~ N
   * so all valid sol[]'s have the same signature of 
   * cumulative XOR
   * for all n-Queen solution have the same signature 
   */
  unsigned stdsig = 1; 
  for (unsigned i=2; i<n+1; stdsig ^= i) {}
  return stdsig;
}
/*
 *  every Row have unique number
 *   0 1 2 3 4 5 6 7
 *  {5,8,4,7,1,3,6,2}; -- valid
 *  {5,8,4,7,1,8,6,2}; -- invalid
 *   because Col 1 and 5 have the same value of 8
 *   i.e. Row 7 have 2 Queens in Col 1 and 5 
 */
bool isRowDiff(int sol[], int n, unsigned stdsig) {
  unsigned sig = unsigned(sol[0]); 
  for(int i=1; i<n; ++i) 
    sig ^= unsigned(sol[i]);
  return stdsig==sig; 
}

void isRowDiff_ut() {
  int sol1[] = {5,8,4,7,1,3,6,2}; 
  int sol2[] = {5,8,4,7,1,8,6,2};
  int n = 8; 
  unsigned stdsig = getStdSig(n);
  assert(isRowDiff(sol1, n, stdsig)==true);
  assert(isRowDiff(sol2, n, stdsig)==false);
}

int main(int argc, char* argv[]) {

  // displaySolution_ut();
  isRowDiff_ut();
  return 0;
}

 
