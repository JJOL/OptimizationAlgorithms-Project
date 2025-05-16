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