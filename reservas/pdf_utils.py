"""
Generacion de PDF de reservas usando solo la libreria estandar + HTML.
Usamos el enfoque de generar HTML y convertirlo con weasyprint si esta disponible,
o alternativamente generamos un PDF manual con reportlab si esta disponible,
o finalmente un HTML descargable como fallback.
"""

import io
from datetime import date
from django.http import HttpResponse


def generar_pdf_reservas(reservas, titulo="Reporte de Reservas"):
    """
    Genera un PDF con las reservas. Intenta weasyprint → reportlab → HTML fallback.
    """
    try:
        return _pdf_con_reportlab(reservas, titulo)
    except ImportError:
        pass
    return _html_fallback(reservas, titulo)


# ── ReportLab (pip install reportlab) ──
def _pdf_con_reportlab(reservas, titulo):
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4),
                            rightMargin=1.5*cm, leftMargin=1.5*cm,
                            topMargin=1.5*cm, bottomMargin=1.5*cm)

    styles = getSampleStyleSheet()
    VERDE = colors.HexColor('#1a7a4a')
    VERDE_CLARO = colors.HexColor('#e8f5ee')
    GRIS = colors.HexColor('#f4f6f8')
    NEGRO = colors.HexColor('#0d1117')

    titulo_style = ParagraphStyle('titulo', fontSize=22, textColor=VERDE,
                                  fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=4)
    sub_style = ParagraphStyle('sub', fontSize=10, textColor=colors.HexColor('#8b949e'),
                               fontName='Helvetica', alignment=TA_CENTER, spaceAfter=16)

    elementos = [
        Paragraph("CanchasSport", titulo_style),
        Paragraph(titulo, sub_style),
        Paragraph(f"Generado el {date.today().strftime('%d/%m/%Y')} &nbsp;|&nbsp; Total: {reservas.count()} reservas", sub_style),
        HRFlowable(width="100%", thickness=2, color=VERDE, spaceAfter=16),
    ]

    # Tabla
    encabezados = ['#', 'Cliente', 'Cancha', 'Tipo', 'Fecha', 'Hora inicio', 'Hora fin', 'Estado', 'Precio/h']
    filas = [encabezados]
    for i, r in enumerate(reservas, 1):
        estado_map = {'pendiente': 'Pendiente', 'confirmada': 'Confirmada', 'cancelada': 'Cancelada'}
        filas.append([
            str(i),
            r.usuario.get_full_name() or r.usuario.username,
            r.cancha.nombre,
            r.cancha.get_tipo_display(),
            r.fecha.strftime('%d/%m/%Y'),
            r.hora_inicio.strftime('%H:%M'),
            r.hora_fin.strftime('%H:%M'),
            estado_map.get(r.estado, r.estado),
            f"${r.cancha.precio_hora:,.0f}",
        ])

    col_widths = [1*cm, 4*cm, 4*cm, 3*cm, 3*cm, 2.5*cm, 2.5*cm, 2.8*cm, 3*cm]
    tabla = Table(filas, colWidths=col_widths, repeatRows=1)
    tabla.setStyle(TableStyle([
        ('BACKGROUND',   (0, 0), (-1, 0), VERDE),
        ('TEXTCOLOR',    (0, 0), (-1, 0), colors.white),
        ('FONTNAME',     (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',     (0, 0), (-1, 0), 9),
        ('ALIGN',        (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN',       (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, GRIS]),
        ('FONTSIZE',     (0, 1), (-1, -1), 8.5),
        ('FONTNAME',     (0, 1), (-1, -1), 'Helvetica'),
        ('GRID',         (0, 0), (-1, -1), 0.4, colors.HexColor('#d0d7de')),
        ('ROWHEIGHT',    (0, 0), (-1, -1), 22),
        ('TOPPADDING',   (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 5),
        # Color por estado
        *[('TEXTCOLOR', (7, i+1), (7, i+1),
           colors.HexColor('#166534') if r.estado == 'confirmada'
           else colors.HexColor('#991b1b') if r.estado == 'cancelada'
           else colors.HexColor('#92400e'))
          for i, r in enumerate(reservas)],
        *[('FONTNAME', (7, i+1), (7, i+1), 'Helvetica-Bold') for i in range(reservas.count())],
    ]))
    elementos.append(tabla)

    # Footer
    elementos.append(Spacer(1, 20))
    elementos.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#d0d7de')))
    elementos.append(Paragraph("CanchasSport — Sistema de Reservas Deportivas", sub_style))

    doc.build(elementos)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reservas_{date.today()}.pdf"'
    return response





# ── HTML fallback (descarga HTML si no hay PDF lib) ──
def _html_fallback(reservas, titulo):
    html = _generar_html_tabla(reservas, titulo)
    response = HttpResponse(html, content_type='text/html; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="reservas_{date.today()}.html"'
    return response


def _generar_html_tabla(reservas, titulo):
    filas = ""
    for i, r in enumerate(reservas, 1):
        color = '#166534' if r.estado == 'confirmada' else '#991b1b' if r.estado == 'cancelada' else '#92400e'
        bg = '#f0fff4' if r.estado == 'confirmada' else '#fff5f5' if r.estado == 'cancelada' else '#fffbeb'
        filas += f"""
        <tr>
          <td>{i}</td>
          <td>{r.usuario.get_full_name() or r.usuario.username}</td>
          <td>{r.cancha.nombre}</td>
          <td>{r.cancha.get_tipo_display()}</td>
          <td>{r.fecha.strftime('%d/%m/%Y')}</td>
          <td>{r.hora_inicio.strftime('%H:%M')}</td>
          <td>{r.hora_fin.strftime('%H:%M')}</td>
          <td style="color:{color};background:{bg};font-weight:700;">{r.get_estado_display()}</td>
          <td>${r.cancha.precio_hora:,.0f}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>{titulo}</title>
<style>
  body {{ font-family: Arial, sans-serif; margin: 32px; color: #0d1117; }}
  h1 {{ color: #1a7a4a; text-align: center; margin-bottom: 4px; }}
  p.sub {{ text-align: center; color: #8b949e; font-size: 13px; margin-bottom: 24px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  thead {{ background: #1a7a4a; color: #fff; }}
  th, td {{ padding: 10px 12px; border: 1px solid #d0d7de; text-align: center; }}
  tbody tr:nth-child(even) {{ background: #f4f6f8; }}
  .footer {{ text-align: center; color: #8b949e; font-size: 11px; margin-top: 24px; }}
</style>
</head>
<body>
  <h1>CanchasSport</h1>
  <p class="sub">{titulo} — {date.today().strftime('%d/%m/%Y')} — Total: {reservas.count()} reservas</p>
  <table>
    <thead>
      <tr><th>#</th><th>Cliente</th><th>Cancha</th><th>Tipo</th><th>Fecha</th>
          <th>Inicio</th><th>Fin</th><th>Estado</th><th>Precio/h</th></tr>
    </thead>
    <tbody>{filas}</tbody>
  </table>
  <p class="footer">CanchasSport — Sistema de Reservas Deportivas</p>
</body>
</html>"""
