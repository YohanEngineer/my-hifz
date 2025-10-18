"""
Service layer for PDF generation.
Creates formatted PDF schedules for memorization plans.
"""

from io import BytesIO
from typing import List, Dict
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

from app.models import PlanningSettings
from app.config import logger


class PDFService:
    """Service for generating PDF documents."""

    def __init__(self):
        """Initialize PDF service and register Arabic font."""
        # Register Arabic font (using a font that supports Arabic)
        # Note: ReportLab includes some basic fonts, but for production,
        # you should include a proper Arabic font file
        self.has_arabic_font = self._register_arabic_font()

    def _register_arabic_font(self) -> bool:
        """
        Register an Arabic font if available.

        Returns:
            True if Arabic font was registered successfully
        """
        try:
            # Try to use a system Arabic font
            # For production, include a TTF file like "NotoNaskhArabic-Regular.ttf"
            # For now, we'll use ReportLab's built-in Helvetica which has limited Arabic support
            logger.info("Using built-in font for Arabic (limited support)")
            return False
        except Exception as e:
            logger.warning(f"Could not register Arabic font: {e}")
            return False

    def generate_schedule_pdf(
        self,
        settings: PlanningSettings,
        schedule: List[Dict]
    ) -> BytesIO:
        """
        Generate a PDF document for the memorization schedule.

        Args:
            settings: Planning settings used to generate the schedule
            schedule: List of period schedules

        Returns:
            BytesIO buffer containing the PDF document
        """
        logger.info("Generating PDF schedule")

        # Create buffer
        buffer = BytesIO()

        # Create PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.75*inch,
            bottomMargin=0.5*inch
        )

        # Build content
        elements = []
        styles = getSampleStyleSheet()

        # Add header
        elements.extend(self._create_header(settings, styles))

        # Add spacing
        elements.append(Spacer(1, 0.3*inch))

        # Add schedule table
        elements.append(self._create_schedule_table(schedule))

        # Build PDF
        doc.build(elements)

        # Reset buffer position
        buffer.seek(0)

        logger.info(f"PDF generated successfully ({len(schedule)} periods)")
        return buffer

    def _create_header(self, settings: PlanningSettings, styles) -> List:
        """
        Create the PDF header with user settings.

        Args:
            settings: Planning settings
            styles: ReportLab styles

        Returns:
            List of header elements
        """
        elements = []

        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=12,
            alignment=TA_CENTER
        )
        elements.append(Paragraph("Hifz Memorization Schedule", title_style))

        # Settings info
        info_style = ParagraphStyle(
            'InfoStyle',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=6
        )

        settings_info = [
            f"<b>Pace:</b> {settings.pages_per_period} pages per {settings.period_type.lower()}",
            f"<b>Starting Page:</b> {settings.start_page}",
            f"<b>Order:</b> {settings.order}",
            f"<b>Total Periods:</b> Will be calculated"
        ]

        for info in settings_info:
            elements.append(Paragraph(info, info_style))

        return elements

    def _create_schedule_table(self, schedule: List[Dict]) -> Table:
        """
        Create the schedule table.

        Args:
            schedule: List of period schedules

        Returns:
            Table object
        """
        # Prepare table data
        data = [
            ['Period', 'Pages', 'Surahs (Arabic)', 'Juz']
        ]

        for period in schedule:
            # Format surahs - use Arabic names
            surahs_text = ', '.join(period['surahs_ar'])

            # Format juzs
            juzs_text = ', '.join(map(str, period['juzs']))

            data.append([
                period['period_label'],
                period['page_range'],
                surahs_text,
                juzs_text
            ])

        # Create table
        table = Table(data, colWidths=[1*inch, 1*inch, 3.5*inch, 1*inch])

        # Style the table
        table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

            # Data rows
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (1, -1), 'CENTER'),  # Period and Pages columns centered
            ('ALIGN', (3, 1), (3, -1), 'CENTER'),  # Juz column centered
            ('ALIGN', (2, 1), (2, -1), 'RIGHT'),   # Arabic column right-aligned
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),

            # Grid
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),

            # Alternating row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))

        return table


# Global service instance
pdf_service = PDFService()
