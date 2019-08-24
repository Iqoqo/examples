# Light-Curve Calculations

An example of [light curve](https://en.wikipedia.org/wiki/Light_curve) calculations.

The approximate execution time is about four minutes in an DISCO environment.

## Script File

The main script for this job is `light_curve_calculations.py`. 

It can be run locally like in the following example.

```
$ python light_curve_calculations.py data/data137.txt params/orbital_params137.txt
```

*Please note that the script requires a **Python 3.x** runtime.*

## Data Files
  
A file named `data*.txt` from the `data` directory should be passed as the data (first) argument to each task.

## Parameter Files

A file named  `orbital_params*.txt` from the `params` directory should be passed as the parameter (second) argument to each task.

## Constants
  
File  `constant.txt` is a constants file and must be available to each task. It contains a time set used for the light curve calculations.

## Output

The script produces stdout output that prints names of input files and the result of a calculation.