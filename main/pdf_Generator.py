import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg


def write_to_pdf(plot_x, plot_y):

    fig = plt.figure(figsize=(5, 4))
    plt.plot(plot_x, plot_y)

    plt.xlabel("Attempts")
    plt.ylabel("Faults ")
    plt.title("Faults caught in time")

    plt.grid(True)
    # plt.show()
    imgdata = BytesIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)  # rewind the data

    drawing = svg2rlg(imgdata)

    c = canvas.Canvas('test2.pdf')
    renderPDF.draw(drawing, c, 10, 40)

    c.showPage()
    print("pdf created!")
    c.save()


