import fitz
import sys

"""
install the pymupdf module:
$ pip3 install pymupdf
then
./rotate_resize.py *.pdf
or
python3 rotate_resize.py *.pdf
"""
#lets create a function
def export_to_portrait(name):
    #open the landscape PDF
    doc_l=fitz.open(name)
    #open an empty PDF for portrait
    doc_p=fitz.open()
    #we iterate on all the pages from the landscape PDF
    for page in doc_l:
        #lets store the page number
        p_num=page.number
        #rect is a matrix with the bounding box of the page [0,0,width,height]
        rect_l=page.bound()
        # for convenience we store width and height
        w=rect_l[2]
        h=rect_l[3]
        #print(f"w={w}-h={h}")
        #we create a new page in the new document, we invert width and height for portrait mode
        doc_p.newPage(width=h,height=w)
        #we need to create another Rectangle that will be the location we insert the content to
        #here its centered in the middle of the portrait page
        #if you want it on top : x0=0,y0=0,x1=h,y1=h/2**0.5
        #note 2**0.5=squareroot(2)
        x0=0
        y0=(w-h/(2**0.5))/2
        x1=h
        y1=y0+h/2**0.5
        #print(f"x0={x0}, yo={y0}, x1={x1}, y1={y1}")
        #we create the rectangle
        rect=fitz.Rect(x0,y0,x1,y1)
        #we insert in page 'p_num' of 'doc_p' the page number 'p_num' of document 'doc_l' in the rectangle 'rect'
        #with this method the pdf is not included as an image but as a small PDF in the PDF
        #this way you can still select text and the size is the same as the original
        doc_p[p_num].showPDFpage(rect,doc_l,p_num,keep_proportion=True)
    #at the end of the loop we save the new document
    doc_p.save(f"Rotated-{name}")
    
#create a list of the arguments provided in the command line
list_inputs=sys.argv

#iterate the function on all the pdf (only)
for file in list_inputs:
    if file.endswith(".pdf"):
        print(f"{file} is a pdf, processing...")
        export_to_portrait(file)
    else:
        print(f"{file} is not a pdf")
