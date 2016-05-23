# cellular_automaton.py
## Author
Daniel J. Rothblatt, May 2015

## Description
A cellular automaton is a model of computation pioneered by John von
Neumann. A cellular automaton is a matrix of cells whose values are
determined by their neighbors' values. Rules governing cellular
automata can be specified in a fairly simple way (depending on the
rules, a full set of rules can be represented as a small natural
number), yet some rules have been shown to be Turing-complete.

This project provides a command-line binary cellular automaton (in
other words, all cells have a value of either 0 or 1).

## Purpose
I started this project because I was interested in identifying
patterns in cellular automata rulesets.

## Use

### Grammar
    <command> ::= python3 cellular_automaton.py <nullary_flag>*
    <unary_flag>*
    <nullary_flag> ::= -s | -c
    <unary_flag> ::= (-n | -d | -i) \d+
EX: python3 cellular_automaton.py -s -c -n 20 -i 40 -d 1

### Semantics
#### Nullary Flags
- -s: ("spill") Indicates that the cellular automaton is built on
a sphere topology; if a cell is on the periphery of the matrix,
its neighbors include cells on the other side of the periphery.
- -c: ("control") Allows the user to step through the iterations
of the cellular automaton.

#### Unary Flags
 - -i: ("iterations") Indicates that the next argument will be a
 number indicating how many iterations to step through the
 automaton.
 - -n: ("N x N") Indicates that the next argument will be a number
 specifying the size of the cell matrix (which is square)
 - -d: ("dimension") Indicates that the next argument will be a
 number (1 or 2) specifying whether a cell counts neighbors in 2D
 or 1D. If 1D, neighbors are only to the left and right of a cell.

## To Do
   Many things would make this cellular automaton more useful and
   interesting. Potential improvements include:
- Translation to a GUI: A graphical user interface would allow the user
  to, among other things, turn individual cells on and off manually,
  which allows users to experiment more freely with the effects of
  their rules
- User-side rule input: Nobody should have to open up and edit the
  cellular automaton's code just to specify new rules. An interface
  for reading in rules would make the process of using the automaton
  less tedious.
- Greater range of cell values: If rules worked in a non-binary way
  (by making cell values reals instead of elements of {0,1}, for
  example), what would they represent? To make this at all coherent
  would require a good graphical interface.
