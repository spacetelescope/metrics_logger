> # STScI Metrics Logger


[![CI](https://github.com/spacetelescope/metrics_logger/actions/workflows/metrics_logger_ci.yml/badge.svg)](https://github.com/spacetelescope/metrics_logger/actions/workflows/metrics_logger_ci.yml)
[![Powered by STScI Badge](https://img.shields.io/badge/powered%20by-STScI-blue.svg?colorA=707170&colorB=3e8ddd&style=flat)](http://www.stsci.edu)
[![codecov](https://codecov.io/gh/spacetelescope/metrics_logger/graph/badge.svg?token=hGkFbpjWBk)](https://codecov.io/gh/spacetelescope/metrics_logger)

The metrics logger is a simple decorator intended to provide standardized logging for annotated pytest methods with tags to identify associated build requirements. As this is a generic utility, any method can be decorated and any type of tagging can be provided.

Log messages will follow a format that will provide:

- METRIC - A static tag that will mark the beginning of the message.
- Tags - A comma delimited list of the provided tags to the decorator.
- Method - The decorated method name.
- Result - FAIL if the method raises an exception and PASS otherwise.

The above will be delimited with a spaced hyphen: ` - `

> **Note**\
> Hyphens in the provided tags are supported.

## Installation

The metrics_logger utility is not currently available in PyPi. To include it in a Conda environment, you can refer to it directly in your conda environment file in the pip section as follows:

```yml
dependencies:
  - pip
  - pip:
    metrics_logger https://github.com/spacetelescope/romancal.git
```

## Development

metrics_logger development can be done with Conda.

### Create and activate the environment
```
$ conda env create --file conda-env.yml
$ conda activate metrics-logger
```

### Update the requirements
```
$ conda activate metrics-logger
$ conda env update --file conda-env.yml
```

## Usage

Import the metrics_logger utility and insert it above the method to be annotated providing a list of tags as arguments. Each time the method is invoked, it will result in a log line being emitted to a logger named "metrics_logger".

Example:
```python
from metrics_logger.decorators import metrics_logger

@metrics_logger('DMS86', 'DMS-129')
def test_some_functional_thing():
    assert True
```

Will result in the following log line (depending on log format):
```text
2023-06-14 16:09:28,947 - stpipe - INFO - DMS86, DMS129 - test_some_functional_thing - PASS
```

Similarly:
```python
@metrics_logger('DMS86', 'DMS-129')
def test_some_functional_thing():
    raise Exception("Oops!")
```

Will result in:
```text
2023-06-14 16:10:09,221 - stpipe - INFO - DMS86, DMS129 - test_some_functional_thing - FAIL
```
