
Asignacion de tarea i en CPU j = (i, j)


maxCpuLoad(candidate, solution):
    dummySolution <- solution U { candidate }
    return max {  usedResources(cpu, solution) + r_t / capacity(cpu) | for cpu in CPUS(dummySolution) }

Greedy(tasks):
    solution <- {}
    sortedTasks <- sort(tasks, decreasingResourcesCriterium)

    for each task in sortedTasks do
        candidates <- { (task, cpu) | for cpu in CPUs and leftCapacity(cpu, solution) - resources(task) >= 0 }

        if candidates = {} then
            return "No feasible solution found for problem"
        
        assignment <- argmin { maxCpuLoad(c, solution) | for c in candidates}

        solution <- solution U { assignment }

    return solution
