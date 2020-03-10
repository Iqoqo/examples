# Machine learning with discomp

This is an example of using Python's built in `multiprocessing` or `discomp` to test many hyperparameters of an XGBoost regression on a credit card fraud dataset.

To test 30 hyperparameter configurations on my MacBook Pro it took:
* 81 minutes and 30 seconds using `map`
* 34 minutes and 40 seconds using `multiprocessing.Pool().map`
* 8 minutes and 52 seconds using `discomp.Pool().map`

For a more detailed explanation see https://dis.co/blog/machine-learning-with-disco/

# Launching this example

## Using the dockerfile

You can build and publish the dockerfile from this folder to your dockerhub account.

```
docker build -t your-username/disco-image -f dockerfile .
docker push your-username/disco-image:latest
```

Then set this image as the [default image on disco](https://docs.dis.co/integrations/custom-docker-images).

## Using requirements.txt

To launch locally, utilize a virtualenv, and install the requirements.txt file

```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python credit_fraud.py
```
=======
