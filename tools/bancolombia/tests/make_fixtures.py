"""Generate SYNTHETIC Bancolombia-like statements for tests (no real data).

Run directly to write the fixtures somewhere for manual inspection:
    python tests/make_fixtures.py /tmp/fixtures
"""
from __future__ import annotations

import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

DUMMY_PASSWORD = "test123"


def _text_page(path: Path, lines: list[str], font_size: int = 9) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setFont("Helvetica", font_size)
    y = letter[1] - 50
    for line in lines:
        if line == "<PAGEBREAK>":
            c.showPage()
            c.setFont("Helvetica", font_size)
            y = letter[1] - 50
            continue
        c.drawString(40, y, line)
        y -= font_size + 5
    c.save()


def savings_table_pdf(path: Path) -> Path:
    """Savings statement, US number format, ruled movement table, period crossing a year."""
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setFont("Helvetica", 10)
    header = [
        "BANCOLOMBIA S.A.",
        "ESTADO DE CUENTA - CUENTA DE AHORROS",
        "Número de cuenta: *****6948",
        "DESDE: 2025/11/01 HASTA: 2026/01/31",
        "RESUMEN",
        "SALDO ANTERIOR $ 1,000,000.00",
        "TOTAL ABONOS $ 2,500,012.34",
        "TOTAL CARGOS $ 1,550,000.50",
        "SALDO ACTUAL $ 1,950,011.84",
    ]
    y = letter[1] - 50
    for line in header:
        c.drawString(40, y, line)
        y -= 15
    data = [
        ["FECHA", "DESCRIPCIÓN", "SUCURSAL", "DCTO.", "VALOR", "SALDO"],
        ["5/11", "ABONO TRANSFERENCIA DESDE WALLBIT", "", "", "2,500,000.00", "3,500,000.00"],
        ["20/11", "COMPRA EN SUPERMERCADO", "BOGOTA", "1001", "-150,000.50", "3,349,999.50"],
        ["15/12", "PAGO TARJETA VISA", "", "", "-1,200,000.00", "2,149,999.50"],
        ["31/12", "ABONO INTERESES AHORROS", "", "", "12.34", "2,150,011.84"],
        ["05/01", "RETIRO CAJERO", "CHAPINERO", "2002", "-200,000.00", "1,950,011.84"],
    ]
    table = Table(data)
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
    ]))
    w, h = table.wrapOn(c, 520, 400)
    table.drawOn(c, 40, y - h - 10)
    c.save()
    return path


def savings_text_pdf(path: Path) -> Path:
    """Savings statement, Colombian number format, no ruled table (regex fallback)."""
    _text_page(path, [
        "BANCOLOMBIA",
        "ESTADO DE CUENTA",
        "CUENTA DE AHORROS",
        "Número de cuenta: *****6948",
        "DESDE: 01/04/2025 HASTA: 30/06/2025",
        "SALDO ANTERIOR $ 500.000,00",
        "TOTAL ABONOS $ 1.000.000,00",
        "TOTAL CARGOS $ 250.000,00",
        "SALDO ACTUAL $ 1.250.000,00",
        "FECHA DESCRIPCIÓN SUCURSAL DCTO. VALOR SALDO",
        "10/04 TRANSFERENCIA DESDE PAYONEER 1.000.000,00 1.500.000,00",
        "15/05 COMPRA POS TIENDA 4521 -250.000,00 1.250.000,00",
        "20/06 LINEA RARA SIN FORMATO 12.000,00 XX",
    ])
    return path


def visa_text_pdf(path: Path) -> Path:
    """Credit card statement with a pesos section and a dollars section."""
    _text_page(path, [
        "BANCOLOMBIA",
        "TARJETA DE CRÉDITO VISA",
        "Número de tarjeta: **** **** **** 7380",
        "Periodo facturado desde 16/01/2025 hasta 15/02/2025",
        "PESOS",
        "SALDO ANTERIOR $ 2,000,000.00",
        "COMPRAS DEL MES $ 1,450,000.00",
        "PAGOS Y ABONOS $ 2,000,000.00",
        "SALDO TOTAL $ 1,485,000.00",
        "PAGO MINIMO $ 385,000.00",
        "AUTORIZACION FECHA DESCRIPCION VALOR ORIGINAL TASA PACTADA TASA EA CARGOS Y ABONOS SALDO A DIFERIR CUOTAS",
        "123456 20/01/2025 RESTAURANTE CREPES 250,000.00 0.0000% 0.0000% 250,000.00 0.00 1/1",
        "234567 25/01/2025 ALMACEN ELECTRO 1,200,000.00 1.8900% 25.1200% 100,000.00 1,100,000.00 1/12",
        "05/02/2025 ABONO SUCURSAL VIRTUAL PSE -2,000,000.00",
        "15/02/2025 INTERESES CORRIENTES 35,000.00",
        "<PAGEBREAK>",
        "DOLARES",
        "SALDO ANTERIOR $ 0.00",
        "SALDO TOTAL $ 25.50",
        "345678 01/02/2025 NETFLIX.COM 25.50 0.0000% 0.0000% 25.50 0.00 1/1",
    ])
    return path


def encrypt(src: Path, dst: Path, password: str = DUMMY_PASSWORD) -> Path:
    import pikepdf

    with pikepdf.open(src) as pdf:
        pdf.save(dst, encryption=pikepdf.Encryption(user=password, owner=password))
    return dst


def build_all(folder: Path) -> dict[str, Path]:
    """Write the fixture set into `folder` using Bancolombia-style filenames."""
    folder.mkdir(parents=True, exist_ok=True)
    plain = folder / "_plain_savings.pdf.tmp"
    savings_table_pdf(plain)
    files = {
        "savings_table": encrypt(plain, folder / "2026-01_Bancolombia_CuentaAhorros_6948.pdf"),
        "savings_text": savings_text_pdf(folder / "2025-06_Bancolombia_Extracto_6948.pdf"),
        "visa": visa_text_pdf(folder / "2025-02_Bancolombia_Visa_7380.pdf"),
    }
    plain.unlink()
    return files


if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "fixtures")
    for name, p in build_all(out).items():
        print(name, p)
