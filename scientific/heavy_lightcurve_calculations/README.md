# Heavy Light-Curve Calculations

An example of very heavy [light curve](https://en.wikipedia.org/wiki/Light_curve) calculations, taking up to 35 hours to complete in an DISCO environment.

## Script File

The main script is `job.py`. 

It can be run locally using, for example

```
$ python job.py data/KOI_137_lc.txt params/params.txt
```

*Please note that the script requires a **Python 3.x** runtime.*

## Data Files
  
A file named `KOI*.txt` located in the `data` directory should be passed as the data (first) argument to each task.

## Parameter Files

A file named  `params.txt` located in the `params` directory should be passed as the parameter (second) argument to each task.

## Constants
  
This job does not require constants.

## Output

The script produces console (stdout) output and a number of files.