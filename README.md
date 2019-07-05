# Electronic Defense Weapon Report

## TL;DR

This program gathers information from a set of fillable PDFs and returns a CSV file where each row is the data from one PDF.

## Motivation

Law Enforcement agencies in the state of Connecticut are required to document taser deployments and usage with a standardized PDF report;

> Public Act 14-149 requires “each law enforcement agency that authorizes a police officer employed by such agency to use and electronic defense weapon shall: (A) Not later than January 31, 2015 adopt and maintain a written policy that meets or exceeds the model policy developed by the Police Officer Standards and Training Council regarding the use of an electronic defense weapon”; (B) “require police officers to document any use of an electronic defense weapon in use-of-force reports”; (C) “not later than January fifteenth following each calendar year in which an electronic defense weapon is used, prepare an annual report using the form developed and promulgated by the Police Officer Standards and Training Council. (Source: [State of Connecticut Office of Policy and Management](https://portal.ct.gov/OPM/CJ-External/Electronic-Defense-Weapon-Reports/Electronic-Defense-Weapon-Reports?fbclid=IwAR2hLzhT4JtQWWTJqy6R8_xLjvU3JvNLixe4oH7pUIv81y-bkggkEfWqGpY))

This program aims to automate data collection from sets of these report PDFs into data sets that can be used by organizations, such as the ACLU, for analysis.

## Usage

1. All PDFs to be scraped must be in the same folder.  
  
2. The `scraper.py` file must be accessible by the `main.py` file, which is used to execute the program (this can be achieved by making `__init__.py` files in all directories between `scraper.py` and `main.py`, or simply by keeping them in the same directory).

3. Edit the `main.py` file to use the proper file path as an argument of the `Scraper` class instantiation. The basic file should look like this (where the file path reflects where the PDFs to be scraped are stored):

```python
import scraper

scraper = scraper.Scraper("/Users/samgaudet/Documents/GitHub/taser_pdf/test_pdfs/")

scraper.scrape()
```

4. Execute the `main.py` file in the terminal:

```shell
$ python3.6 main.py
```

5. The output of the program, a CSV file called `export.csv` will be in the directory with all of your PDFs.

## Improvements To Make

- [ ] Implementation of `os` library that searches child directories.
- [ ] Integrity check to make sure all PDFs include the same fields.
- [ ] Improve error and exception handling.
- [ ] Remove pandas `index` as a column in the dataframe.
- [ ] Add PDF filename as a column in the dataframe for reference.