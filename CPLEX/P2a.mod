/*********************************************
 * OPL 12.8.0.0 Model
 * Author: juan.jose.olivera
 * Creation Date: 04/03/2025 at 11.20.47
 *********************************************/

 int nCPUs = ...;
 int nTasks = ...;
 
 range tasks = 1..nTasks;
 range computers = 1..nCPUs;
 
 float rt[tasks] = ...;          // amount of processing time requested by Task t
 float rc[computers] = ...;     // maximum amount of processing resource available con Computer c
  
 dvar boolean assigment[tasks][computers]; // proportion [0, 1] of assigment of task i on computer j
 dvar float+ z;                           // maximum load on any computer
 
 execute {
   // Compute totalLoad and totalCapacity to perform validation
   var totalLoad = 0;
   for (var t = 1; t <= nTasks; t++) {
     totalLoad += rt[t];
   }
   writeln("Total load: " + totalLoad);
   
   var totalCapacity = 0;
   for (var c = 1; c <= nCPUs; c++) {
     totalCapacity += rc[c];
   }
   writeln("Total capacity: " + totalCapacity);
   
   if (totalLoad > totalCapacity) {
     writeln("Insufficient compute capacity to satisfy load!");
     stop();
   }
 }
 
 // Minimize z which is highest load in any computer
 minimize z;
 
 subject to {
 	satisfaction: 
 		forall(t in tasks)
 		  sum(c in computers) assigment[t][c] == 1;
 	availability:
 		forall(c in computers)
 		  sum(t in tasks) rt[t] * assigment[t][c] <= rc[c];
 	maxload:
 		forall(c in computers)
 		  z >= (1/rc[c]) * (sum(t in tasks) rt[t] * assigment[t][c]);
 }
 
 
execute {
    // Print CPU's Loads
	for (var c = 1; c <= nCPUs; c++) {
	  var load = 0;
	  for (var t = 1; t <= nTasks; t++) {
	    load += rt[t] * assigment[t][c];
	  }
	  load = (1/rc[c]) * load;
	  
	  writeln("CPU #" + c + " has load: " + (100*load) + "%");
	} 
	
	// Print Solution
	settings.displayPrecision=8;
	
	for (var t = 1; t <= nTasks; t++) {
	  for (var c = 1; c <= nCPUs; c++) {
	    writeln("assig[" + t + "][" + c + "] = ", assigment[t][c]);
   	  }	    
	}
}