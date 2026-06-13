"""
PDF Report Generator — RoadMate Pro
Generates a professional A4 trip report PDF using ReportLab.
"""

import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                 Paragraph, Spacer, HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime


# ── COLOUR PALETTE ──────────────────────────────────────────────────────────
BLUE       = colors.HexColor('#1a73e8')
DARK_BLUE  = colors.HexColor('#0d47a1')
GREEN      = colors.HexColor('#2e7d32')
LIGHT_BLUE = colors.HexColor('#e8f0fe')
LIGHT_GREY = colors.HexColor('#f5f7fb')
MID_GREY   = colors.HexColor('#e0e0e0')
WHITE      = colors.white
BLACK      = colors.HexColor('#212121')
ORANGE     = colors.HexColor('#f57c00')


def generate_pdf(trip, costs, user, resources=None):
    buffer = io.BytesIO()
    doc    = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=0.6*inch, bottomMargin=0.6*inch,
        leftMargin=0.7*inch, rightMargin=0.7*inch
    )

    styles = getSampleStyleSheet()
    elements = []

    # ── CUSTOM STYLES ───────────────────────────────────────────────────────
    title_style = ParagraphStyle('title', fontSize=22, textColor=WHITE,
                                  alignment=TA_CENTER, fontName='Helvetica-Bold',
                                  spaceAfter=4)
    sub_style   = ParagraphStyle('sub', fontSize=11, textColor=LIGHT_BLUE,
                                  alignment=TA_CENTER, fontName='Helvetica')
    h2_style    = ParagraphStyle('h2', fontSize=13, textColor=DARK_BLUE,
                                  fontName='Helvetica-Bold', spaceBefore=12, spaceAfter=6)
    normal      = ParagraphStyle('norm', fontSize=10, textColor=BLACK,
                                  fontName='Helvetica', spaceAfter=4)
    footer_style= ParagraphStyle('footer', fontSize=8, textColor=colors.grey,
                                  alignment=TA_CENTER)

    # ── HEADER BANNER ───────────────────────────────────────────────────────
    header_data = [[
        Paragraph('RoadMate Pro', title_style),
    ]]
    header_sub  = [[
        Paragraph('Intelligent Road Trip Planning &amp; Cost Optimization Report', sub_style),
    ]]
    banner = Table(header_data, colWidths=[7.1*inch])
    banner.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BLUE),
        ('TOPPADDING',    (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
        ('ROUNDEDCORNERS', [6]),
    ]))
    elements.append(banner)

    banner2 = Table(header_sub, colWidths=[7.1*inch])
    banner2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK_BLUE),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(banner2)
    elements.append(Spacer(1, 0.25*inch))

    # ── REPORT META ─────────────────────────────────────────────────────────
    meta_data = [
        ['Report ID', f"RPT-{trip['id'][:8].upper()}",
         'Traveler',  user['full_name']],
        ['Generated', datetime.utcnow().strftime('%d %b %Y, %H:%M UTC'),
         'Status',    trip.get('status','Planned').title()],
    ]
    meta_table = Table(meta_data, colWidths=[1.3*inch, 2.2*inch, 1.2*inch, 2.4*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (0,-1), LIGHT_BLUE),
        ('BACKGROUND',    (2,0), (2,-1), LIGHT_BLUE),
        ('FONTNAME',      (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME',      (2,0), (2,-1), 'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,-1), 9),
        ('GRID',          (0,0), (-1,-1), 0.5, MID_GREY),
        ('ROWBACKGROUNDS',(0,0), (-1,-1), [LIGHT_GREY, WHITE]),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 0.2*inch))

    # ── ROUTE DETAILS ───────────────────────────────────────────────────────
    elements.append(Paragraph('Route Details', h2_style))
    elements.append(HRFlowable(width='100%', thickness=1.5, color=BLUE))
    elements.append(Spacer(1, 0.1*inch))

    route_data = [
        ['FIELD', 'VALUE'],
        ['Source City',         trip['source']],
        ['Destination City',    trip['destination']],
        ['Total Distance',      f"{int(trip['distance_km'])} km"],
        ['Estimated Duration',  f"{trip['estimated_duration_hours']} hours"],
        ['Travel Days',         f"{trip['travel_days']} day(s)"],
        ['Hotel Nights',        f"{costs['nights']} night(s)"],
        ['Accommodation Band',  trip['accommodation_budget'].title()],
        ['Vehicle Mileage',     f"{trip['vehicle_mileage']} km/L"],
        ['Fuel Price',          f"Rs. {trip['fuel_price']}/L"],
    ]
    rt = Table(route_data, colWidths=[3*inch, 4.1*inch])
    rt.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0), BLUE),
        ('TEXTCOLOR',     (0,0), (-1,0), WHITE),
        ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,-1), 10),
        ('BACKGROUND',    (0,1), (0,-1), LIGHT_BLUE),
        ('FONTNAME',      (0,1), (0,-1), 'Helvetica-Bold'),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [WHITE, LIGHT_GREY]),
        ('GRID',          (0,0), (-1,-1), 0.5, MID_GREY),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
    ]))
    elements.append(rt)
    elements.append(Spacer(1, 0.2*inch))

    # ── COST BREAKDOWN ──────────────────────────────────────────────────────
    elements.append(Paragraph('Cost Breakdown', h2_style))
    elements.append(HRFlowable(width='100%', thickness=1.5, color=GREEN))
    elements.append(Spacer(1, 0.1*inch))

    cost_data = [
        ['COST ITEM', 'DETAILS', 'AMOUNT (INR)'],
        ['Fuel Required',
         f"{costs['fuel_required_liters']} L @ Rs.{trip['fuel_price']}/L",
         f"Rs. {costs['fuel_cost']:,.2f}"],
        ['Estimated Toll',
         f"Rs. {costs['toll_rate_per_km']}/km x {int(trip['distance_km'])} km",
         f"Rs. {costs['toll_cost']:,.2f}"],
        ['Accommodation',
         f"{costs['nights']} nights @ Rs. {costs['avg_price_per_night']:,.0f}/night",
         f"Rs. {costs['accommodation_cost']:,.2f}"],
        ['TOTAL TRIP COST', '', f"Rs. {costs['total_cost']:,.2f}"],
        ['Cost per KM',     '', f"Rs. {costs['cost_per_km']}"],
    ]
    ct = Table(cost_data, colWidths=[2.2*inch, 3*inch, 1.9*inch])
    ct.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0), GREEN),
        ('TEXTCOLOR',     (0,0), (-1,0), WHITE),
        ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME',      (0,-2), (-1,-2), 'Helvetica-Bold'),
        ('BACKGROUND',    (0,-2), (-1,-2), colors.HexColor('#e8f5e9')),
        ('FONTSIZE',      (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS',(0,1), (-1,-3), [WHITE, LIGHT_GREY]),
        ('GRID',          (0,0), (-1,-1), 0.5, MID_GREY),
        ('ALIGN',         (2,0), (2,-1), 'RIGHT'),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
    ]))
    elements.append(ct)
    elements.append(Spacer(1, 0.2*inch))

    # ── COST DISTRIBUTION BAR ───────────────────────────────────────────────
    elements.append(Paragraph('Cost Distribution', h2_style))
    elements.append(HRFlowable(width='100%', thickness=1.5, color=ORANGE))
    elements.append(Spacer(1, 0.1*inch))

    total = costs['total_cost']
    def pct(v): return round(v / total * 100, 1) if total else 0

    dist_data = [
        ['CATEGORY', 'AMOUNT', 'PERCENTAGE', 'VISUAL'],
        ['Fuel', f"Rs. {costs['fuel_cost']:,.0f}",
         f"{pct(costs['fuel_cost'])}%",
         '█' * int(pct(costs['fuel_cost']) / 5)],
        ['Tolls', f"Rs. {costs['toll_cost']:,.0f}",
         f"{pct(costs['toll_cost'])}%",
         '█' * int(pct(costs['toll_cost']) / 5)],
        ['Accommodation', f"Rs. {costs['accommodation_cost']:,.0f}",
         f"{pct(costs['accommodation_cost'])}%",
         '█' * int(pct(costs['accommodation_cost']) / 5)],
    ]
    dt = Table(dist_data, colWidths=[1.8*inch, 1.6*inch, 1.2*inch, 2.5*inch])
    dt.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0), ORANGE),
        ('TEXTCOLOR',     (0,0), (-1,0), WHITE),
        ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [WHITE, LIGHT_GREY]),
        ('GRID',          (0,0), (-1,-1), 0.5, MID_GREY),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('TEXTCOLOR',     (3,1), (3,1), BLUE),
        ('TEXTCOLOR',     (3,2), (3,2), colors.HexColor('#c62828')),
        ('TEXTCOLOR',     (3,3), (3,3), GREEN),
    ]))
    elements.append(dt)
    elements.append(Spacer(1, 0.2*inch))

    # ── RESOURCES SUMMARY ───────────────────────────────────────────────────
    if resources:
        elements.append(Paragraph('Route Resources Summary', h2_style))
        elements.append(HRFlowable(width='100%', thickness=1.5, color=colors.HexColor('#7b1fa2')))
        elements.append(Spacer(1, 0.1*inch))
        res_data = [
            ['RESOURCE TYPE', 'COUNT FOUND'],
            ['Fuel Stations',     str(resources['counts'].get('fuel_station', 0))],
            ['Hotels / Accommodation', str(resources['counts'].get('hotel', 0))],
            ['Emergency Services', str(resources['counts'].get('emergency', 0))],
            ['Rest Stops',        str(resources['counts'].get('rest_stop', 0))],
            ['TOTAL',             str(len(resources.get('all', [])))],
        ]
        rst = Table(res_data, colWidths=[4.5*inch, 2.6*inch])
        rst.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (-1,0), colors.HexColor('#7b1fa2')),
            ('TEXTCOLOR',     (0,0), (-1,0), WHITE),
            ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTNAME',      (0,-1), (-1,-1), 'Helvetica-Bold'),
            ('BACKGROUND',    (0,-1), (-1,-1), colors.HexColor('#f3e5f5')),
            ('FONTSIZE',      (0,0), (-1,-1), 10),
            ('ROWBACKGROUNDS',(0,1), (-1,-2), [WHITE, LIGHT_GREY]),
            ('GRID',          (0,0), (-1,-1), 0.5, MID_GREY),
            ('ALIGN',         (1,0), (1,-1), 'CENTER'),
            ('TOPPADDING',    (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ]))
        elements.append(rst)
        elements.append(Spacer(1, 0.2*inch))

    # ── FOOTER ──────────────────────────────────────────────────────────────
    elements.append(Spacer(1, 0.15*inch))
    elements.append(HRFlowable(width='100%', thickness=1, color=MID_GREY))
    elements.append(Spacer(1, 0.05*inch))
    elements.append(Paragraph(
        f'Generated by RoadMate Pro | {datetime.utcnow().strftime("%d %b %Y")} | '
        f'Traveler: {user["full_name"]} | This is a cost estimate only.',
        footer_style
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer
