# DevTools

DevTools is a collection of utility scripts aimed at assisting developers with
various tasks. This repository contains a variety of scripts, each solving a
unique problem. The code is written in Python and is intended to be easy to
understand, modify and use.

## Scripts

### devtools.timed

The `timed` script is a Python decorator for timing asynchronous functions. It
uses Python's `time.monotonic_ns` function to measure the time it takes for a
function to run. It then saves this timing information in a log.

You can use this decorator by importing it and using it to decorate your
asynchronous functions like this:

```python
from devtools.timed import timed

@timed
async def my_function():
    # Your code here...

```

The decorator will automatically measure the time it takes for your function to
run and add it to the log. You can process the logs using the provided
`process_logs` function, which will give you a summary of timings for all timed
functions.

## License

This project is licensed under the LGPL-3.0 License - see the
[LICENSE](https://github.com/Nachtalb/devtools/blob/master/LICENSE) file for
details.

## Author

Nachtalb - [GitHub](https://github.com/Nachtalb)

## Contributions

Contributions are welcome. Please open a pull request to contribute to this
project.
