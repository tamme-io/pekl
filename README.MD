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
import pekl

Pekl = pekl.init("BUCKET_NAME", "REGION")


def handler(event, context):
  event = Pekl.receive(event)
  response = someFunction(event)
  return Pekl.respond(event)
```



### Invoking functions with Pekl


```python
import pekl

Pekl = pekl.init("BUCKET_NAME", "REGION")


def handler(event, context):
  event = Pekl.receive(event)
  lambda_response = Pekl.invoke(
      "FUNCTION_NAME",
      {
        "event" : "dictionary"
      },
      "REGION" # OPTIONAL
  )
  some_value = lambda_response.get("some_key")
  Pekl.invokeAsync(
    "FUNCTION_NAME",
    {
      "some_key" : some_value
    },
    "REGION" # OPTIONAL
    )
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
