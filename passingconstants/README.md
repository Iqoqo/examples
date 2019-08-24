# Passing Constants

This job performs a calculation on the elements of a two-dimensional array of decimal point numbers. Each value is multiplied by a given number and the product is then raised to a given power. The elements are fed from a data file, the multiplicative factor and the power are read from a parameters file.

The console output of a task will also include a text header specified by a constant stored in `constant.txt` file.

## Script File

The main script for this job is `calculation_2d_array.py`. 

It can be run locally like in the following example.

```
$ python calculation_2d_array.py data/data2.txt params/params2.txt
```

## Data Files
  
A file named `data*.txt` located in the `data` directory should be passed as the data (first) argument to each task.

## Parameter Files

A file named  `params*.txt` located in the `params` directory should be passed as the parameter (second) argument to each task.

## Constants
  
File  `constant.txt` contains a header (constant) that will be printed during each execution. It must be present in the script's directory.

## Output

The script produces console (stdout) output that prints the header specified in the constants file, and the result of a calculation in the form of rows of numbers.