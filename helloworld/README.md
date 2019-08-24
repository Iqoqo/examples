
# helloworld

This is a collection of simple, straightforward scripts that can be used to illustrate input/output capabilities of the DISCO job runtime,
as well as for troubleshooting.

## Scripts

### Argument Echo 

**Script**: `argument_echo.py`

You can pass a filename as an argument and read from the file in your code, assuming that file has been submitted as a part of the job.

An easy way to understand the behavior is to run the script locally.

```
$ python argument_echo.py error_output.py
```

In this case we pass another script in the argument. This produces the following output, printing the other script's content.

```
error_output.py
ohhh no... this is an error since its not a valid python code
```

The argument echo script may be used for troubleshooting a job, to see if an input file makes it as expected to the job runtime.

### Long-Running Task with Simple Output

**Script:** `long_running_task.py`

This script does not accept arguments, but produces standard output by printing a sequence of numbers from 1 through 999 at a constant interval, 
for a total of ~1000 seconds (~17 minutes).

### Error Output

**Script:** `error_output.py`

This is not a valid Python file and therefore will produce an error. 
It simulates a situation when a script cannot be executed for some reason, such as missing dependencies, syntax errors, etc.