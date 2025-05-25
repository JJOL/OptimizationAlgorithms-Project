/*********************************************
 * OPL 22.1.2.0 Model
 * Author: Juan Jose Olivera & Pol Verdura
 * Creation Date: Mar 9, 2025 at 10:34:26 AM
 *********************************************/


// Execution Parameters (value in params.dat). Can be later used as thisOplModel.[variableName]
string dataFile=...;
string modelFile=...;
string outputFile=...;
float epgap=...;
float tilim=...;


 main {
	var src = new IloOplModelSource(thisOplModel.modelFile);
	var def = new IloOplModelDefinition(src);
	var cplex = new IloCplex();
	var model = new IloOplModel(def,cplex);
	var data = new IloOplDataSource(thisOplModel.dataFile);
	model.addDataSource(data);
	model.generate();

	cplex.epgap = thisOplModel.epgap; // comment this for trying to find the most optimal solution in the time limit
	cplex.tilim  = thisOplModel.tilim;
	cplex.barobjrng = 498318;
	writeln("\n\nGoing to Run CPLEX Solver");
	writeln("--Data file: " + thisOplModel.dataFile);
	writeln("--Model Used: " + thisOplModel.modelFile);
	writeln("--Output file: " + thisOplModel.outputFile);
	writeln("--Using hyperparameter cplex.epgap = " + cplex.epgap);
	writeln("--Using hyperparameter cplex.tilim = " + cplex.tilim);

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