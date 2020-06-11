import os
from fpdf import FPDF
from video_analyze import videoAnalyze
from extract_text import languageDetect, extractAudio
from text_analyze import *


def createReport(path, title, lang):
    va = videoAnalyze(path)
    et = extractAudio(path, lang)
    ts = textSentiment(et)

    ct = cleanText(et)
    fw = freqWords(ct)

    preprocessing(et)
    pp = preprocessingPhrases(et)
    cd = createDict(pp)
    cc = createCorpus(cd, pp)
    try:
        th = extractThemes(cc, cd)

    except Exception as e:
        print(e)

    wimage = 120
    ximage = 105 - (wimage / 2)

    loc = path.split('/')[-1][:-4]
    frame = f'..\\output\\frames\\{loc}\\frame.jpg'

    pdf = FPDF('P', 'mm', 'A4')

    pdf.add_page()
    pdf.set_margins(left=12, top=12, right=12)

    pdf.set_font('Arial', 'B', size=16)
    pdf.multi_cell(
        190, 8, txt=title, align='C')
    pdf.ln()
    pdf.image(frame, x=ximage, w=wimage)
    pdf.ln()
    pdf.image('..\\input\\icon\\woman.png', x=84, y=101, w=20)
    pdf.image('..\\input\\icon\\man.png', x=105, y=100, w=20)
    pdf.set_font('Arial', size=30)
    pdf.text(x=43, y=129, txt=str(va[0])+'%')
    pdf.text(x=130, y=129, txt=str(va[1])+'%')
    pdf.ln(42)
    pdf.set_font('Arial', 'B', size=16)
    pdf.cell(180, 8, txt='Diálogo')
    pdf.ln()
    pdf.set_font('Arial', size=12)
    pdf.multi_cell(180, 8, txt=et, align='L')
    pdf.ln()
    pdf.set_font('Arial', 'B', size=16)
    pdf.cell(180, 8, txt='Sentiment')
    pdf.ln()
    pdf.set_font('Arial', size=12)
    pdf.multi_cell(
        180, 8, txt=ts)
    pdf.ln()
    pdf.set_font('Arial', 'B', size=16)
    pdf.cell(180, 8, txt='Palabras más frecuentes')
    pdf.ln()
    pdf.set_font('Arial', size=12)
    pdf.multi_cell(
        180, 8, txt=fw)
    pdf.ln()
    pdf.set_font('Arial', 'B', size=16)
    pdf.cell(180, 8, txt='Temas principales')
    pdf.ln()
    pdf.set_font('Arial', size=12)
    pdf.multi_cell(180, 8, txt='th')  # CAMBIAR POR TEMA

    pdf.output(f'..\\output\\frames\\{loc}\\{title}.pdf')

    os.startfile(f'..\\output\\frames\\{loc}\\{title}.pdf')
