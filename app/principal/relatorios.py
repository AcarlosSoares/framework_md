from flask import render_template, make_response


# pip install reportlab
def imprimir_reportlab(titulo, subtitulo, lista, result):

  from reportlab.pdfgen import canvas
  from reportlab.lib.pagesizes import A4
  from io import BytesIO

  pagina = 1
  margem_direita = 50
  tamanho_pagina = 770

  # # # CONFIGURAÇÕES DO RELATÓRIO
  output = BytesIO()
  p = canvas.Canvas(output, pagesize=A4)
  p.setLineWidth(.3)
  p.setFont('Helvetica', 12)
  # width, height = A4
  # print("Largura= ",width,"  Altura= ", height)

  # # # IMPRIME TÍTULO
  if titulo:
    y = tamanho_pagina
    p.setFont('Helvetica-Bold', 20)
    p.drawString(margem_direita, y, titulo)

  # # # IMPRIME SUB-TÍTULO
  if subtitulo:
    y = y - 25
    p.setFont('Helvetica-Bold', 16)
    p.drawString(margem_direita, y, subtitulo)

  # # # IMPRIME CABEÇALHO
  y = y - 30
  p.setFont('Helvetica-Bold', 12)
  for i in range(len(lista)):
    linha = ('p.drawString(' + str(lista[i][2]) + ', ' + str(y) + ', "' + lista[i][0] + '")')
    exec(linha)

  # # # IMPRIME TRAÇOS
  for i in range(len(lista)):
    linha = ('p.line(' + str(lista[i][2]) + ', ' + str(y-3) + ', ' + str(lista[i][3]) + ', ' + str(y-3) + ')')
    exec(linha)

  # # # IMPRIME DETALHE
  p.setFont('Helvetica', 12)
  for row in result:

    # QUEBRA DE PÁGINA
    if y < 70:
      # IMPRIME TRAÇO
      linha = ('p.line(' + str(margem_direita) + ', ' + str(y-10) + ', ' + str(lista[i][3]) + ', ' + str(y-10) + ')')
      exec(linha)
      # IMPRIME NÚMERO DA PAGINA
      linha = ('p.drawString(' + str(margem_direita) + ', ' + str(y-30) + ', "Pag. ' + str(pagina) + '")')
      exec(linha)
      p.showPage() # Quebra de página
      pagina += 1
      # IMPRIME TÍTULO
      y = tamanho_pagina
      p.setFont('Helvetica', 20)
      p.drawString(margem_direita, y, titulo)
      # IMPRIME CABEÇALHO
      y = y - 30
      p.setFont('Helvetica', 12)
      for i in range(len(lista)):
        linha = ('p.drawString(' + str(lista[i][2]) + ', ' + str(y) + ', "' + lista[i][0] + '")')
        exec(linha)
      # IMPRIME TRAÇOS
      for i in range(len(lista)):
        linha = ('p.line(' + str(lista[i][2]) + ', ' + str(y-3) + ', ' + str(lista[i][3]) + ', ' + str(y-3) + ')')
        exec(linha)

    y = y - 20
    # IMPRIME DETALHE
    for i in range(len(lista)):
      linha = ('p.drawString(' + str(lista[i][2]) + ', ' + str(y) + ', str(' + lista[i][1] + '))')
      exec(linha)

  # # # ÚLTIMA PÁGINA
  # IMPRIME TRAÇO
  linha = ('p.line(' + str(margem_direita) + ', ' + str(y-10) + ', ' + str(lista[i][3]) + ', ' + str(y-10) + ')')
  exec(linha)

  # IMPRIME NÚMERO DA PAGINA
  linha = ('p.drawString(' + str(margem_direita) + ', ' + str(y-30) + ', "Pag. ' + str(pagina) + '")')
  exec(linha)

  # # # GRAVA RELATÓRIO
  p.showPage()
  p.save()
  pdf_out = output.getvalue()
  output.close()

  # # # APRESENTA RELATÓRIO
  response = make_response(pdf_out)
  response.headers['Content-Disposition'] = 'attachment; filename=relatorio.pdf' # inline
  response.mimetype = 'application/pdf'

  return response


# pip install pdfkit
# precisar instalar: wkhtmltopdf - open source (LGPLv3) command line tools to render HTML into PDF
def imprimir_pdfkit(titulo, lista, result):

  import pdfkit

  # relatorio = render_template('relatorio.html', title='Lista de Modelos', dados=dados)
  # pdf = pdfkit.from_string(relatorio, False)
  # response = make_response(pdf)
  # response.headers['Content-Type'] = 'application/pdf'
  # # response.headers['Content-Disposition'] = 'inline; filename=relatoio.pdf'
  # response.headers['Content-Disposition'] = 'attachment; filename=relatoio.pdf'
  # return response

  return render_template('relatorio.html', title='Lista de Modelos', dados=result)


# pip install Flask-WeasyPrint
# pip install WeasyPrint
def imprimir_weasyprint(titulo, lista, result):

  from weasyprint import HTML

  # relatorio = render_template('relatorio.html', title='Lista de Modelos', dados=dados)
  # pdf = pdfkit.from_string(relatorio, False)
  # response = make_response(pdf)
  # response.headers['Content-Type'] = 'application/pdf'
  # # response.headers['Content-Disposition'] = 'inline; filename=relatoio.pdf'
  # response.headers['Content-Disposition'] = 'attachment; filename=relatoio.pdf'
  # return response

  html =  render_template('relatorio.html', title='Lista de Modelos', dados=result)
  return render_pdf(HTML(string=html))


# pip install xhtml2pdf
def imprimir_xhtml2pdf(titulo, lista, result):

  from xhtml2pdf import pisa
  from io import StringIO

  html =  render_template('relatorio.html', title='Lista de Modelos', dados=result)

  pdf = StringIO()
  pisa.CreatePDF(StringIO(html.encode('utf-8')), pdf)
  # response = make_response(pdf.getvalue())
  # response.headers['Content-Type'] = 'application/pdf'
  # response.headers['Content-Disposition'] = 'attachment; filename=relatoio.pdf'
  # pdf.close()
  # return response
  return html
