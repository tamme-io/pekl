# PEKL
## Yiddish: Package


This package is designed for AWS Lambda invocations and responses.

AWS Lambda has limits on the body size that can be used to invoke a function
and the size of the response that is returned.

When using AWS Lambda prolifically these limits can be cumbersome.

Pekl addresses this issue by checking the size of the body when invoking a
function or receiving the response from an invoked function. If the body
is too large then it writes it to an S3 bucket and then reads the contents of
the file in the receiving function.

To prevent excess data usage and transfer costs it is wise to initialize Pekl
in the same region that your functions are running in and to make sure that
the bucket that you use has appropriate retention policies initiated.



### Handling Pekl events


```python

from pekl import Pekl

Pekl = Pekl.Pekl("BUCKET_NAME", "REGION") # Region is optional


def handler(event, context):
  # Receive the event via Pekl, if it has been sent via any means other than
  # Pekl it will automatically be translated, and if Pekl has sent the event
  # and it has been larger than 128kb then it will be read from the S3 Bucket
  # it was written to.
  # NB: This does not necessarily have to be the same bucket as you have used
  # in this script when initializing Pekl
  event = Pekl.receive(event)

  response = someFunction(event)

  # Respond to the event using Pekl to make sure that any large event bodies
  # are handled. Pekl aims to write anything that is larger than 4.7MB in python
  # memory to leave headroom for any transformations that AWS choose to do
  # or any mysterious headroom in the black box of lambda.
  return Pekl.respond(event)

```



### Invoking functions with Pekl


```python

from pekl import Pekl

Pekl = Pekl.Pekl("BUCKET_NAME", "REGION") # Region is optional


def handler(event, context):

  # Use pekl to receive events and automatically read any larger event bodies
  # from the S3 bucket
  event = Pekl.receive(event)

  # Pekl invoke will handle your invocations automatically and handle any
  # large event bodies. It will also handle any json transformations that are
  # required
  # NB : Pekl will try and write any invocation event body that is larger than
  # 100kb to the S3 bucket in order to leave headroom for translation that
  # AWS seems to do when it is passing event bodies between functions.
  lambda_response = Pekl.invoke(
      "FUNCTION_NAME",
      {
        "event" : "dictionary"
      },
      "REGION" # OPTIONAL
  )

  # the response from Pekl comes back as a native Python dictionary, no need
  # to translate from JSON
  some_value = lambda_response.get("some_key")

  # You can also use Pekl to invoke the lambda function asynchronously
  Pekl.invokeAsync(
    "FUNCTION_NAME",
    {
      "some_key" : some_value
    },
    "REGION" # OPTIONAL
  )

  # Then use Pekl to respond, it will handle the JSON for you, as well as
  # ensuring that any large event bodies are written to S3 and replaced with
  # the details for Pekl to pick up on the receiving end.
  return Pekl.respond(
    {
      "some_key" : some_value
    }
  )

```


### Installing Pekl

Pekl is available via PyPi (https://pypi.python.org/pypi/pekl), you can install
using:

```
pip install pekl
```
