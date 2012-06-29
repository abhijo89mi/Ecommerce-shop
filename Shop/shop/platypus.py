from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib import colors
from reportlab.lib.units import inch


styles = getSampleStyleSheet()

Title = "Hello world"
pageinfo = "PLATYPUS Demo"

products = [{'name': 'Cranberry Sauce',
             'description': 'A tasty sauce that goes great with Turkey!'},
            {'name': 'Cranberry Garland',
             'description': 'A decorative strand of dried cranberry fruit.'}]

def go():
    doc = SimpleDocTemplate("products.pdf")
    Catalog = []
    header = Paragraph("Product Inventory", styles['Heading1'])    
    Catalog.append(header)
    style = styles['Normal']
    for product in products:
        p = Paragraph("%s" % product['name'], style)
        Catalog.append(p)
        p = Paragraph("%s" % product['description'], style)        
        Catalog.append(p)
        s = Spacer(1, 0.25*inch)
        Catalog.append(s)
    doc.build(Catalog)

def gotable():
    doc = SimpleDocTemplate("products.pdf")
    Catalog = []
    header = Paragraph("Product Inventory", styles['Heading1'])    
    Catalog.append(header)
    style = styles['Normal']
    headings = ('Product Name', 'Product Description')
    allproducts = [ (p['name'], p['description']) for p in products]
    t = Table([headings] + allproducts)
    t.setStyle(TableStyle(
            [('GRID', (0,0), (1,-1), 2, colors.black),
             ('LINEBELOW', (0,0), (-1,0), 2, colors.red),
             ('BACKGROUND', (0, 0), (-1, 0), colors.pink)]))
    Catalog.append(t)
    doc.build(Catalog)    

sales = [ (23, 74, 93) ]
months = ['Oct', 'Nov', 'Dec']

def gochart():
    doc = SimpleDocTemplate("products.pdf")
    Catalog = []
    style = styles['Normal']
    p = Paragraph("Cranberry Sauce Sales", styles['Heading1'])
    Catalog.append(p)
    d = Drawing(100, 100)
    cht = HorizontalLineChart()
    cht.data = sales
    cht.categoryAxis.categoryNames = months
    d.add(cht)
    Catalog.append(d)
    doc.build(Catalog)

def gopie():
    doc = SimpleDocTemplate("products.pdf")
    Catalog = []
    style = styles['Normal']
    p = Paragraph("Cranberry Sauce Sales", styles['Heading1'])
    Catalog.append(p)
    d = Drawing(100, 125)
    cht = Pie()
    cht.data = sales[0]
    cht.labels = months
    cht.slices[0].popout = 10
    d.add(cht)
    Catalog.append(d)
    doc.build(Catalog)
gopie()
