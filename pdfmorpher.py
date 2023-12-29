import PyPDF2
import tkinter as tk
from tkinter import filedialog

class PdfMorpher():
	def __init__(self):
		self.master = tk.Tk()
		self.master.geometry("400x40")
		self.master.title("PDF-morphing tool by Ashardalon78")

		tk.Button(self.master, text="Extract from PDF", command=self.pdfExtract).grid(row=0, column=0)
		tk.Button(self.master, text="Merge 2 PDFs", command=self.pdfMerge).grid(row=0, column=1)

		self.master.mainloop()

	def pdfExtract(self):	
		pdfInFile = open(filedialog.askopenfilename(title = "Select PDF file to extract from",filetypes = (("PDF Files","*.pdf"),("all files","*.*"))),'rb')
		self.pdfReader = PyPDF2.PdfReader(pdfInFile,strict=False)
			
		self.pdfWriter = PyPDF2.PdfWriter()
		
		self.extractDialog = tk.Toplevel()
		self.extractDialog.title("Pages to extract")
		tk.Label(self.extractDialog,text="From page:").grid(row=0,column=0)
		self.T1 = tk.Text(self.extractDialog,height=1,width=5)
		self.T1.grid(row=0,column=1)
		self.T1.insert(tk.END,1)
		tk.Label(self.extractDialog,text=" to page:").grid(row=0,column=2)
		self.T2 = tk.Text(self.extractDialog,height=1,width=5)
		self.T2.grid(row=0,column=3)
		self.T2.insert(tk.END,len(self.pdfReader.pages))
		tk.Button(self.extractDialog, text="Extract", command=self.pdfExtract_a).grid(row=1, column=4)
		
	def pdfExtract_a(self):
		startp = int(self.T1.get('1.0',tk.END)) - 1
		endp = int(self.T2.get('1.0',tk.END))
		
		for pageNum in range(startp,endp):
			pageObj = self.pdfReader.pages[pageNum]			
			self.pdfWriter.add_page(pageObj)
			
		pdfOutFile = open(filedialog.asksaveasfilename(title = "Name your output",filetypes = (("PDF Files","*.pdf"),("all files","*.*")),defaultextension='.pdf'), 'wb')		
		self.pdfWiter = self.pdfWriter.remove_links()
		self.pdfWriter.write(pdfOutFile)
		pdfOutFile.close()
		
	def pdfMerge(self):
		pdfInFile1 = open(filedialog.askopenfilename(title = "Select first PDF file to merge",filetypes = (("PDF Files","*.pdf"),("all files","*.*"))),'rb')
		pdfReader1 = PyPDF2.PdfReader(pdfInFile1,strict=False)
		pdfInFile2 = open(filedialog.askopenfilename(title = "Select second PDF file to merge",filetypes = (("PDF Files","*.pdf"),("all files","*.*"))),'rb')
		pdfReader2 = PyPDF2.PdfReader(pdfInFile2,strict=False)
		
		pdfWriter = PyPDF2.PdfWriter()
		
		for pageNum in range(len(pdfReader1.pages)):
			pageObj = pdfReader1.pages[pageNum]
			pdfWriter.add_page(pageObj)
			
		for pageNum in range(len(pdfReader2.pages)):			
			pageObj = pdfReader2.pages[pageNum]
			pdfWriter.add_page(pageObj)	

		pdfOutFile = open(filedialog.asksaveasfilename(title = "Name your output",filetypes = (("PDF Files","*.pdf"),("all files","*.*")),defaultextension='.pdf'), 'wb')
		pdfWriter.write(pdfOutFile)
		pdfOutFile.close()
		pdfInFile1.close()
		pdfInFile2.close()
	
if __name__ == '__main__':    
    main_window = PdfMorpher()
	