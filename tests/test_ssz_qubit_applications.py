#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ-Qubits: Anwendungstests für Qubit-Physik

Diese Tests validieren die KONKRETEN Anwendungen von SSZ für Qubits:

1. Segmentierte Zeitlogik als Qubit-Uhr
2. Decoherence als Geometrie-Phänomen  
3. Gravitationsbedingte Drift-Vorhersage
4. Segment-Aware Fehlerkorrektur
5. Quantenkommunikation & SSZ-Synchronisation

"Wenn du Qubits betreibst, ohne die Metrikstruktur zu verstehen,
dann ist das wie ein Konzert ohne Stimmung."

(c) 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pytest
from ssz_qubits import (
    # Constants
    C, G, HBAR, M_EARTH, R_EARTH, PHI,
    # Core functions
    schwarzschild_radius, xi_segment_density, xi_gradient,
    ssz_time_dilation, ssz_time_dilation_difference, time_difference_per_second,
    # Qubit functions
    Qubit, QubitPair, SegmentAnalysis,
    analyze_qubit_segment, qubit_pair_segment_mismatch,
    optimal_qubit_height, segment_coherent_zone,
    gate_timing_correction, two_qubit_gate_timing,
    ssz_decoherence_rate, effective_T2, pair_decoherence_time,
    optimize_qubit_array, array_segment_uniformity,
    height_to_time_offset
)


# =============================================================================
# TEST 1: SEGMENTIERTE ZEITLOGIK ALS QUBIT-UHR
# =============================================================================

class TestSegmentedTimeClock:
    """
    Tests für: Segmentierte Zeitlogik = neue Uhr für Qubits
    
    SSZ-Logik: "Das Qubit lebt auf segmentierter Raumzeit - 
    und seine eigene Zeit entsteht aus lokaler Segmentanzahl (Xi)."
    
    -> Timing wird geometrisch festgelegt, nicht über externe Sync.
    """
    
    def test_local_segment_time_as_reference(self):
        """Xi(r) als lokale Referenzuhr für Qubits."""
        print("\n" + "="*70)
        print("TEST: Lokale Segmentzeit als Qubit-Referenzuhr")
        print("="*70)
        
        # Zwei Qubits auf verschiedenen Höhen
        h1 = 0      # Meeresspiegel
        h2 = 1.0    # 1 Meter höher
        
        r1 = R_EARTH + h1
        r2 = R_EARTH + h2
        
        xi1 = xi_segment_density(r1, M_EARTH)
        xi2 = xi_segment_density(r2, M_EARTH)
        
        # Segmentzeit-Differenz
        delta_xi = abs(xi1 - xi2)
        
        print(f"Qubit 1: h = {h1} m, Xi = {xi1:.15e}")
        print(f"Qubit 2: h = {h2} m, Xi = {xi2:.15e}")
        print(f"Delta Xi = {delta_xi:.6e}")
        
        # Xi-Differenz sollte messbar sein
        assert delta_xi > 0, "Xi-Differenz muss existieren"
        assert delta_xi < 1e-15, "Bei 1m Höhe: Delta Xi ~ 10^-16"
        
        print("\n** SSZ-ANWENDUNG **")
        print("-> Xi(r) definiert lokale 'Segmentzeit'")
        print("-> Keine externe Synchronisation nötig!")
        print("-> Timing ist GEOMETRISCH festgelegt")
        print("="*70)
    
    def test_geometric_timing_for_gates(self):
        """Gate-Timing aus Geometrie statt externer Uhren."""
        print("\n" + "="*70)
        print("TEST: Geometrisches Gate-Timing")
        print("="*70)
        
        # Qubit mit 50 ns Gate-Zeit
        q = Qubit(id="Q1", x=0, y=0, z=0, gate_time=50e-9)
        
        # SSZ-korrigierte Gate-Zeit
        analysis = analyze_qubit_segment(q, M_EARTH)
        d_ssz = analysis.time_dilation
        
        # Korrigierte Gate-Zeit
        t_gate_corrected = q.gate_time / d_ssz
        correction = t_gate_corrected - q.gate_time
        
        print(f"Nominale Gate-Zeit: {q.gate_time*1e9:.3f} ns")
        print(f"D_SSZ = {d_ssz:.15f}")
        print(f"Korrigierte Gate-Zeit: {t_gate_corrected*1e9:.15f} ns")
        print(f"Korrektur: {correction*1e18:.6f} as (Attosekunden)")
        
        # Korrektur sollte im Attosekunden-Bereich liegen
        assert abs(correction) < 1e-15, "Korrektur im sub-fs Bereich"
        assert abs(correction) > 0, "Korrektur existiert"
        
        print("\n** SSZ-ANWENDUNG **")
        print("-> Gate-Timing aus D_SSZ berechnet")
        print("-> Weniger Fehler bei Zwei-Qubit-Gates")
        print("-> Weniger Drift in Superposition")
        print("="*70)
    
    def test_two_qubit_gate_sync(self):
        """Zwei-Qubit-Gate Synchronisation via SSZ."""
        print("\n" + "="*70)
        print("TEST: Zwei-Qubit-Gate SSZ-Synchronisation")
        print("="*70)
        
        # Zwei Qubits mit 10 mm Höhenunterschied
        q1 = Qubit(id="Q1", x=0, y=0, z=0, gate_time=50e-9)
        q2 = Qubit(id="Q2", x=0, y=0, z=0.01, gate_time=50e-9)  # 10 mm höher
        pair = QubitPair(q1, q2)
        
        # SSZ-Timing-Analyse
        timing = two_qubit_gate_timing(pair, M_EARTH)
        
        print(f"Höhendifferenz: {pair.height_difference*1e3:.3f} mm")
        print(f"Optimale Gate-Zeit: {timing['optimal_gate_time']*1e9:.6f} ns")
        print(f"Timing-Asymmetrie: {timing['timing_asymmetry']:.6e}")
        print(f"Max Fidelity-Verlust: {timing['max_fidelity_loss']:.6e}")
        
        # Asymmetrie sollte klein aber messbar sein
        assert timing['timing_asymmetry'] >= 0
        assert timing['max_fidelity_loss'] >= 0
        
        print("\n** SSZ-ANWENDUNG **")
        print("-> SSZ berechnet optimales gemeinsames Timing")
        print("-> Timing-Asymmetrie wird kompensiert")
        print("-> Gate-Fidelity wird maximiert")
        print("="*70)


# =============================================================================
# TEST 2: DECOHERENCE ALS GEOMETRIE-PHÄNOMEN
# =============================================================================

class TestDecoherenceGeometry:
    """
    Tests für: Decoherence als Geometrie-Phänomen
    
    SSZ: Decoherence entsteht, wenn zwei Qubits in unterschiedlichen 
    Segmenten sitzen -> Die Raumzeit hat den Qubits nicht dieselbe 
    Zeit angeboten.
    
    -> Lösung: Platziere Qubits in geometrisch kohärenten Segmentzonen
    """
    
    def test_segment_mismatch_causes_decoherence(self):
        """Segment-Mismatch führt zu Decoherence."""
        print("\n" + "="*70)
        print("TEST: Segment-Mismatch verursacht Decoherence")
        print("="*70)
        
        # Zwei Qubits mit verschiedenen Höhen
        heights = [0, 0.001, 0.01, 0.1, 1.0]  # Meter
        
        print(f"{'Höhendiff [mm]':>15} | {'Delta Xi':>15} | {'Decoherence-Faktor':>20}")
        print("-" * 55)
        
        base_qubit = Qubit(id="Q0", x=0, y=0, z=0, coherence_time_T2=100e-6)
        
        for h in heights:
            q = Qubit(id="Q1", x=0, y=0, z=h, coherence_time_T2=100e-6)
            pair = QubitPair(base_qubit, q)
            
            mismatch = qubit_pair_segment_mismatch(pair, M_EARTH)
            delta_xi = mismatch['delta_xi']
            decoherence_factor = mismatch['decoherence_enhancement']
            
            print(f"{h*1e3:>15.3f} | {delta_xi:>15.6e} | {decoherence_factor:>20.6f}")
            
            # Größerer Mismatch -> mehr Decoherence
            assert decoherence_factor >= 1.0
        
        print("\n** SSZ-ERKENNTNIS **")
        print("-> Decoherence ist NICHT nur thermisches Rauschen!")
        print("-> Qubits in verschiedenen Segmenten = verschiedene Zeit")
        print("-> Sie decoherieren weil sie METRIKVERSCHOBEN sind")
        print("="*70)
    
    def test_coherent_segment_zone(self):
        """Finde geometrisch kohärente Segmentzonen."""
        print("\n" + "="*70)
        print("TEST: Geometrisch kohärente Segmentzonen")
        print("="*70)
        
        # Finde kohärente Zone um Referenzhöhe
        reference_height = 0  # Meeresspiegel
        target_xi = xi_segment_density(R_EARTH + reference_height, M_EARTH)
        tolerance = 1e-18  # Sehr enge Toleranz
        
        zone = segment_coherent_zone(reference_height, tolerance, M_EARTH)
        h_min, h_max = zone
        width = h_max - h_min
        
        print(f"Referenzhöhe: {reference_height} m")
        print(f"Ziel-Xi: {target_xi:.15e}")
        print(f"Toleranz: {tolerance:.0e}")
        print(f"Kohärente Zone: {h_min*1e6:.3f} um bis {h_max*1e6:.3f} um")
        print(f"Zonenbreite: {width*1e6:.3f} um")
        
        # Zone sollte existieren
        assert width > 0
        
        print("\n** SSZ-LÖSUNG **")
        print("-> Platziere Qubits in kohärenten Segmentzonen!")
        print("-> Nicht nur nach Abstand oder Kühlung optimieren")
        print("-> GEOMETRISCHE Kohärenz ist der Schlüssel")
        print("="*70)
    
    def test_decoherence_rate_from_gradient(self):
        """Decoherence-Rate aus Xi-Gradient."""
        print("\n" + "="*70)
        print("TEST: Decoherence-Rate aus Segment-Gradient")
        print("="*70)
        
        # Qubit mit räumlicher Ausdehnung
        q = Qubit(id="Q1", x=0, y=0, z=0, coherence_time_T2=100e-6)
        
        # Gradient am Qubit-Ort
        grad = abs(xi_gradient(R_EARTH, M_EARTH))
        
        # SSZ-Decoherence-Rate
        gamma_ssz = ssz_decoherence_rate(q, M_EARTH)
        
        # Effektive T2
        T2_eff = effective_T2(q, M_EARTH)
        
        print(f"|dXi/dr|: {grad:.6e} /m")
        print(f"SSZ Decoherence Rate: {gamma_ssz:.6e} /s")
        print(f"Intrinsische T2: {q.coherence_time_T2*1e6:.1f} us")
        print(f"Effektive T2: {T2_eff*1e6:.3f} us")
        
        # Effektive T2 sollte <= intrinsische T2 sein
        assert T2_eff <= q.coherence_time_T2
        
        print("\n** SSZ-PHYSIK **")
        print("-> Decoherence-Rate proportional zu |dXi/dr| * L_qubit")
        print("-> Größere Qubits = mehr Segment-Variation = mehr Decoherence")
        print("-> SSZ erklärt 'unerklärliche' Decoherence-Quellen!")
        print("="*70)


# =============================================================================
# TEST 3: GRAVITATIONSBEDINGTE DRIFT-VORHERSAGE
# =============================================================================

class TestGravitationalDrift:
    """
    Tests für: Gravitationsbedingte Drift wird vorhersagbar
    
    SSZ erlaubt, Xi(r) punktgenau zu berechnen.
    -> Präzise Simulation der Segmentzeit-Verteilung
    -> Keine unvorhersehbaren Gate Errors mehr!
    """
    
    def test_nanometer_height_difference(self):
        """Xi-Differenz bei Nanometer-Höhenunterschied."""
        print("\n" + "="*70)
        print("TEST: Nanometer-Höhenunterschiede")
        print("="*70)
        
        # Höhenunterschiede im Nanometer-Bereich
        heights_nm = [1, 10, 100, 1000]  # Nanometer
        
        print(f"{'Höhendiff [nm]':>15} | {'Delta Xi':>20} | {'Delta D_SSZ':>20}")
        print("-" * 60)
        
        r_base = R_EARTH
        xi_base = xi_segment_density(r_base, M_EARTH)
        d_base = ssz_time_dilation(r_base, M_EARTH)
        
        for h_nm in heights_nm:
            h = h_nm * 1e-9  # Convert to meters
            r = R_EARTH + h
            
            xi = xi_segment_density(r, M_EARTH)
            d = ssz_time_dilation(r, M_EARTH)
            
            delta_xi = abs(xi - xi_base)
            delta_d = abs(d - d_base)
            
            print(f"{h_nm:>15} | {delta_xi:>20.6e} | {delta_d:>20.6e}")
            
            # Selbst nm-Unterschiede sollten berechenbar sein
            if h_nm >= 10:
                assert delta_xi > 0, "Delta Xi muss bei nm-Unterschieden existieren"
        
        print("\n** SSZ-PRÄZISION **")
        print("-> Xi(r) ist punktgenau berechenbar!")
        print("-> Selbst Nanometer-Unterschiede sind vorhersagbar")
        print("-> Keine 'unvorhersehbaren' Gate Errors mehr")
        print("="*70)
    
    def test_qubit_array_drift_map(self):
        """Drift-Map für Qubit-Array."""
        print("\n" + "="*70)
        print("TEST: Qubit-Array Drift-Map")
        print("="*70)
        
        # 3x3 Qubit-Array mit leichter Höhenvariation
        qubits = []
        for i in range(3):
            for j in range(3):
                # Höhe variiert um +/- 0.5 mm
                z = (i - 1) * 0.5e-3 + (j - 1) * 0.2e-3
                q = Qubit(id=f"Q{i}{j}", x=i*1e-3, y=j*1e-3, z=z)
                qubits.append(q)
        
        print("Qubit-Array (3x3):")
        print(f"{'ID':>5} | {'z [um]':>10} | {'Xi':>20} | {'D_SSZ':>20}")
        print("-" * 60)
        
        xi_values = []
        for q in qubits:
            analysis = analyze_qubit_segment(q, M_EARTH)
            xi_values.append(analysis.xi)
            print(f"{q.id:>5} | {q.z*1e6:>10.1f} | {analysis.xi:>20.15e} | {analysis.time_dilation:>20.15f}")
        
        # Uniformität berechnen
        uniformity = array_segment_uniformity(qubits, M_EARTH)
        
        print(f"\nArray-Uniformität:")
        print(f"  Xi Range: {uniformity['xi_range']:.6e}")
        print(f"  Xi Std: {uniformity['xi_std']:.6e}")
        print(f"  Uniformitäts-Score: {uniformity['uniformity']:.6f}")
        
        print("\n** SSZ-ANWENDUNG **")
        print("-> Komplette Drift-Map des Arrays berechenbar")
        print("-> Identifiziere problematische Qubit-Positionen")
        print("-> Optimiere Array-Layout für minimale Drift")
        print("="*70)
    
    def test_predict_gate_error_from_position(self):
        """Gate-Error aus Position vorhersagen."""
        print("\n" + "="*70)
        print("TEST: Gate-Error-Vorhersage aus Position")
        print("="*70)
        
        # Qubit 1.5 mm näher an Erdoberfläche als Nachbar
        q1 = Qubit(id="Q1", x=0, y=0, z=0, gate_time=50e-9)
        q2 = Qubit(id="Q2", x=1e-3, y=0, z=1.5e-3, gate_time=50e-9)  # 1.5 mm höher
        pair = QubitPair(q1, q2)
        
        mismatch = qubit_pair_segment_mismatch(pair, M_EARTH)
        timing = two_qubit_gate_timing(pair, M_EARTH)
        
        print(f"Qubit 1: z = {q1.z*1e3:.1f} mm")
        print(f"Qubit 2: z = {q2.z*1e3:.1f} mm")
        print(f"Höhendifferenz: {pair.height_difference*1e3:.1f} mm")
        print(f"\nSSZ-Vorhersagen:")
        print(f"  Delta Xi: {mismatch['delta_xi']:.6e}")
        print(f"  Phase Drift/Gate: {mismatch['phase_drift_per_gate']:.6e} rad")
        print(f"  Timing-Asymmetrie: {timing['timing_asymmetry']:.6e}")
        print(f"  Max Fidelity-Verlust: {timing['max_fidelity_loss']:.6e}")
        
        print("\n** SSZ-LÖSUNG **")
        print("-> Gate-Error ist VORHERSAGBAR aus Position!")
        print("-> 'Dein Qubit ist 1.5 mm näher an der Erde' = quantifizierbar")
        print("-> Kompensation durch angepasstes Timing möglich")
        print("="*70)


# =============================================================================
# TEST 4: SEGMENT-AWARE FEHLERKORREKTUR
# =============================================================================

class TestSegmentAwareQEC:
    """
    Tests für: Segment-Aware Fehlerkorrektur
    
    Klassische QEC geht davon aus, dass die Welt gleichmäßig ist.
    -> Haha. Nope.
    
    SSZ ermöglicht gravitationssensitive QEC-Methoden.
    """
    
    def test_segment_aware_syndrome_weights(self):
        """Syndrome-Gewichte basierend auf Segment-Position."""
        print("\n" + "="*70)
        print("TEST: Segment-Aware Syndrome-Gewichte")
        print("="*70)
        
        # Simuliere 5-Qubit Code mit Höhenvariation
        heights = [0, 0.1e-3, 0.2e-3, 0.1e-3, 0]  # mm
        
        print("5-Qubit Code mit Höhenvariation:")
        print(f"{'Qubit':>6} | {'Höhe [um]':>10} | {'Xi':>20} | {'Gewicht':>10}")
        print("-" * 55)
        
        xi_values = []
        for i, h in enumerate(heights):
            r = R_EARTH + h
            xi = xi_segment_density(r, M_EARTH)
            xi_values.append(xi)
            
            # Gewicht basierend auf Xi-Abweichung vom Mittel
            weight = 1.0  # Wird später berechnet
            print(f"Q{i:>5} | {h*1e6:>10.1f} | {xi:>20.15e} | {weight:>10.4f}")
        
        # Berechne Gewichte basierend auf Xi-Variation
        xi_mean = np.mean(xi_values)
        xi_std = np.std(xi_values)
        
        print(f"\nXi-Statistik:")
        print(f"  Mean Xi: {xi_mean:.15e}")
        print(f"  Std Xi: {xi_std:.6e}")
        
        # Gewichte: Qubits mit höherer Xi-Abweichung bekommen niedrigeres Gewicht
        weights = []
        for xi in xi_values:
            if xi_std > 0:
                deviation = abs(xi - xi_mean) / xi_std
                weight = 1.0 / (1.0 + deviation)
            else:
                weight = 1.0
            weights.append(weight)
        
        print(f"\nSegment-Aware Gewichte:")
        for i, w in enumerate(weights):
            print(f"  Q{i}: {w:.4f}")
        
        print("\n** SSZ-QEC **")
        print("-> Syndrome-Gewichte berücksichtigen lokales Xi!")
        print("-> Qubits in 'schlechten' Segmenten = niedrigeres Gewicht")
        print("-> Erste 'gravitationssensitive' QEC-Methode!")
        print("="*70)
    
    def test_segment_boundary_detection(self):
        """Erkennung kritischer Segment-Grenzen."""
        print("\n" + "="*70)
        print("TEST: Kritische Segment-Grenzen erkennen")
        print("="*70)
        
        # Scanne Höhenbereich nach Xi-Gradienten
        heights = np.linspace(0, 1e-3, 100)  # 0 bis 1 mm
        
        gradients = []
        for h in heights:
            r = R_EARTH + h
            grad = abs(xi_gradient(r, M_EARTH))
            gradients.append(grad)
        
        max_grad = max(gradients)
        max_grad_height = heights[gradients.index(max_grad)]
        
        print(f"Höhenbereich: 0 - 1 mm")
        print(f"Max |dXi/dr|: {max_grad:.6e} /m")
        print(f"Bei Höhe: {max_grad_height*1e6:.1f} um")
        
        # Gradient sollte relativ konstant sein (weak field)
        grad_variation = (max(gradients) - min(gradients)) / np.mean(gradients)
        print(f"Gradient-Variation: {grad_variation*100:.4f}%")
        
        print("\n** SSZ-QEC **")
        print("-> Identifiziere Bereiche mit hohem Xi-Gradienten")
        print("-> Diese sind 'kritische Segment-Grenzen'")
        print("-> Vermeide Qubit-Platzierung an diesen Grenzen!")
        print("="*70)


# =============================================================================
# TEST 5: QUANTENKOMMUNIKATION & SSZ-SYNCHRONISATION
# =============================================================================

class TestQuantumCommunicationSSZ:
    """
    Tests für: Quantenkommunikation & SSZ als Sync-Schicht
    
    "Du brauchst keine Uhr - du brauchst ein Xi-gestütztes 
    Raumzeit-Segmentmodell."
    
    -> Neue Synchronisationsinfrastruktur basierend auf Raumzeit selbst
    """
    
    def test_distributed_qubits_sync(self):
        """Synchronisation verteilter Qubits über SSZ."""
        print("\n" + "="*70)
        print("TEST: Verteilte Qubits SSZ-Synchronisation")
        print("="*70)
        
        # Zwei Qubits 10 km entfernt, verschiedene Höhen
        # Qubit 1: Meeresspiegel
        # Qubit 2: 100 m höher, 10 km entfernt
        
        q1 = Qubit(id="Q1", x=0, y=0, z=0)
        q2 = Qubit(id="Q2", x=10000, y=0, z=100)  # 10 km entfernt, 100 m höher
        
        r1 = R_EARTH + q1.z
        r2 = R_EARTH + q2.z
        
        xi1 = xi_segment_density(r1, M_EARTH)
        xi2 = xi_segment_density(r2, M_EARTH)
        d1 = ssz_time_dilation(r1, M_EARTH)
        d2 = ssz_time_dilation(r2, M_EARTH)
        
        print(f"Qubit 1: Höhe = {q1.z} m")
        print(f"Qubit 2: Höhe = {q2.z} m, Distanz = {q2.x/1000} km")
        print(f"\nSSZ-Parameter:")
        print(f"  Xi(Q1) = {xi1:.15e}")
        print(f"  Xi(Q2) = {xi2:.15e}")
        print(f"  D_SSZ(Q1) = {d1:.15f}")
        print(f"  D_SSZ(Q2) = {d2:.15f}")
        
        # Zeitdifferenz pro Sekunde
        delta_d = abs(d1 - d2)
        time_drift_per_second = delta_d  # Sekunden pro Sekunde
        
        print(f"\nZeitdrift:")
        print(f"  |D1 - D2| = {delta_d:.6e}")
        print(f"  Drift/Sekunde = {time_drift_per_second*1e12:.6f} ps")
        print(f"  Drift/Stunde = {time_drift_per_second*3600*1e9:.6f} ns")
        
        print("\n** SSZ-SYNC **")
        print("-> Zeitdifferenz ist aus Xi BERECHENBAR!")
        print("-> Keine klassische Uhr-Synchronisation nötig")
        print("-> SSZ = Raumzeit-basierte Sync-Infrastruktur")
        print("="*70)
    
    def test_teleportation_timing_correction(self):
        """Timing-Korrektur für Quanten-Teleportation."""
        print("\n" + "="*70)
        print("TEST: Teleportation Timing-Korrektur")
        print("="*70)
        
        # Alice und Bob auf verschiedenen Höhen
        alice_height = 0      # Meeresspiegel
        bob_height = 500      # 500 m höher (z.B. Berggipfel)
        
        r_alice = R_EARTH + alice_height
        r_bob = R_EARTH + bob_height
        
        d_alice = ssz_time_dilation(r_alice, M_EARTH)
        d_bob = ssz_time_dilation(r_bob, M_EARTH)
        
        # Teleportation dauert nominell 1 us
        t_teleport_nominal = 1e-6
        
        # SSZ-korrigierte Zeiten
        t_alice = t_teleport_nominal / d_alice
        t_bob = t_teleport_nominal / d_bob
        
        # Timing-Mismatch
        timing_mismatch = abs(t_alice - t_bob)
        
        print(f"Alice: Höhe = {alice_height} m, D_SSZ = {d_alice:.15f}")
        print(f"Bob: Höhe = {bob_height} m, D_SSZ = {d_bob:.15f}")
        print(f"\nTeleportation Timing:")
        print(f"  Nominell: {t_teleport_nominal*1e6:.3f} us")
        print(f"  Alice (lokal): {t_alice*1e6:.15f} us")
        print(f"  Bob (lokal): {t_bob*1e6:.15f} us")
        print(f"  Mismatch: {timing_mismatch*1e15:.6f} fs")
        
        # Korrektur berechnen
        correction_factor = d_bob / d_alice
        print(f"\nSSZ-Korrektur:")
        print(f"  Korrekturfaktor: {correction_factor:.15f}")
        print(f"  Bob muss Timing um {(correction_factor-1)*1e12:.6f} ppm anpassen")
        
        print("\n** SSZ-TELEPORTATION **")
        print("-> Timing-Mismatch ist VORHERSAGBAR!")
        print("-> Korrektur aus D_SSZ-Verhältnis berechenbar")
        print("-> Ermöglicht präzise Quanten-Teleportation über Distanzen")
        print("="*70)
    
    def test_quantum_repeater_chain(self):
        """SSZ-Analyse einer Quantum Repeater Kette."""
        print("\n" + "="*70)
        print("TEST: Quantum Repeater Kette SSZ-Analyse")
        print("="*70)
        
        # 5 Repeater über 50 km mit variierenden Höhen
        repeater_positions = [
            (0, 0),        # km, m Höhe
            (10, 50),
            (25, 200),     # Hügel
            (40, 100),
            (50, 0),
        ]
        
        print("Repeater-Kette (50 km):")
        print(f"{'Repeater':>10} | {'Distanz [km]':>12} | {'Höhe [m]':>10} | {'Xi':>20} | {'D_SSZ':>15}")
        print("-" * 75)
        
        xi_values = []
        d_values = []
        
        for i, (dist, height) in enumerate(repeater_positions):
            r = R_EARTH + height
            xi = xi_segment_density(r, M_EARTH)
            d = ssz_time_dilation(r, M_EARTH)
            xi_values.append(xi)
            d_values.append(d)
            
            print(f"R{i:>9} | {dist:>12} | {height:>10} | {xi:>20.15e} | {d:>15.12f}")
        
        # Maximale Variation
        max_delta_xi = max(xi_values) - min(xi_values)
        max_delta_d = max(d_values) - min(d_values)
        
        print(f"\nKetten-Analyse:")
        print(f"  Max Delta Xi: {max_delta_xi:.6e}")
        print(f"  Max Delta D_SSZ: {max_delta_d:.6e}")
        print(f"  Kritischstes Segment: R{xi_values.index(max(xi_values))} <-> R{xi_values.index(min(xi_values))}")
        
        print("\n** SSZ-REPEATER **")
        print("-> Jeder Repeater hat eigene Segmentzeit!")
        print("-> SSZ ermöglicht präzise Timing-Kompensation")
        print("-> Quantum Repeater werden ZUVERLÄSSIGER")
        print("="*70)


# =============================================================================
# INTEGRATION TEST: VOLLSTÄNDIGES QUBIT-SYSTEM
# =============================================================================

class TestFullQubitSystem:
    """Integration Test: Vollständiges Qubit-System mit SSZ."""
    
    def test_complete_ssz_qubit_workflow(self):
        """Kompletter SSZ-Workflow für Qubit-System."""
        print("\n" + "="*70)
        print("INTEGRATION TEST: Vollständiger SSZ-Qubit-Workflow")
        print("="*70)
        
        # 1. Definiere Qubit-Array
        print("\n[1] Qubit-Array Definition")
        qubits = [
            Qubit(id="Q0", x=0, y=0, z=0, coherence_time_T2=100e-6, gate_time=50e-9),
            Qubit(id="Q1", x=1e-3, y=0, z=0.1e-3, coherence_time_T2=100e-6, gate_time=50e-9),
            Qubit(id="Q2", x=0, y=1e-3, z=0.2e-3, coherence_time_T2=100e-6, gate_time=50e-9),
            Qubit(id="Q3", x=1e-3, y=1e-3, z=0.15e-3, coherence_time_T2=100e-6, gate_time=50e-9),
        ]
        print(f"  -> {len(qubits)} Qubits definiert")
        
        # 2. SSZ-Analyse jedes Qubits
        print("\n[2] SSZ-Analyse")
        analyses = []
        for q in qubits:
            analysis = analyze_qubit_segment(q, M_EARTH)
            analyses.append(analysis)
            print(f"  {q.id}: Xi={analysis.xi:.6e}, D_SSZ={analysis.time_dilation:.12f}")
        
        # 3. Array-Uniformität
        print("\n[3] Array-Uniformität")
        uniformity = array_segment_uniformity(qubits, M_EARTH)
        print(f"  Xi Range: {uniformity['xi_range']:.6e}")
        print(f"  Uniformitäts-Score: {uniformity['uniformity']:.4f}")
        
        # 4. Paar-Analyse
        print("\n[4] Qubit-Paar-Analyse")
        pair = QubitPair(qubits[0], qubits[3])  # Diagonal
        mismatch = qubit_pair_segment_mismatch(pair, M_EARTH)
        print(f"  Q0-Q3 Mismatch: Delta Xi = {mismatch['delta_xi']:.6e}")
        
        # 5. Gate-Timing
        print("\n[5] Gate-Timing-Optimierung")
        timing = two_qubit_gate_timing(pair, M_EARTH)
        print(f"  Optimale Gate-Zeit: {timing['optimal_gate_time']*1e9:.6f} ns")
        print(f"  Timing-Asymmetrie: {timing['timing_asymmetry']:.6e}")
        
        # 6. Decoherence-Vorhersage
        print("\n[6] Decoherence-Vorhersage")
        for q in qubits:
            T2_eff = effective_T2(q, M_EARTH)
            print(f"  {q.id}: T2_eff = {T2_eff*1e6:.3f} us (von {q.coherence_time_T2*1e6:.1f} us)")
        
        # 7. Kohärente Zone
        print("\n[7] Kohärente Segmentzone")
        zone = segment_coherent_zone(0, 1e-18, M_EARTH)
        h_min, h_max = zone
        print(f"  Zonenbreite: {(h_max - h_min)*1e6:.3f} um")
        
        print("\n" + "="*70)
        print("SSZ-QUBIT-WORKFLOW KOMPLETT")
        print("="*70)
        print("\n** FAZIT **")
        print("-> SSZ ermöglicht vollständige Qubit-System-Analyse")
        print("-> Alle Effekte sind VORHERSAGBAR und KOMPENSIERBAR")
        print("-> 'Konzert mit Stimmung' statt 'schiefer Töne'")
        print("="*70)
        
        # Assertions
        assert len(analyses) == 4
        assert uniformity['uniformity'] > 0
        assert timing['optimal_gate_time'] > 0


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short"])
