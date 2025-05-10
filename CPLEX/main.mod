/*********************************************
 * OPL 22.1.2.0 Model
 * Author: jjoul
 * Creation Date: Mar 9, 2025 at 10:34:26 AM
 *********************************************/


// Execution Parameters (value in params.dat). Can be later used as thisOplModel.[variableName]
string dataFile=...;
string modelFile=...;
string outputFile=...;
float epgap=...;



 main {
	var src = new IloOplModelSource(thisOplModel.modelFile);
	var def = new IloOplModelDefinition(src);
	var cplex = new IloCplex();
	var model = new IloOplModel(def,cplex);
	var data = new IloOplDataSource(thisOplModel.dataFile);
	model.addDataSource(data);
	model.generate();

	cplex.epgap = thisOplModel.epgap;
	writeln("\n\nGoing to Run CPLEX Solver");
	writeln("--Data file: " + thisOplModel.dataFile);
	writeln("--Model Used: " + thisOplModel.modelFile);
	writeln("--Output file: " + thisOplModel.outputFile);
	writeln("--Using hyperparameter cplex.epgap = " + cplex.epgap);

	if (cplex.solve()) {
		writeln("[SOLVED]");
		writeln("[OPTIMAL COST] " + cplex.getObjValue());

		var f = new IloOplOutputFile(thisOplModel.outputFile);
		f.writeln("z = ", cplex.getObjValue(), ";");
		f.close();
	}
	else {
		writeln("[UNSOLVED]");
	}

	data.end();
	model.end();
	cplex.end();
	def.end();
	src.end();
 }


 	// var src = new IloOplModelSource("P1.mod");
 	// var def = new IloOplModelDefinition(src);
 	// var cplex = new IloCplex();
 	// var model = new IloOplModel(def, cplex);
 	// var data  = new IloOplDataSource("P1.dat");
 	// model.addDataSource(data);
 	// model.generate();
 	
 	// cplex.epgap = 0.01;
 	
 	// if (cplex.solve()) {
 	//   writeln("Max load is " + (100 * cplex.getObjValue()) + "%");
 	//   for (var c = 1; c <= model.N_COMPUTERS; c++) {
	//   	var load = 0;
	// 	  for (var t = 1; t <= model.N_TASKS; t++) {
	// 	    load += model.req[t] * model.assigment[t][c];
	// 	  }
	//   	load = (1/model.avail[c]) * load;
	//   	writeln("CPU #" + c + " has load: " + (100*load) + "%");
	//   } 
	  
	
	// 	for (var t = 1; t <= model.N_TASKS; t++) {
	// 	  for (var c = 1; c <= model.N_COMPUTERS; c++) {
	// 	    writeln("assig[" + t + "][" + c + "] = ", model.assigment[t][c]);
	//    	  }	    
	// 	}
 	// } else {
 	//   writeln("No solution found!");
 	// }
 	
 	// model.end();
 	// data.end();
 	// def.end();
 	// cplex.end();
 	// src.end();
//  }