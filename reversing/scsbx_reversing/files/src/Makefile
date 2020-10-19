all:
	g++ -c instr_mem.cpp -o instr_mem.o -O2
	g++ -c instr_branch.cpp -o instr_branch.o -O2
	g++ -c instr_arith.cpp -o instr_arith.o -O2
	g++ -c instr_logic.cpp -o instr_logic.o -O2
	g++ -c instr_sys.cpp -o instr_sys.o -O2
	g++ -c scsbx.cpp -o scsbx.o -O2
	g++ -c main.cpp -o main.o -O2
	g++ main.o instr_sys.o instr_branch.o instr_logic.o instr_arith.o instr_mem.o scsbx.o -o scsbx
