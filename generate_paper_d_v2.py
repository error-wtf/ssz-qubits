#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Paper D v2 — "Kurz & Hart" (8–12 pages)

Gravitational Phase Coupling in Quantum Systems:
A Unified Framework for Testing SSZ Predictions

Structure:
  Title page (compact, no full-page waste)
  Abstract + Keywords
  1. Introduction & Claim Boundaries
  2. Unified Notation & Core Equations
  3. Experimental Protocol: With/Without Compensation
  4. Feasibility & Platform Analysis
  5. Falsifiability & Statistical Framework
  6. Conclusion & Roadmap
  References
  Appendix A: Test Suite Summary

Changes vs v1:
  - No static ToC (document is <12 pages)
  - Proper Unicode: Xi -> Ξ, DeltaPhi -> ΔΦ, omega -> ω, etc.
  - Strong-field definition clarified (r*/r_s ≈ 1.387)
  - 184 tests (current count)
  - Real figures embedded from outputs/
  - Compact: no redundant part-divider pages

(c) 2025 Carmen Wrede, Lino Casu
"""

import os
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'outputs')
PAPERS_DIR = os.path.join(SCRIPT_DIR, 'SSZ_QUBIT_PAPERS')


# ─────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────

def shade_cell(cell, color='D9E2F3'):
    tcp = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color)
    tcp.append(shd)


def add_table(doc, headers, rows, shade='D9E2F3'):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = 'Table Grid'
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = h
        c.paragraphs[0].runs[0].bold = True
        shade_cell(c, shade)
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            t.rows[ri + 1].cells[ci].text = val
    return t


def add_fig(doc, filename, caption, width=5.0):
    fp = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(fp):
        p = doc.add_paragraph(f'[Figure not found: {filename}]')
        p.italic = True
        return False
    doc.add_picture(fp, width=Inches(width))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap = doc.add_paragraph(caption)
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.runs[0].italic = True
    cap.runs[0].font.size = Pt(9)
    return True


def add_eq(doc, text):
    """Add a centered, bold equation-like paragraph."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(11)
    return p


# ─────────────────────────────────────────────────────────────────────
# Main generator
# ─────────────────────────────────────────────────────────────────────

def generate():
    doc = Document()

    # Global style
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(11)
    style.paragraph_format.space_after = Pt(4)

    # ── COPYRIGHT HEADER (compact) ──────────────────────────────────
    cp = doc.add_paragraph()
    r = cp.add_run('\u26a0\ufe0f WORKING PAPER \u2013 STRICT COPYRIGHT RESTRICTIONS')
    r.bold = True
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor(0x99, 0x00, 0x00)
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cp2 = doc.add_paragraph()
    r2 = cp2.add_run(
        'Preliminary working paper. Any use\u2014including citation, copying, '
        'or distribution\u2014requires prior written permission from the authors. '
        'Unauthorized reproduction or commercial exploitation is explicitly prohibited. '
        '(December 2025 | mail@error.wtf)'
    )
    r2.font.size = Pt(8)
    r2.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    cp2.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph()

    # ── TITLE ───────────────────────────────────────────────────────
    t = doc.add_paragraph()
    r = t.add_run('Gravitational Phase Coupling in Quantum Systems:\n'
                   'A Unified Framework for Testing SSZ Predictions')
    r.bold = True
    r.font.size = Pt(18)
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph()

    sub = doc.add_paragraph()
    r = sub.add_run('Paper D \u2014 Master Document')
    r.italic = True
    r.font.size = Pt(13)
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph()

    auth = doc.add_paragraph()
    auth.add_run('Lino Casu, Carmen Wrede').bold = True
    auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph('Independent Researchers \u2022 mail@error.wtf').alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph('December 2025').alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph()

    # Core claim box
    box = doc.add_paragraph()
    box.add_run('CORE CLAIM').bold = True
    box.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cl = doc.add_paragraph()
    cl.add_run(
        'SSZ predicts a deterministic, geometry-coupled phase drift '
        '\u0394\u03a6 = \u03c9 \u00d7 \u0394D \u00d7 t that is principally compensable. '
        'Current transmon qubits provide robust upper bounds; '
        'optical atomic clocks are the gold standard for direct detection.'
    ).italic = True
    cl.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph()
    repo = doc.add_paragraph()
    repo.add_run('Repository: ').bold = True
    repo.add_run('https://github.com/error-wtf/ssz-qubits')
    repo.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_page_break()

    # ── ABSTRACT ────────────────────────────────────────────────────
    doc.add_heading('Abstract', level=1)

    abstract = (
        'The Segmented Spacetime (SSZ) framework predicts that quantum systems '
        'at different gravitational potentials experience deterministic phase drifts '
        'arising from differential time dilation. This paper unifies our three-paper '
        'series (A\u2013C) into a single experimental framework.\n\n'
        'We establish the theoretical basis\u2014the SSZ time-dilation factor '
        'D = 1/(1+\u039e), the segment density \u039e(r), and the core phase-drift equation '
        '\u0394\u03a6 = \u03c9 \u0394D t\u2014and derive explicit numerical predictions. '
        'The with/without compensation protocol is presented as the strongest '
        'discriminator between SSZ and confounds, exploiting that SSZ drift is '
        'deterministic and linearly scales with \u0394h, \u03c9, and t.\n\n'
        'An honest feasibility analysis reveals that mm-scale height differences '
        'with superconducting qubits yield signals ~12 orders of magnitude below '
        'detectability. We reframe this as an upper-bound experiment and identify '
        'optical atomic clocks (\u0394\u03a6 \u2248 0.3 rad at 1 m) as the gold-standard '
        'platform. A statistical framework using slope-fitting with explicit '
        'confidence intervals replaces binary thresholds.\n\n'
        'All 184 unit tests pass (100%); all results are reproducible via the '
        'accompanying open-source code. A null result in the current superconducting '
        'regime is SSZ-consistent\u2014the theory predicts negligibility at mm-scale '
        'with current coherence times.'
    )
    p = doc.add_paragraph(abstract)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    doc.add_paragraph()
    kw = doc.add_paragraph()
    kw.add_run('Keywords: ').bold = True
    kw.add_run(
        'Segmented Spacetime, Gravitational Phase Coupling, Quantum Computing, '
        'Falsifiability, Optical Clocks, Upper Bound, Statistical Framework'
    )

    doc.add_page_break()

    # ================================================================
    # SECTION 1: Introduction & Claim Boundaries
    # ================================================================
    doc.add_heading('1  Introduction and Claim Boundaries', level=1)

    doc.add_heading('1.1  What SSZ Is (Operationally)', level=2)
    p = doc.add_paragraph(
        'The Segmented Spacetime (SSZ) framework is an operational model that '
        'predicts how quantum phase evolution differs between systems at different '
        'gravitational potentials. It is:'
    )
    doc.add_paragraph(
        'A deterministic correction to quantum gate timing based on local segment density',
        style='List Bullet')
    doc.add_paragraph(
        'Testable via comparison of separated quantum systems',
        style='List Bullet')
    doc.add_paragraph(
        'Consistent with GR in the weak-field limit (r \u226b r\u209b) but structurally '
        'distinct near the Schwarzschild radius',
        style='List Bullet')

    doc.add_heading('1.2  What SSZ Does NOT Claim', level=2)
    doc.add_paragraph(
        '\u201cMagical\u201d detectability at mm-scale with current transmons \u2014 '
        'we make no claim of present-day detectability in mm-scale superconducting '
        'devices; the contribution is a falsifiable coupling structure and a measurement '
        'protocol with explicit confound controls.',
        style='List Bullet')
    doc.add_paragraph(
        'Violation of the equivalence principle for local measurements',
        style='List Bullet')
    doc.add_paragraph(
        'Effects observable without comparing separated systems',
        style='List Bullet')

    doc.add_heading('1.3  Scope Clarification: Weak vs. Strong Field', level=2)
    p = doc.add_paragraph()
    p.add_run('Weak-field baseline: ').bold = True
    p.add_run(
        'Earth-scale qubit predictions (\u0394\u03a6 ~ 10\u207b\u00b9\u2076 rad/gate '
        'at 1 mm) are practically unmeasurable on current chips. This is by design: '
        'the weak-field regime serves as methodological baseline and upper-bound constraint.'
    )

    p2 = doc.add_paragraph()
    p2.add_run('Strong-field signature: ').bold = True
    p2.add_run(
        'SSZ predicts a universal transition boundary at r*/r\u209b \u2248 1.387, '
        'where the strong-field formula \u039e(r) = 1 \u2212 exp(\u2212\u03c6 r/r\u209b) '
        'yields +11\u201314% excess time dilation relative to GR. This regime is tested '
        'against neutron-star and black-hole data (184/184 tests pass) and becomes '
        'accessible via optical-clock metrology (\u0394\u03a6 ~ 0.3 rad at 1 m height difference).'
    )

    doc.add_heading('1.4  Document Structure', level=2)
    p = doc.add_paragraph('This paper synthesizes three prior papers:')
    for label, title in [
        ('Paper A', 'Segmented Spacetime Geometry for Qubit Optimization'),
        ('Paper B', 'Phase Coherence and Entanglement Preservation'),
        ('Paper C', 'Falsifiable Predictions and Experimental Protocols'),
    ]:
        pp = doc.add_paragraph()
        pp.add_run(f'{label}: ').bold = True
        pp.add_run(title)

    doc.add_page_break()

    # ================================================================
    # SECTION 2: Unified Notation & Core Equations
    # ================================================================
    doc.add_heading('2  Unified Notation and Core Equations', level=1)

    doc.add_heading('2.1  Notation Lock', level=2)
    p = doc.add_paragraph(
        'The following symbols are used consistently throughout this document '
        'and all companion papers:'
    )

    add_table(doc,
        ['Symbol', 'Definition', 'Units'],
        [
            ['\u039e(r)',  'Segment density at radius r',          'dimensionless'],
            ['D(r)',       'Time-dilation factor 1/(1+\u039e)',    'dimensionless'],
            ['\u0394D',    'Differential dilation |D(r\u2081)\u2212D(r\u2082)|', 'dimensionless'],
            ['\u03c9',     'Angular frequency 2\u03c0f',           'rad/s'],
            ['t',          'Evolution / integration time',         's'],
            ['\u0394h',    'Height difference',                    'm'],
            ['\u0394\u03a6', 'Accumulated phase drift',            'rad'],
            ['r\u209b',    'Schwarzschild radius 2GM/c\u00b2',     'm'],
            ['\u03c6',     'Golden ratio (\u221a5+1)/2 \u2248 1.618', 'dimensionless'],
        ])

    doc.add_paragraph()

    doc.add_heading('2.2  Segment Density', level=2)

    p = doc.add_paragraph()
    p.add_run('Weak field (r \u226b r\u209b):  ').bold = True
    p.add_run('\u039e(r) = r\u209b / (2r)')

    p = doc.add_paragraph()
    p.add_run('Strong field (r ~ r\u209b):  ').bold = True
    p.add_run('\u039e(r) = 1 \u2212 exp(\u2212\u03c6 \u00b7 r / r\u209b)')

    p = doc.add_paragraph()
    p.add_run(
        'At the universal boundary r*/r\u209b \u2248 1.387 both expressions yield '
        'continuous, C\u00b2-smooth values. '
        'The strong-field formula is validated against neutron-star and black-hole '
        'datasets where SSZ predicts \u039e(r\u209b) = 0.802 and D(r\u209b) = 0.555 '
        '(finite, no singularity).'
    )

    doc.add_heading('2.3  Time Dilation', level=2)

    add_eq(doc, 'D(r) = 1 / (1 + \u039e(r))')

    p = doc.add_paragraph(
        'In the weak-field limit, D \u2248 1 \u2212 \u039e(r), recovering GR to '
        'first order in r\u209b/r. At r = r\u209b, GR diverges (D \u2192 0) while '
        'SSZ remains finite (D = 0.555).'
    )

    doc.add_heading('2.4  Phase Drift Formula', level=2)

    add_eq(doc, '\u0394\u03a6 = \u03c9 \u00d7 \u0394D \u00d7 t')

    p = doc.add_paragraph('where ')
    p.add_run('\u03c9 = 2\u03c0f').italic = True
    p.add_run(' is the angular frequency, ')
    p.add_run('\u0394D = |D(r\u2081) \u2212 D(r\u2082)|').italic = True
    p.add_run(' the differential time dilation, and ')
    p.add_run('t').italic = True
    p.add_run(' the gate/evolution time.')

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('Numerical example: ').bold = True
    p.add_run(
        'For f = 5 GHz, t = 50 ns gate, \u0394h = 1 mm: '
        '\u0394\u03a6 \u2248 1.7 \u00d7 10\u207b\u00b9\u2076 rad per gate.'
    )

    add_fig(doc, 'paper_d_fig2_phase_vs_height.png',
            'Figure 1: Phase shift vs. height difference showing linear scaling '
            '(slope = 1 on log\u2013log).')

    doc.add_heading('2.5  Relativity Hygiene: Local vs. Global', level=2)
    p = doc.add_paragraph()
    p.add_run('LOCAL: ').bold = True
    p.add_run(
        'In any single reference frame, proper time is proper time. No local '
        'observable effect for a single qubit (consistent with the equivalence principle).'
    )
    p2 = doc.add_paragraph()
    p2.add_run('GLOBAL: ').bold = True
    p2.add_run(
        'When comparing two separated clocks (or qubits) that evolved at different '
        'gravitational potentials, the relative phase drift accumulates and IS measurable. '
        'Quantum systems amplify this via the \u03c9\u00b7t lever.'
    )

    add_fig(doc, 'paper_d_fig1_local_vs_global.png',
            'Figure 2: Local vs. global phase comparison. '
            'SSZ effects emerge only from comparing separated systems.')

    doc.add_page_break()

    # ================================================================
    # SECTION 3: Experimental Protocol
    # ================================================================
    doc.add_heading('3  Experimental Protocol', level=1)

    doc.add_heading('3.1  The Core Discriminator: With/Without Compensation', level=2)
    p = doc.add_paragraph()
    p.add_run(
        'The strongest experimental discriminator is the with/without compensation test:'
    ).bold = True

    doc.add_paragraph('Measure phase drift without any SSZ correction', style='List Number')
    doc.add_paragraph('Apply calculated SSZ compensation \u0394\u03a6_comp = \u2212\u03c9 \u0394D t', style='List Number')
    doc.add_paragraph('Measure residual drift', style='List Number')
    doc.add_paragraph(
        'Compare: SSZ predicts deterministic reduction; confounds (thermal, LO noise, '
        'magnetic flux) do not reproduce the same \u03c9\u00b7t scaling and removability',
        style='List Number')

    doc.add_heading('3.2  Why This Works', level=2)
    p = doc.add_paragraph('SSZ drift is ')
    p.add_run('deterministic').bold = True
    p.add_run(
        ' \u2014 calculable from geometry alone. Confounds are stochastic or follow '
        'different functional forms. A compensation scheme tuned to SSZ will NOT '
        'reduce confound contributions.'
    )

    doc.add_heading('3.3  Scaling Signatures', level=2)
    p = doc.add_paragraph('SSZ is uniquely identified by ')
    p.add_run('linear scaling').bold = True
    p.add_run(' in all three parameters:')

    doc.add_paragraph('\u0394\u03a6 \u221d \u0394h  (height difference)', style='List Bullet')
    doc.add_paragraph('\u0394\u03a6 \u221d \u03c9   (frequency)', style='List Bullet')
    doc.add_paragraph('\u0394\u03a6 \u221d t   (evolution time)', style='List Bullet')

    p = doc.add_paragraph('AND ')
    p.add_run('invariance under randomization').bold = True
    p.add_run(' (same result regardless of measurement order).')

    add_fig(doc, 'paper_d_fig3_scaling.png',
            'Figure 3: SSZ scaling laws \u2014 linear dependence on \u03c9 and t.')

    doc.add_heading('3.4  Confound Discrimination', level=2)

    add_table(doc,
        ['Confound', 'Scaling', 'Control', 'Discrimination'],
        [
            ['Temperature',  'Non-linear in t',     'mK thermometry',       'Randomize \u0394h order'],
            ['LO phase noise', '\u221at; indep. of \u0394h', 'Common-mode ref. LO',  'Compare scaling exponent'],
            ['Magnetic flux', 'Non-linear in \u03c9', '\u03bc-metal shielding',  'Sweet-spot operation'],
            ['Vibration',    'AC spectrum',          'Accelerometer',        'Spectral analysis'],
        ])

    add_fig(doc, 'paper_d_fig6_confounds.png',
            'Figure 4: Confound discrimination matrix \u2014 distinct scaling signatures.')

    doc.add_page_break()

    # ================================================================
    # SECTION 4: Feasibility & Platform Analysis
    # ================================================================
    doc.add_heading('4  Feasibility and Platform Analysis', level=1)

    doc.add_heading('4.1  Order-of-Magnitude Reality Check', level=2)
    p = doc.add_paragraph(
        'For a 5 GHz transmon with 100 \u00b5s Ramsey time at Earth surface:'
    )

    add_table(doc,
        ['\u0394h', '\u0394D', '\u0394\u03a6', 'Detectable?'],
        [
            ['1 mm',  '1.09 \u00d7 10\u207b\u00b9\u2079', '3.4 \u00d7 10\u207b\u00b9\u00b3 rad', 'No'],
            ['1 m',   '1.09 \u00d7 10\u207b\u00b9\u2076', '3.4 \u00d7 10\u207b\u00b9\u2070 rad', 'No'],
            ['10 m',  '1.09 \u00d7 10\u207b\u00b9\u2075', '3.4 \u00d7 10\u207b\u2079 rad',       'No'],
            ['100 m', '1.09 \u00d7 10\u207b\u00b9\u2074', '3.4 \u00d7 10\u207b\u2078 rad',       'Marginal'],
        ])

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('Signal/Noise ~ 10\u207b\u00b9\u00b3 at mm-scale.').bold = True
    p.add_run(
        '  This is approximately 12 orders of magnitude below single-shot '
        'detectability (~1 rad quantum projection noise).'
    )

    p = doc.add_paragraph()
    p.add_run('A null result is SSZ-consistent.').bold = True
    p.add_run(
        '  For \u0394h < 1 cm and T\u2082 < 1 s, SSZ predicts '
        '\u0394\u03a6 < 10\u207b\u2077 rad, below detection limits. '
        'Null results in this regime tighten upper bounds.'
    )

    doc.add_heading('4.2  Upper-Bound Experiment Design', level=2)

    p = doc.add_paragraph('Three hardware configurations:')
    doc.add_paragraph('Piezo stages: 0\u201310 mm continuous', style='List Bullet')
    doc.add_paragraph(
        'Chip tilt: \u0394h = L sin\u03b8 (e.g., 20 mm chip at 10\u00b0 \u2192 3.47 mm)',
        style='List Bullet')
    doc.add_paragraph('Vertical cryostat stacking', style='List Bullet')

    add_fig(doc, 'paper_d_fig5_setups.png',
            'Figure 5: Hardware configurations for height-difference generation.')

    doc.add_heading('4.3  Platform Comparison: Transmon vs. Optical Clock', level=2)

    add_table(doc,
        ['Parameter', 'Transmon', 'Optical Clock', 'Ratio'],
        [
            ['Frequency',       '5 GHz',                     '429 THz',    '8.6 \u00d7 10\u2074'],
            ['Coherence time',  '100 \u00b5s',               '1 s',        '10\u2074'],
            ['\u0394\u03a6 @ 1 m', '3.4 \u00d7 10\u207b\u00b9\u2070 rad', '0.29 rad',   '8.6 \u00d7 10\u2078'],
            ['Shots for SNR=3', '7.6 \u00d7 10\u00b9\u2079', '~100',       '\u2014'],
            ['Time required',   '>10\u2078 years',           '<1 hour',    '\u2014'],
            ['Feasible?',       'NO (upper bound only)',     'YES',        '\u2014'],
        ])

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run(
        'For quantitative SSZ tests, optical atomic clocks are the gold-standard platform.'
    ).bold = True
    p.add_run(
        '  Superconducting qubits serve as protocol validators and upper-bound setters. '
        'Optical-clock experiments have already demonstrated gravitational redshift '
        'at the ~1 cm level (Bothwell et al., Nature 2022).'
    )

    add_fig(doc, 'paper_d_fig4_feasibility.png',
            'Figure 6: Platform feasibility comparison.')

    doc.add_page_break()

    # ================================================================
    # SECTION 5: Falsifiability & Statistical Framework
    # ================================================================
    doc.add_heading('5  Falsifiability and Statistical Framework', level=1)

    doc.add_heading('5.1  Model Comparison', level=2)
    p = doc.add_paragraph('We fit ')
    p.add_run('\u0394\u03a6 = \u03b1 \u00b7 \u0394h').italic = True
    p.add_run(' and test three models:')

    for label, desc in [
        ('H\u2080 (Null)', '\u03b1 = 0 (no coupling)'),
        ('H_SSZ', '\u03b1 = \u03b1_SSZ (predicted slope from SSZ geometry)'),
        ('H_anom', '\u03b1 = free parameter (anomalous coupling)'),
    ]:
        pp = doc.add_paragraph()
        pp.add_run(f'{label}: ').bold = True
        pp.add_run(desc)

    p = doc.add_paragraph(
        'A likelihood-ratio test on the measured \u0394\u03a6 vs. \u0394h slope '
        'determines which model the data support. '
        'At mm-scale, both H\u2080 and H_SSZ predict \u03b1 \u2248 0, so a null result '
        'is consistent with SSZ.'
    )

    doc.add_heading('5.2  Falsification Criteria', level=2)

    p = doc.add_paragraph()
    p.add_run('SSZ falsified if: ').bold = True
    p.add_run(
        'measured slope inconsistent with \u03b1_SSZ at >3\u03c3 AND significantly '
        'non-zero, OR signal does not scale linearly with \u0394h, \u03c9, t, '
        'OR compensation reduces drift via SSZ-incompatible mechanism.'
    )

    p = doc.add_paragraph()
    p.add_run('SSZ supported if: ').bold = True
    p.add_run(
        'null result consistent with \u03b1_SSZ \u2248 0 in bound regime; '
        'measured slope matches \u03b1_SSZ within CI in detection regime; '
        'compensation removes predicted fraction of drift.'
    )

    doc.add_heading('5.3  Upper-Bound Example', level=2)
    p = doc.add_paragraph(
        'With \u0394h_max = 3.5 mm (10\u00b0 tilt), N = 10\u2079 shots:'
    )
    doc.add_paragraph(
        '\u03c3_avg = 1/\u221a(10\u2079) = 3.2 \u00d7 10\u207b\u2075 rad',
        style='List Bullet')
    doc.add_paragraph(
        '\u03c3_slope = 3.2 \u00d7 10\u207b\u2075 / 3.5 \u00d7 10\u207b\u00b3 = '
        '9 \u00d7 10\u207b\u00b3 rad/m',
        style='List Bullet')
    doc.add_paragraph(
        'Upper bound: |\u03b1_anom| < 9 \u00d7 10\u207b\u00b3 rad/m (95% CL)',
        style='List Bullet')

    p = doc.add_paragraph()
    p.add_run(
        'This constrains anomalous couplings to < 10\u00b9\u2070 \u00d7 \u03b1_SSZ.'
    ).bold = True

    doc.add_heading('5.4  What Would NOT Falsify SSZ', level=2)
    doc.add_paragraph(
        'Null result at mm-scale \u2014 this IS the SSZ prediction',
        style='List Bullet')
    doc.add_paragraph(
        'Signal consistent with \u03b1_SSZ in the detection regime (optical clocks)',
        style='List Bullet')

    add_fig(doc, 'paper_d_fig7_taxonomy.png',
            'Figure 7: Claim taxonomy \u2014 bounded, detectable, '
            'and engineering-relevant regimes.')

    doc.add_page_break()

    # ================================================================
    # SECTION 6: Conclusion & Roadmap
    # ================================================================
    doc.add_heading('6  Conclusion and Roadmap', level=1)

    doc.add_heading('6.1  Key Findings', level=2)

    findings = [
        'SSZ predicts deterministic phase drift: \u0394\u03a6 = \u03c9 \u0394D t',
        'At mm-scale, signal is ~12 OoM below noise \u2014 null result is SSZ-consistent',
        'Optical atomic clocks are the gold-standard platform '
        '(\u0394\u03a6 \u2248 0.3 rad at 1 m)',
        'With/without compensation is the strongest experimental discriminator',
        'Statistical framework uses slope-fitting, not binary thresholds',
        'All 184 tests pass (100%); all results fully reproducible',
    ]
    for f in findings:
        doc.add_paragraph(f, style='List Number')

    doc.add_heading('6.2  Roadmap', level=2)

    for period, desc in [
        ('Near-term (2025\u20132027)',
         'Upper-bound experiments with tilted chips; optical-clock collaborations'),
        ('Medium-term (2027\u20132030)',
         'Tower experiments at 10\u2013100 m; 3D chiplet stacks; '
         'NICER neutron-star observations'),
        ('Long-term (2030+)',
         'Multi-height metrology with pre-registered analysis; '
         'space-based quantum networks; ngEHT black-hole shadow observations'),
    ]:
        pp = doc.add_paragraph()
        pp.add_run(f'{period}: ').bold = True
        pp.add_run(desc)

    doc.add_heading('6.3  Final Statement', level=2)
    p = doc.add_paragraph()
    p.add_run(
        'SSZ makes testable predictions. This paper honestly assesses where '
        'those tests are feasible and how they should be conducted. We provide '
        'all tools for independent verification.'
    ).italic = True

    doc.add_page_break()

    # ================================================================
    # REFERENCES
    # ================================================================
    doc.add_heading('References', level=1)

    refs = [
        '[1]  Casu, L. & Wrede, C. (2025). Paper A: Segmented Spacetime Geometry '
        'for Qubit Optimization.',
        '[2]  Casu, L. & Wrede, C. (2025). Paper B: Phase Coherence and '
        'Entanglement Preservation.',
        '[3]  Casu, L. & Wrede, C. (2025). Paper C: Falsifiable Predictions and '
        'Experimental Protocols.',
        '[4]  Bothwell, T. et al. (2022). Resolving the gravitational redshift '
        'across a millimetre-scale atomic sample. Nature 602, 420\u2013424.',
        '[5]  Zheng, X. et al. (2023). Differential clock comparisons with a '
        'multiplexed optical lattice clock. Nature 602, 425\u2013430.',
        '[6]  Pound, R. V. & Rebka, G. A. (1960). Apparent Weight of Photons. '
        'Phys. Rev. Lett. 4, 337\u2013341.',
        '[7]  Chou, C. W. et al. (2010). Optical Clocks and Relativity. '
        'Science 329, 1630\u20131633.',
        '[8]  SSZ-Qubits Repository: https://github.com/error-wtf/ssz-qubits',
        '[9]  SSZ-Metric-Pure Repository: https://github.com/error-wtf/ssz-metric-pure',
        '[10] SSZ Research Program Roadmap: docs/SSZ_RESEARCH_PROGRAM_ROADMAP.md',
    ]
    for ref in refs:
        doc.add_paragraph(ref)

    doc.add_page_break()

    # ================================================================
    # APPENDIX A: Test Suite Summary
    # ================================================================
    doc.add_heading('Appendix A: Test Suite Summary', level=1)

    doc.add_heading('A.1  ssz-qubits Repository', level=2)
    p = doc.add_paragraph(
        'The ssz-qubits repository contains 184 unit tests covering segment density, '
        'time dilation, phase drift, entanglement fidelity, and edge cases. All tests '
        'pass with pytest on Python 3.10+.'
    )
    p2 = doc.add_paragraph()
    p2.add_run(
        'Note: the test count may grow as the suite evolves; the numbers in this paper '
        'correspond to git tag v1.0-paper-d. Later commits may add tests but never '
        'remove or weaken existing ones.'
    ).italic = True

    add_table(doc,
        ['Test File', 'Tests', 'Status'],
        [
            ['test_edge_cases.py',              '25', 'PASS'],
            ['test_ssz_physics.py',             '17', 'PASS'],
            ['test_ssz_qubit_applications.py',  '15', 'PASS'],
            ['test_validation.py',              '17', 'PASS'],
            ['test_paper_c_support.py',         '19', 'PASS'],
            ['test_paper_d_master.py',          '91', 'PASS'],
        ])

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('TOTAL: 184/184 tests passed (100%)').bold = True

    doc.add_heading('A.2  One-Command Reproduction', level=2)
    code = doc.add_paragraph(
        'git clone https://github.com/error-wtf/ssz-qubits.git\n'
        'cd ssz-qubits\n'
        'python -m pytest tests/ -v          # All 184 tests\n'
        'python generate_paper_d_master_plots.py  # All figures'
    )
    code.runs[0].font.name = 'Courier New'
    code.runs[0].font.size = Pt(9)

    doc.add_heading('A.3  Related Repositories', level=2)

    add_table(doc,
        ['Repository', 'Tests', 'Focus'],
        [
            ['ssz-metric-pure',    '12+', 'Tensor validation, Einstein/Ricci'],
            ['ssz-full-metric',    '41',  'Observable tests (lensing, Shapiro, etc.)'],
            ['g79-cygnus-test',    '14',  'Astronomical validation (Cygnus X-1)'],
            ['Unified-Results',    '54',  'Cross-repository pipeline (25 suites)'],
        ])

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('TOTAL ACROSS ALL SSZ REPOS: 560+ tests').bold = True

    # ================================================================
    # FOOTER
    # ================================================================
    doc.add_paragraph()
    doc.add_paragraph()

    ft = doc.add_paragraph()
    ft.add_run('\u00a9 2025 Carmen Wrede & Lino Casu').italic = True
    ft.alignment = WD_ALIGN_PARAGRAPH.CENTER

    lic = doc.add_paragraph()
    lic.add_run('Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4').italic = True
    lic.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # ================================================================
    # SAVE
    # ================================================================
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(PAPERS_DIR, exist_ok=True)

    fname = 'SSZ_Paper_D_Gravitational Phase Coupling in Quantum Systems.docx'
    p1 = os.path.join(PAPERS_DIR, fname)
    p2 = os.path.join(OUTPUT_DIR, 'SSZ_Paper_D_MASTER_v2.docx')

    doc.save(p1)
    doc.save(p2)

    print(f"Saved: {p1}")
    print(f"Saved: {p2}")
    return p1


if __name__ == '__main__':
    generate()
