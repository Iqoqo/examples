# Passing Constants

This job performs a calculation on the elements of a two-dimensional array of decimal point numbers. Each value is multiplied by a given number and the product is then raised to a given power. The elements are fed from a data file, the multiplicative factor and the power are read from  constants files.

The console output of a task will also include a text header specified also by a constant file.

## Script File

The main script for this job is `calculation_2d_array.py`. 

## Data Files
  
A file named `data*.txt` located in the `data` directory should be passed as the data argument to each task.

## Constants
  
File `header.txt` contains a header (constant) that will be printed during each execution.
The multiplicative factor is stored in `multiplicative_factor.txt` and the power in `power.txt`. 

## Output

The job produces output that prints the header specified in the constants file, and the result of a calculation in the form of rows of numbers.