import os
import pandas as pd
import numpy as np

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdftypes import resolve1

class Scraper:

	"""
	Given a filepath, scrape the contents of all pdfs in the filepath and create a dataframe where each row is
	the data of one pdf.

	:param filepath: <string> The filepath containing group of pdfs to be scraped
	"""

	def __init__(self, filepath):

		# base filepath for PDF files, inherited from class instantiation
		self.filepath = filepath

		# empty list of filenames to be filled from a walk in the filepath
		self.filenames = []

		# empty list of fields for column names
		self.field_list = []

		# dictionary to convert postscript literal strings to integer booleans
		self.psLiteralDict = {
			"Off" : 0,
			"Yes" : 1
		}

		# csv filename for exported pdf data
		self.exportFilename = "export.csv"

	# ===================================================================

	def getFilesFromPath(self):
		"""
		Given a filepath from the instantiated class, list all pdf files.

		:modify filenames: <list> The list of filenames in the filepath
		"""

		for (dirpath, dirnames, filenames) in os.walk(self.filepath):

			self.filenames.extend(filenames)

			# remove files that do not end with a .pdf extension
			self.filenames = [file for file in filenames if file.endswith(".pdf")]

			break

	# ===================================================================

	def openFileFromPath(self, filename):
		"""
		Given a filename and password, open and return a PDFDocument object.

		:param filename: <str> The filepath for a given PDF
		:return document: <pdfminer.pdfdocument.PDFDocument> The parsed PDFDocument object
		"""

		file = open(self.filepath + filename, "rb")

		parser = PDFParser(file)

		document = PDFDocument(parser)

		return document

	# ===================================================================

	def resolveFields(self, document):
		"""
		Given a list of fields, return the resolved list of fields.

		:param document: <pdfminer.pdfdocument.PDFDocument> The parsed PDFDocument object
		:return fields: <list> The original fields list for a given PDF
		"""

		fields = resolve1(document.catalog['AcroForm'])['Fields']

		return fields

	# ===================================================================

	def getColumnsFromFields(self, fields):

		"""
		Given a resolved list of fields from PDF document, create an empty dataframe with field column names.
    
		:param fields: <list> The original fields list for a given PDF
		:return df: <DataFrame> The empty dataframe with field column names
		"""

		for i in fields:
			field = resolve1(i)
			field_name = field.get('T').decode("utf-8")
			self.field_list.append(field_name)

		df = pd.DataFrame(columns=self.field_list)

		return df

	# ===================================================================

	def getValuesFromFields(self, fields):
		"""
		Given a resolved list of fields from PDF document, create a list of the field values.
    
		:param fields: <list> The original fields list for a given PDF
		:return values: <list> The list of field values for a given PDF
		"""
    	
		values = []

		for i in fields:
        
			field = resolve1(i)
			field_value = field.get('V')
    
			try:
        
				field_value = field_value.decode("utf-8")
    
			except:
        
				field_value = str(field_value).strip("\/")
				field_value = str(field_value).strip("\'") 
				field_value = self.psLiteralDict.get(field_value)
        
			values.append(field_value)

		return values

	# ===================================================================

	def addRowToDataFrame(self, df, values):
		"""
		Given a dataframe and a list, append the list as a new row to the dataframe.

		:param df: <DataFrame> The original dataframe
		:param values: <list> The new list to be added as a row
		:return df: <DataFrame> The dataframe with the newly appended row
		"""

		listLength = len(values)

		newRow = pd.DataFrame(np.array(values).reshape(1,listLength), columns = list(df.columns))

		df = df.append(newRow, ignore_index=True)

		return df

	# ===================================================================

	def writeToCSV(self, df):
		"""
		Given a dataframe, write a CSV file with the contents of the dataframe.

		:param df: <DataFrame> The dataframe containing all pdf data
		"""

		exportFilepath = self.filepath + self.exportFilename

		df.to_csv(path_or_buf=exportFilepath)

	# ===================================================================	

	def scrape(self):
		"""
		Scrape the contents of a set of pdf documents and assemble the data into a global dataframe.

		:export df to csv: <CSV File> The csv containing scraped data from the dataframe
		"""

		self.getFilesFromPath()
		filename = str(self.filenames[1])
		document = self.openFileFromPath(filename)
		fields = self.resolveFields(document)
		df = self.getColumnsFromFields(fields)

		for filename in self.filenames:

			document = self.openFileFromPath(filename)
			fields = self.resolveFields(document)
			values = self.getValuesFromFields(fields)
			df = self.addRowToDataFrame(df, values)

		self.writeToCSV(df)



scraper = Scraper("/Users/samgaudet/Documents/GitHub/taser_pdf/test_pdfs/")

scraper.scrape()

# print(scraped_pdf_df)