# bugfind

A lightweight Bash utility for finding security writeups by vulnerability type.

`bugfind` retrieves the Pentester Land writeup dataset, searches for matching vulnerability names, and saves the corresponding writeup URLs to a local text file.

## Features

* Search writeups by vulnerability name.
* Case-insensitive matching.
* Retrieve data directly from the remote JSON source.
* Save matching writeup URLs to a local file.
* Automatically generate an output filename when none is specified.
* Does not store the remote JSON dataset locally.

## Requirements

* Bash
* curl
* jq
* sed
* tr
* wc

## Usage

Make the script executable:

```bash
chmod +x bugfind.sh
```

Search for a vulnerability:

```bash
./bugfind.sh -b "Race condition"
```

Using the long option:

```bash
./bugfind.sh --bug "Race condition"
```

Specify an output file:

```bash
./bugfind.sh -b "Race condition" -o race.txt
```

Other examples:

```bash
./bugfind.sh -b "RCE"
./bugfind.sh -b "SQL injection"
```

## Options

| Option                | Description                       |
| --------------------- | --------------------------------- |
| `-b, --bug <name>`    | Vulnerability name to search for. |
| `-o, --output <file>` | Optional output file name.        |
| `-h, --help`          | Display the help message.         |

## Data Source

Writeup data is retrieved directly from the Pentester Land JSON dataset:

https://pentester.land/writeups.json

The dataset is not downloaded or stored locally.

## Output

If no output file is specified, `bugfind` generates a filename from the vulnerability name.

For example:

```bash
./bugfind.sh -b "Race condition"
```

generates:

```text
race-condition.txt
```

The output file contains URLs of matching security writeups.

## Use Cases

`bugfind` can be useful for:

* Security research
* Bug bounty research
* Penetration testing research
* Vulnerability-specific writeup discovery
* Building security research references

## License

This project is provided for educational and security research purposes.
