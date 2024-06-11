
# iVerify Log Processor

This is a telemetry log data processor written in Python for the iVerify Coding Challenge.

It takes a tar file (`.tar.gz`) as an input, finds and extracts the relevant log files (`ps.txt` and `powerlog_<yyyy>-<MM>-<dd>_<HH>-<MM>_<id>.plsql`), processes them into standardised JSON format, and outputs the resulting JSON files to a specified output directory.


## Authors

- [stas-vas](https://github.com/LuckyRG)


## Tech Stack

Written in Pure Python 3.12.4 - no external package dependencies


## Compatibility:

This code was tested on Windows 7+ and MacOS 10+

## Assumptions Made (for this coding challenge):

- The input file format will always be the same - a tar.gz file.
.zip will not work, since it is parsed differently, though it would be straight forward to add support for this, if needed
- We are always looking for the two log files to process - a `ps.txt` file, and a db file that has a name format of `powerlog<_any other valid file name chars_>.PLSQL`. It does not matter where in the tar file these two log files are located, as a search is done to find their path automatically
- These two log file names are unique per TAR file (i.e. only one `ps.txt` and `powerlog...plsql` file exist in the input TAR).
If there are multiple of these log files in the TAR, the first path will be taken and used
- The column names in the ps.txt log file will always have the same name, be in the same order, and have the same data type (only had a single example to work from, but assuming this is the case)
- The SQLite DB log file (.PLSQL) will always need the same table parsed. This table will always have the same column names and data types (again, working from the sole example that I have)


## How To Run Locally

Make sure you have Python version 3.12.4 installed on your system.
(can download from https://www.python.org/downloads/ ).

Download this repo and extract it.

![screenshot-1](https://i.imgur.com/nCAEEM3.png)

To run, open cmd / terminal in the root folder of wherever you extracted this project (should see the `main.py` file in this directory).

![screenshot-2](https://i.imgur.com/tZDC0ym.png)

If you have multiple Python versions installed on your system, make sure that Python 3.12.4 is selected (in MacOS can do this by running `alias python=python3.12` command. For Windows, you will have to set this in your `PATH` system enviroment vairable).
Can check via `python --version`

Have a valid TAR (`.tar.gz`) log telemetry file (not more than 400MB in size, and containing `ps.txt` and `powerlog_<yyyy>-<MM>-<dd>_<HH>-<MM>_<id>.plsql` files).

I have provided a number of TAR files for testing, with different variations of the log files (Google Drive Link):
https://drive.google.com/drive/folders/1WYjPv9r9AC3-TtqraFM4krf0o-Snpk-2?usp=drive_link


![screenshot-3](https://i.imgur.com/OzpRsyh.png)

Run 
```
python main.py --input "<path-to-tar-file>.tar.gz" --output "existing-output-folder-where-resulting-json-files-will-be-written"
```

![screenshot-4](https://i.imgur.com/WkUNqZN.png)

For example:
```
python main.py --input "input-files/sysdiagnose_2024.04.16_19-30-52+0100_iPhone-OS_iPhone_21E236.tar.gz" --output "results-json"
```

This example has the `sysdiagnose_2024.04.16_19-30-52+0100_iPhone-OS_iPhone_21E236.tar.gz` telemetry log file in the `<project-root>/input-files` folder, and will output the resulting JSON files to the `<project-root>/results-json` folder.

![screenshot-5](https://i.imgur.com/slAFPUv.png)

Resulting JSON files will have a UTC timestamp of when the file was processed appended to the name, to keep file names unique and recognisable.

![screenshot-6](https://i.imgur.com/PwdzUIF.png)

## Running Tests

To run all unit tests locally, run the following command in terminal / cmd (the `-b` option silences logs during tests)

```bash
python -m unittest -b
```

This could also be used in CI, such as a step in GitHub Action

## Possible Improvements / Further Development

This program is made to run locally for the purposes of the code challenge, but it would not take much to make it Cloud-Native.

With AWS and Serverless in mind, it would be relatively straight-forward to change this to run inside a Lambda function / handler.

The main changes would be around the input in `main.py`. 
Instead of user-provided arguments, and local file system paths, the function would start on recieving an event from AWS SQS or an AWS S3 bucket.

Then, instead of doing the data processing in-memory, the temp files would be wiritten to [Lambda ephemeral storage](https://aws.amazon.com/blogs/aws/aws-lambda-now-supports-up-to-10-gb-ephemeral-storage/) (up to 10GB), and read from there during processing.

Resulting JSON files would then be written to another S3 bucket, rather than the local file system.