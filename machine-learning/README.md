# Machine learning with discomp

This is an example of using Python's built in `multiprocessing` or `discomp` to test many hyperparameters of an XGBoost regression on a credit card fraud dataset.

To test 30 hyperparameter configurations on my MacBook Pro it took:
* 81 minutes and 30 seconds using `map`
* 34 minutes and 40 seconds using `multiprocessing.Pool().map`
* 8 minutes and 52 seconds using `discomp.Pool().map`

For a more detailed explanation see https://dis.co/blog/machine-learning-with-disco/
