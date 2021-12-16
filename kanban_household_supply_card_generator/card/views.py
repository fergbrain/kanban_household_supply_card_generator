from django.shortcuts import render
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from django.core.files.images import get_image_dimensions
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Frame, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from .models import Item

stylesheet = getSampleStyleSheet()
normalStyle = stylesheet["Normal"]


def initiate_card() -> (canvas.Canvas, io.BytesIO):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    c = canvas.Canvas(filename=buffer, pagesize=(5 * inch, 3 * inch))

    return c, buffer


def generate_single_card(c, buffer, pk) -> (canvas.Canvas, io.BytesIO):
    item = Item.objects.get(id=pk)

    if item.supply_type == "EXTERNAL":
        background_color = colors.orange
    elif item.supply_type == "INTERNAL":
        background_color = colors.green
    else:
        background_color = colors.red

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    story = []

    TABLE_DEFAULT_STYLE = TableStyle(
        [
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("TOPPADDING", (0, 0), (-1, -1), 1),
            ("LEFTPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
        ]
    )

    p_header = Paragraph(
        """<para leading="30" textColor="white" alignment="center">KANBAN<font size='28'> EXTERNAL </font>SUPPLY</para>""",
        normalStyle,
    )
    t_header_data = [["{:05d}".format(item.id), p_header]]
    t_header = Table(
        t_header_data,
        colWidths=(1 * inch, 3.5 * inch),
        hAlign="LEFT",
        rowHeights=0.4 * inch,
        style=TABLE_DEFAULT_STYLE,
    )
    t_header.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (1, 0), (1, 0), background_color),
                ("TEXTCOLOR", (1, 0), (1, 0), colors.white),
                ("FONT", (0, 0), (0, 0), "Helvetica", 16),
                ("ALIGNMENT", (0, 0), (0, 0), "CENTER"),
                ("VALIGN", (0, 0), (0, 0), "MIDDLE"),
            ]
        )
    )
    story.append(t_header)

    if item.alt_source_ok:
        alt_src = " -&nbsp;ALT&nbsp;OK"
    else:
        alt_src = ""

    p_supply_item_name = Paragraph(item.name + alt_src)

    if item.alt_supplier_ok:
        alt_supp = " - ALT OK"
    else:
        alt_supp = ""

    t_item_data = [
        ["Item", p_supply_item_name],
    ]
    t_item = Table(
        t_item_data,
        colWidths=(0.6 * inch, 3.9 * inch),
        hAlign="LEFT",
        style=TABLE_DEFAULT_STYLE,
    )
    t_item.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), background_color),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
            ]
        )
    )
    story.append(t_item)

    t_supply_data = [
        ["Supplier", item.supplier.name + alt_supp],
    ]
    t_supply = Table(
        t_supply_data,
        colWidths=(0.6 * inch, 2.15 * inch),
        hAlign="LEFT",
        style=TABLE_DEFAULT_STYLE,
    )
    t_supply.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), background_color),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
            ]
        )
    )
    story.append(t_supply)

    if item.location is None:
        t_loc_data = [
            ["Location", "Rack"],
            ["TBD", "TBD"],
            ["", "Shelf"],
            ["", "TBD"],
        ]
    else:
        t_loc_data = [
            ["Location", "Rack", "Shelf"],
            [item.location.region, item.location.rack, item.location.shelf],
        ]
    t_loc = Table(
        t_loc_data,
        colWidths=(1.375 * inch, 0.6875 * inch, 0.6875 * inch),
        hAlign="LEFT",
        style=TABLE_DEFAULT_STYLE,
    )
    t_loc.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), background_color),
                # ('BACKGROUND', (1, 2), (1, 2), background_color),
                ("TEXTCOLOR", (1, 2), (1, 2), colors.white),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("VALIGN", (0, 1), (0, 1), "MIDDLE"),
                # ('SPAN', (0, 1), (0, 3)),
            ]
        )
    )
    story.append(t_loc)

    p_add_info = Paragraph(
        "<p>" + item.additional_information.replace("\n", "<br />") + "&nbsp;</p>"
    )

    t_add_info_data = [
        ["Additional Info"],
        [p_add_info],
    ]
    t_add_info = Table(
        t_add_info_data,
        colWidths=(2.75 * inch),
        hAlign="LEFT",
        style=TABLE_DEFAULT_STYLE,
    )
    t_add_info.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), background_color),
                ("TEXTCOLOR", (0, 0), (0, 0), colors.white),
                ("VALIGN", (0, 1), (0, 1), "TOP"),
            ]
        )
    )
    story.append(t_add_info)

    t_reorder_data = [
        ["Reorder At", "Reorder Quantity"],
        [
            str(item.reorder_at) + " " + item.reorder_units,
            str(item.reorder_qty) + " " + item.reorder_units,
        ],
    ]
    t_reorder = Table(
        t_reorder_data,
        colWidths=(1.375 * inch, 1.375 * inch),
        hAlign="LEFT",
        style=TABLE_DEFAULT_STYLE,
    )
    t_reorder.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (1, 0), background_color),
                ("TEXTCOLOR", (0, 0), (1, 0), colors.white),
            ]
        )
    )
    story.append(t_reorder)

    f = Frame(
        inch * 0.25,
        inch * 0.25,
        4.5 * inch,
        2.5 * inch,
        showBoundary=0,
        leftPadding=0,
        topPadding=0,
    )
    f.addFromList(story, c)

    img_w_orig, img_h_orig = get_image_dimensions(item.image.path)
    img_ratio = img_w_orig / img_h_orig

    max_size = 1.64 * inch

    if img_ratio > 1.0:
        h_img_ratio = 1 / img_ratio
        w_img_ratio = 1.0
        x_offset = 0.0
        y_offset = (max_size - (max_size * h_img_ratio)) / 2
    elif img_ratio < 1.0:
        h_img_ratio = 1.0
        w_img_ratio = img_ratio
        x_offset = (max_size - (max_size * w_img_ratio)) / 2
        y_offset = 0.0
    else:
        h_img_ratio = 1.0
        w_img_ratio = 1.0
        x_offset = 0.0
        y_offset = 0.0

    c.drawImage(
        item.image.path,
        x=(3.11 * inch) + x_offset,
        y=(0.34 * inch) + y_offset,
        width=max_size * w_img_ratio,
        height=max_size * h_img_ratio,
        showBoundary=0,
    )

    # Close the PDF object cleanly, and we're done.
    c.showPage()

    return c, buffer


def single_card(request, pk):

    item = Item.objects.get(id=pk)

    c, buffer = initiate_card()

    c.setTitle(
        "%s from %s"
        % (
            item.name,
            item.supplier.name,
        )
    )

    c, buffer = generate_single_card(c, buffer, pk)

    c.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(
        buffer,
        as_attachment=False,
        filename="%s_%s.pdf" % (item.supplier.name, item.name),
    )


def all_cards(request):
    items = Item.objects.all().order_by("pk")
    c, buffer = initiate_card()

    c.setTitle("All Cards")

    for item in items:
        c, buffer = generate_single_card(c, buffer, item.pk)

    c.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename="all_cards.pdf")


def initiate_shelf_label() -> (canvas.Canvas, io.BytesIO):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    c = canvas.Canvas(filename=buffer, pagesize=letter)

    return c, buffer


def all_shelf_labels(request):
    items = Item.objects.all()

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    c = canvas.Canvas(filename=buffer, pagesize=letter)
    c.setTitle("Shelf Labels")

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    story = []

    TABLE_DEFAULT_STYLE = TableStyle(
        [
            # ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]
    )

    labels = []

    for item in items:

        if item.supply_type == "EXTERNAL":
            background_color = colors.orange
        elif item.supply_type == "INTERNAL":
            background_color = colors.green
        else:
            background_color = colors.red

        img_w_orig, img_h_orig = get_image_dimensions(item.image.path)
        img_ratio = img_h_orig / img_w_orig

        if img_ratio < 1.0:
            h_img_ratio = img_ratio
            w_img_ratio = 1
        else:
            h_img_ratio = 1
            w_img_ratio = img_ratio

        image = Image(
            item.image.path,
            width=0.5 / w_img_ratio * inch,
            height=0.5 * h_img_ratio * inch,
        )
        t_shelf_data = [
            ["ITEM DESCRIPTION", image],
            [Paragraph("<para leading=10>" + item.name + "</para>"), ""],
            [
                item.location.region
                + "/Rack "
                + item.location.rack
                + "/Shelf "
                + item.location.shelf,
                "",
            ],
        ]
        t_shelf = Table(
            t_shelf_data,
            colWidths=(2 * inch, 0.5 * inch),
            hAlign="LEFT",
            rowHeights=(0.2 * inch, 0.4 * inch, 0.15 * inch),
            style=TABLE_DEFAULT_STYLE,
        )
        t_shelf.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, 0), background_color),
                    ("TEXTCOLOR", (0, 0), (0, 0), colors.white),
                    ("FONT", (0, 0), (0, 0), "Helvetica", 12),
                    ("FONT", (0, 2), (0, 2), "Helvetica", 6),
                    ("ALIGNMENT", (0, 0), (1, 0), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("SPAN", (1, 0), (-1, -1)),
                    ("LEFTPADDING", (1, 0), (1, 0), 0),
                    ("RIGHTPADDING", (1, 0), (1, -0), 0),
                ]
            )
        )
        labels.append(t_shelf)

    t_shelf_label_data = [labels[i : i + 3] for i in range(0, len(labels), 3)]

    t_shelf_label = Table(t_shelf_label_data, hAlign="LEFT", style=TABLE_DEFAULT_STYLE)
    t_shelf_label.setStyle(
        TableStyle(
            [
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(t_shelf_label)

    f = Frame(
        inch * 0.2,
        inch * 0.2,
        8.1 * inch,
        10.6 * inch,
        showBoundary=0,
        leftPadding=0,
        topPadding=0,
    )
    f.addFromList(story, c)

    c.showPage()
    c.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename="shelf_labels.pdf")
