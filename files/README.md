# Arcticons Request Randomizer
A Python3 script that chooses icon requests from [Arcticon](https://github.com/Donnnno/Arcticons)'s `requests.txt` file randomly, because I am indecisive.

## Requirements
Python 3.11+

## Usage
```
python3 random_requests.py [-h] [-di [INPUT_DIR]] [-do [OUTPUT_DIR]] [-n [NUMBER]] [-s [SKIP_POPULAR]] [-t [REQUEST_THRESHOLD]] [-v]
```
The script writes `random_requests.txt` containing the randomly selected requests, and `new_requests.txt` containing the content of `requests.txt` with the randomly selected requests removed.

## Parameters
```
  -h, --help            show this help message and exit
  -di [INPUT_DIR], --input-dir [INPUT_DIR]
                        directory of requests.txt (default=same as this script)
  -do [OUTPUT_DIR], --output-dir [OUTPUT_DIR]
                        directory of the output files (default=same as this script)
  -n [NUMBER], --number [NUMBER]
                        number of requests to be randomly selected (default=10)
  -s [SKIP_POPULAR], --skip-popular [SKIP_POPULAR]
                        skip N most popular requests (default=0/no skip)
  -t [REQUEST_THRESHOLD], --request-threshold [REQUEST_THRESHOLD]
                        selected requests must have been requested at least N times (default=1)
  -v, --verbose         show verbose output
```

## Examples
### Randomly choosing 10 icon requests from `requests.txt` that is in the same folder as the script
```
python3 random_requests.py
```

### Randomly choosing 20 icon requests that have been requested at least 2 times from `requests.txt` that is in the same folder as the script
```
python3 random_requests.py -n 20 -t 2
```

### Randomly choosing 15 icons requests from `requests.txt` that is in the same folder as the script, excluding top 20 most requested icons
Why? Because Donnnno is probably already on them.
```
python3 random_requests.py -n 15 -s 20
```

### Randomly choosing 10 icon requests from `requests.txt` that is in the `\home\myuser\git\Arcticons\other\` directory and writing the output files to a sub-folder `out` of where this script is
```
python3 random_requests.py -di "\home\myuser\git\Arcticons\other" -do ".\out"
```

## License
`random_requests.py` is licensed under [The Unlicense](https://opensource.org/license/unlicense/)
