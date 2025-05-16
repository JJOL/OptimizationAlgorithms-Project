/*********************************************
 * OPL 22.1.2.0 Model
 * Author: Juan Jose Olivera & Pol Verdura
 * Creation Date: May 14, 2025 at 10:58:18 AM
 *********************************************/

 int N =...;
 range ii = 1..N;
 range jj = 1..N;
 float m[ii][jj]=...;  // m[i][j] = the $$ bid of i against j
 int   a[ii][jj];      // a[i][j] = 1 if there is any bid between i and j, that is m[i][j] > 0 or m[j][i] > 0
 
 dvar boolean x[ii][jj]; // x[i][j] = 1 if i has preference over j, else 0
 dvar int u[ii];		 // u[i] = partial order value of i against the rest.
 
 execute {
   /* precompute a[i][j] from m[i][j] to use in constraints
    * to avoid an unintentional assigment x[i][j] when there is no bid between i and j
    */
   for (var i = 1; i <= N; i++) {
     for (var j = 1; j <= N; j++) {
       if (m[i][j] > 0 || m[j][i] > 0)
			a[i][j] = 1;
		else
			a[i][j] = 0;
     }
   }
 }
 
 maximize sum(i in ii, j in jj) m[i][j]*x[i][j]; // maximize profit from selecting bids
 
 subject to {
   NoAutobid:
   	forall(i in ii)
   		x[i][i] == 0;
   BidWinner:
   	forall(i in ii, j in jj: i != j)
   		x[i][j] + x[j][i] <= a[i][j];
   OrderLimits:
   	forall(i in ii)
   		1 <= u[i] <= N;
   PartialOrder: 
   	forall(i in ii, j in jj)
   		u[i] - u[j] + 1 <= (N)*(1-x[i][j]); // x[i][j] -> u[i] < u[j] and apply transformation
 }
 
 