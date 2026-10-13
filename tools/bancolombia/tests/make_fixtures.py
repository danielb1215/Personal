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


def savings_real_layout_pdf(path: Path) -> Path:
    """Mimics the 2018-2026 savings layout: two-column RESUMEN, amounts like '.72' and '-.02'."""
    _text_page(path, [
        "ESTADO DE CUENTA",
        "DESDE: 2024/12/31 HASTA: 2025/03/31",
        "CUENTA DE AHORROS",
        "TITULAR DE PRUEBA",
        "NÚMERO 0000006948",
        "SUCURSAL VIRTUAL",
        "RESUMEN",
        "SALDO ANTERIOR $ 100,000.00 SALDO PROMEDIO $ 500,000",
        "TOTAL ABONOS $ 1,000,002.72 CUENTAS X COBRAR $ .00",
        "TOTAL CARGOS $ 300,000.02 VALOR INTERESES PAGADOS $ 2.72",
        "SALDO ACTUAL $ 800,002.70 RETEFUENTE $ .00",
        "FECHA DESCRIPCIÓN SUCURSAL DCTO. VALOR SALDO",
        "10/01 ABONO INTERESES AHORROS 2.00 100,002.00",
        "10/01 AJUSTE INTERES AHORROS DB -.02 100,001.98",
        "14/01 ABONO INTERESES AHORROS .72 100,002.70",
        "15/01 TRANSF INTERNACIONAL RECIBIDA 1,000,000.00 1,100,002.70",
        "1/02 PAGO PSE EMPRESA SERVICIOS -300,000.00 800,002.70",
        "FIN ESTADO DE CUENTA",
        "PÁGINA: 1",
    ])
    return path


def savings_empty_pdf(path: Path) -> Path:
    """A savings statement with no movements (all balances '$ .00')."""
    _text_page(path, [
        "ESTADO DE CUENTA",
        "DESDE: 2018/06/30 HASTA: 2018/09/30",
        "CUENTA DE AHORROS",
        "NÚMERO 0000005446",
        "RESUMEN",
        "SALDO ANTERIOR $ .00 SALDO PROMEDIO $ 0",
        "TOTAL ABONOS $ .00 CUENTAS X COBRAR $ .00",
        "TOTAL CARGOS $ .00 VALOR INTERESES PAGADOS $ .00",
        "SALDO ACTUAL $ .00 RETEFUENTE $ .00",
        "FECHA DESCRIPCIÓN SUCURSAL DCTO. VALOR SALDO",
        "FIN ESTADO DE CUENTA",
    ])
    return path


def _card_page(currency: str, last4: str, summary: list[str], movements: list[str]) -> list[str]:
    return [
        f"CUPÓN DE PAGO EN: {currency}",
        f"TARJETA: ************{last4}",
        f"ESTADO DE CUENTA EN: {currency}",
        "Cupo Total Cupo de Avances Período Facturado",
        "$ 5,000,000.00 $ 5,000,000.00 Desde: 28/02/2021 Hasta: 30/03/2021",
        "Tasas de interés vigente Resumen Saldo Total Resumen Pago Mínimo",
        *summary,
        "Número de Fecha de Tasa Tasa EA",
        "Descripción Valor Original Cargos y Abonos Saldo a Diferir Cuotas",
        "Autorización Transacción Pactada Facturada",
        *movements,
        "Pag. 1 / 1",
    ]


def card_real_layout_pdf(path: Path, last4: str = "7380") -> Path:
    """Mimics the 2019-2021 card layout: DOLARES page then PESOS page, two-column summary,
    rates with decimal comma, credits with trailing minus, 'VR MONEDA ORIG' continuation."""
    usd = _card_page("DOLARES", last4, [
        "Saldo anterior 50.00 Saldo en mora 0.00",
        "M.V. E.A. + Compras del mes 120.00 + Cuota compras del mes 3.33",
        "Compra Internacional 1,2800 % 16,4888 % + Intereses corrientes 0.00 + Intereses corrientes 0.00",
        "- Pagos / abonos 50.00 + Cuota compras anteriores 0.00",
        "Saldo a favor 0.00 - Saldo a favor 0.00",
        "= Pagos total 120.00 = Pago mínimo 4.00",
    ], [
        "R00001 14/03/2021 ONLINE STORE US 120.00 1,2800 16,4888 3.33 116.67 1/36",
        "VR MONEDA ORIG 120.00 USD",
        "C00002 04/03/2021 ABONO SUCURSAL VIRTUAL 50.00- 50.00- 0.00",
    ])
    cop = _card_page("PESOS", last4, [
        "Saldo anterior 300,000.00 Saldo en mora 0.00",
        "M.V. E.A. + Compras del mes 150,100.00 + Cuota compras del mes 150,100.00",
        "Compra un mes 0,00 % 0,00 % + Intereses corrientes 33.23 + Intereses corrientes 33.23",
        "Avances 1,96 % 26,22 % - Pagos / abonos 300,000.00 + Cuota compras anteriores 10,000.00",
        "Mora 1,96 % 26,22 % Saldo a favor 0.00 - Saldo a favor 0.00",
        "= Pagos total 150,134.00 = Pago mínimo 160,134.00",
    ], [
        "30/03/2021 INTERESES CORRIENTES 33.23 33.23 0.00",
        "F00003 23/03/2021 RESTAURANTE PRUEBA 80,100.00 0,00 00,00 80,100.00 0.00 1/1",
        "R00004 09/03/2021 BOTON PAGO TELEFONIA 20,000.00 0,00 00,00 20,000.00 0.00 1/1",
        "F00005 02/03/2021 FARMACIA PRUEBA 50,000.00 0.00 0.00 1/1",
        "R00006 10/12/2020 GIMNASIO PRUEBA 120,000.00 1,28 16,48 10,000.00 90,000.00 4/12",
        "C00007 04/03/2021 ABONO SUCURSAL VIRTUAL 300,000.00- 300,000.00- 0.00",
    ])
    _text_page(path, usd + ["<PAGEBREAK>"] + cop)
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
        "savings_real": savings_real_layout_pdf(folder / "2025-03_Bancolombia_CuentaAhorros_6948.pdf"),
        "savings_empty": savings_empty_pdf(folder / "2018-09_Bancolombia_CuentaAhorros_5446.pdf"),
        # saved without type/last4, like 2021-07_Bancolombia_Extracto.pdf
        "card_real": card_real_layout_pdf(folder / "2021-03_Bancolombia_Extracto.pdf"),
    }
    plain.unlink()
    return files


if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "fixtures")
    for name, p in build_all(out).items():
        print(name, p)
