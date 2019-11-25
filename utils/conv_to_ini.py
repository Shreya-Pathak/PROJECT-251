from reportlab.pdfgen import canvas
#from reportlab.lib.units import inch
from reportlab.lib.colors import black
import os
#from pdflatex import PDFLaTeX
import subprocess

def conv_to_txt(dic):
	#print(dic)
	f=open('ans.tex', 'w+')
	f.write('\\documentclass{article}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amsmath}\n\\title{Question Bank}\n\\begin{document}\n')
	f.write('\\maketitle\n')
	for k,v in dic.items():
		if k=="main":
			i=1
			for q in v:
				f.write('\\section{Question '+str(i)+"}")
				#f.write("Question"+" "+str(i)+"\n")
				i+=1
				for k1,v1 in q.items():
					if k1=="sub":
						f.write('\n')
						j=1
						for sq in v1:
							f.write('\\subsection{Subquestion '+str(j)+"}")
							#f.write("Subquestion"+" "+str(j)+"\n")
							j+=1
							for k2,v2 in sq.items():
								f.write(str(k2)+ ":" +str(v2)+"\\\\")
					else:
						f.write(str(k1)+": "+str(v1)+"\\\\")
				f.write("\n")
		else:
			f.write(str(k)+": "+str(v)+"\\\\")
	f.write('\\end{document}')
	f.close()

def conv_to_tex(dic):
	f=open('ans.tex','w+')
	tab =""
	tab1 = ""
	tab2 = ""
	for i in range(int(dic['no'])):
		tab+="m{0.5cm} |"
		tab1+="& " +str(i+1)
		tab2+="& "
	f.write('\\documentclass{article}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amsmath}\n\\usepackage{array}\n\\usepackage{fancyhdr}\n\\setlength{\\tabcolsep}{18pt}\n')
	f.write('\\pagestyle{fancy}\n\\lhead{ '+dic['header']+' }\n\\rhead{}\n')
	f.write('\\begin{document}\n\\begin{titlepage}\n\\vspace*{\\fill}\n\\begin{center}\n\\textbf{\\Huge '+ dic['title']+'\\\\ Total Marks ('+ str(dic['tm'])+' marks)}\\\\\n\\textbf{\\Huge '+ dic['header']+' }\\\\\n~\\\\\n~\\\\\n~\\\\\n~\\\\\n')
	f.write('\\begin{tabular}{ |m{2cm} |'+tab +'}\n\\hline\nQues '+ tab1 +'\\\\\n\\hline\nMarks '+tab2+'\\\\\n\\hline\n\\end{tabular}\n~\\\\\n~\\\\\n~\\\\\n~\\\\\n{\\Large Name: \\_\\_\\_\\_\\_\\_\\_\\_\\_}\\\\\n{\\Large Signature: \\_\\_\\_\\_\\_\\_\\_\\_\\_}\n\\end{center}\n\\vspace*{\\fill}\n\\end{titlepage}\n')
	for v in dic['main']:
		f.write('\\section{Question}')
		f.write('\\hfill {\\small ['+ str(v['Marks'])+']}\\\\\n')
		f.write(v['Content'])
		for v1 in v['sub']:
			f.write('\\subsection{Subquestion}')
			f.write('\\hfill {\\small ['+str(v1['Marks'])+']}\\\\\n')
			f.write(v1['Content'])
		f.write('\\\\\n~\\\\')
		f.write('\\textit{Write Solution Here}')
		f.write('\\newpage\n')
	#f.write('\\textit{Space for Rough Work}')
	f.write('\\textit{Scratch Space}')
	f.write('\\end{document}\n')
	f.close()

# def con_to_tex(ldic):
# 	f.open('qp.tex','w+')
# 	f.write('\\documentclass{article}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amsmath}\n\\title{Question Paper}\n\\begin{document}\n')
# 	f.write('\\maketitle\n')
# 	for q in ldic:
# 		f.write('\\section{Question}')
# 		for k,v in q.items():
# 			if k=="sub":
# 				f.write('\n')
# 				for sq in v:
					

# def conv_to_pdf():
# 	styles=getSampleStyleSheet()
# 	styleN=styles['Normal']
# 	styleH=styles['Heading1']
# 	story=[]
# 	pdf_name="ans.pdf"
# 	doc=SimpleDocTemplate(
# 		pdf_name,
# 		pagesize=letter,
# 		bottomMargin=.4*inch,
# 		topMargin=.6*inch,
# 		rightMargin=.8*inch,
# 		leftMargin=.8*inch)
# 	with open("ans.txt", 'r') as txt_file:
# 		text_content=txt_file.read()

# 	P = Paragraph(text_content, styleN)
# 	story.append(P)

# 	doc.build(
#     	story,
# 	)

def conv_to_pdf2():
	file = open("ans.tex", "r")  # text file I need to convert
	lines = file.read()
	file.close()
	report = canvas.Canvas('mypdf5.pdf')#new pdf report i am creating
	report.setFont("Times-Roman", 20)
	report.setFillColor(black)
	report.drawCentredString(100, 800, "Question Bank")

	report.setFillColor(black)
	size = 12
	y = 780
#y = 2.0*inch
#x = 1.3*inch
	for line in lines.split('\n'):
		report.setFont("Helvetica", size)
		report.drawString(10, y, line)
    #y = y-size*1.2
    #size = size+0.5
		y = y - 15
	report.save() 
	#os.remove("ans.txt")


def bash_command(cmd):
    subprocess.Popen(cmd, shell=True, executable='/bin/bash')


def conv_to_pdf3():
	# pdfl = PDFLaTeX.from_texfile('ans.tex')
	# pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=True)
	#bash_command('pdflatex ans.tex --output-directory"home/Music/')
	os.system("pdflatex ans.tex")
	os.remove("ans.tex")
	os.remove("ans.log")
	os.remove("ans.aux")

