# PDF DATA EXTRACTION WITH PYTHON

## Goal
The goal of this project is to automatically extract relevant or key data from similarily-structured _.pdf_ files, with the aim to analyze the data and compute some statistics for the sake of it.

In my case, the files I wanted to analyze were parking fines (in Paris you get a lot if you do not pay attention to where you are and how long you are staying there).

The format of those fines is identical wherever you get fined as long as it is within the French territory.

## Preparation
### 1. Install dependencies :hatching_chick:
Inside the project root, run: `pip install -r 'requirements.txt'`

### 2. Make sure your files are ready :hatched_chick:
Such a project is only interesting if you have a lot of files to analyze, otherwise its usefulness is obviously questionable.

That being said, the first thing to do is to put all your files into `/data/input`. For this project, I included **one** sample showcase _.pdf_ file.

**IMPORTANT**
The _.pdf_ files _**have**_ to have gone through OCR (Optical Character Recognition) before proceeding.

## Script execution
### 1. Text data extraction
The script uses the _PyPDF2_ library to extract all the text content from each and every _.pdf_ page.

### 2. Regex filtering and dictionary building
In order to navigate through the previous step resulting text mess, we use regular expressions in order to filter out the information we want to keep, and finally assign it to dictionary keys.

The product of this step is a dictionary for each fine ingested by the script.

### 3. Saving
The data is saved to `/data/output/extraction` as:
* a _.json_ file,
* and a _.pdf_ file.

Every fine page processed is individually cut from its source _.pdf_ file in `/data/input` to be placed in `/data/output/pdf/fine_year/fine_month`. It means that if one _.pdf_ file contains dozens of fines, dozens of individual fine fiels will be created, sorted depending on their issuance year, and appropriately renamed to facilitate further human manipulation.

## Optimization
This project makes use of the _multiprocessing_ package in order increase the speed at which the 'raw' _.pdf_ files are processed.