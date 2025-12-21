# 6. Engineering Implications — Extended Version

## 6.2 Compiler Integration: Detailed Design Decisions

The integration of SSZ compensation into quantum compilers requires careful trade-offs between precision, overhead, and maintainability. This section explains the design decisions behind the presented code structures.

### 6.2.1 Why Virtual-Z Instead of Physical Pulses?

Compensation of SSZ drift can be implemented in two fundamentally different ways: through physical pulses that realize a Z-rotation, or through virtual Z-gates that only change the reference frame.

**Physical Z-Rotation:**

A physical RZ(φ) pulse consists of a microwave signal that effects a rotation around the Z-axis of the Bloch sphere. Typically, this is realized through an off-resonance pulse or through frame changes in the control system:

```python
def physical_rz(qubit, angle):
    """
    Physical Z-rotation through detuning pulse.
    
    Disadvantages:
    - Finite gate time (10-50 ns)
    - Additional error source (gate infidelity)
    - Potential crosstalk effects
    - Increased circuit depth
    """
    pulse_duration = 20e-9  # 20 ns
    detuning = angle / pulse_duration  # Frequency shift
    apply_pulse(qubit, duration=pulse_duration, detuning=detuning)
```

**Virtual Z-Rotation:**

A virtual RZ(φ) operation requires no physical pulse. Instead, the reference frame for all subsequent pulses of the affected qubit is rotated by angle φ:

```python
def virtual_rz(qubit, angle, frame_tracker):
    """
    Virtual Z-rotation through frame update.
    
    Advantages:
    - Zero gate time (instantaneous)
    - No additional error source
    - No crosstalk
    - No increase in circuit depth
    """
    frame_tracker[qubit] += angle
    # All subsequent pulses are generated with rotated frame
```

**Why Virtual for SSZ?**

SSZ compensation is ideal for virtual implementation:
1. **Magnitude:** Compensation angles are extremely small (10⁻¹³ rad for transmons). Physical pulses with such precision are technically impossible.
2. **Determinism:** SSZ corrections are known before runtime and can be built into pulse generation.
3. **Accumulation:** Many small corrections can be combined into a single frame adjustment.

### 6.2.2 Height Profile Acquisition: Practical Methods

The foundation of any SSZ compensation is precise knowledge of height positions for all qubits. Different measurement methods offer different precision/effort trade-offs:

**Profilometry (Contact/Optical):**

Before chip mounting, the substrate surface topography can be measured:

```python
def acquire_height_map_profilometry(chip_id, measurement_points):
    """
    Acquire height profile using optical profilometry.
    
    Typical parameters:
    - Lateral resolution: 1-10 μm
    - Vertical resolution: 1-10 nm
    - Measurement time: 5-30 min per chip
    
    Limitations:
    - Measures only substrate, not final qubit position
    - Mounting deformation not captured
    """
    height_map = {}
    for qubit_id, (x, y) in measurement_points.items():
        # Profilometer measurement at position (x, y)
        z = profilometer.measure(x, y)
        height_map[qubit_id] = z + chip_mounting_offset
    return height_map
```

**In-situ Calibration:**

After mounting in the cryostat, effective height difference can be determined indirectly via frequency measurements—if an additional height-dependent reference is available:

```python
def calibrate_height_in_situ(qubit_pairs, reference_gradient):
    """
    Calibrate relative heights by comparison with known gradient.
    
    Prerequisite: Known physical gradient (e.g., magnetic field)
    
    Method:
    1. Measure frequency shift between qubit pairs
    2. Correlate with gradient measurement
    3. Extract height difference
    """
    height_diffs = {}
    for q1, q2 in qubit_pairs:
        freq_diff = measure_frequency_difference(q1, q2)
        gradient_component = measure_gradient(q1, q2)
        # Derivation: Δh = Δf / (df/dh) with gradient correction
        delta_h = estimate_height_from_correlations(freq_diff, gradient_component)
        height_diffs[(q1, q2)] = delta_h
    return height_diffs
```

**GPS/Leveling (for Distributed Systems):**

For remote entanglement between different laboratories, GPS or classical leveling is required:

```python
def acquire_height_network(node_locations):
    """
    Determine heights for network nodes.
    
    Methods:
    - Differential GPS: ±1-10 cm vertical
    - Precision leveling: ±1 mm
    - Barometric (backup): ±1-10 m
    """
    heights = {}
    for node_id, location in node_locations.items():
        # Primary: Geodetic database
        h_geodetic = query_geodetic_database(location)
        # Secondary: Local measurement
        h_local = gps_receiver.get_altitude(location)
        # Combination with weighting
        heights[node_id] = weighted_average(h_geodetic, h_local)
    return heights
```

### 6.2.3 Calibration Database Schema

Storage of SSZ-relevant calibration data requires a careful database structure:

```python
# Database schema for SSZ calibration

class DeviceCalibration:
    """
    SSZ calibration data for a quantum device.
    """
    device_id: str
    calibration_timestamp: datetime
    
    # Geometry
    qubit_positions: Dict[QubitId, Position3D]  # (x, y, z) in meters
    height_reference: str  # "chip_center", "lowest_qubit", "lab_floor"
    height_uncertainty: Dict[QubitId, float]  # Measurement uncertainty in meters
    
    # Derived SSZ parameters
    qubit_frequencies: Dict[QubitId, float]  # ω in rad/s
    delta_D_matrix: np.ndarray  # ΔD for all qubit pairs
    compensation_phases: Dict[Tuple[QubitId, GateId], float]  # Φ_corr for gates
    
    # Metadata
    measurement_method: str  # "profilometry", "gps", "in_situ"
    valid_until: datetime  # Expiration date (for static geometry: far in future)


def update_calibration_database(device_id, new_height_map):
    """
    Update SSZ calibration for a device.
    
    Called for:
    - Initial device installation
    - Physical relocation of cryostat
    - Periodic revalidation (annually)
    
    NOT called for:
    - Thermal cycles (geometry stable)
    - Software updates
    - Qubit recalibration (ω, T₁, T₂)
    """
    # Calculate derived parameters
    delta_D = compute_delta_D_matrix(new_height_map)
    
    # Calculate compensation phases for all gate types
    compensation = {}
    for gate_type in ['single', 'cz', 'swap']:
        gate_time = get_typical_gate_time(device_id, gate_type)
        for q1, q2 in all_qubit_pairs(device_id):
            omega_avg = (qubit_frequencies[q1] + qubit_frequencies[q2]) / 2
            phi_corr = -omega_avg * delta_D[q1, q2] * gate_time
            compensation[(q1, q2, gate_type)] = phi_corr
    
    # Store
    calibration = DeviceCalibration(
        device_id=device_id,
        qubit_positions=new_height_map,
        delta_D_matrix=delta_D,
        compensation_phases=compensation,
        calibration_timestamp=datetime.now(),
        valid_until=datetime.now() + timedelta(days=365)
    )
    database.store(calibration)
```

### 6.2.4 Gate Synthesis with SSZ Correction

Integration into the compilation workflow occurs in the gate synthesis phase:

```python
class SSZAwareGateSynthesizer:
    """
    Gate synthesizer with SSZ compensation.
    
    Workflow:
    1. Receives abstract quantum circuit
    2. Decomposes into native gates
    3. Inserts SSZ compensation
    4. Generates control pulses
    """
    
    def __init__(self, device_calibration: DeviceCalibration):
        self.calibration = device_calibration
        self.frame_tracker = defaultdict(float)  # Virtual Z-frame per qubit
    
    def synthesize_circuit(self, circuit: QuantumCircuit) -> PulseSchedule:
        """
        Synthesize circuit with SSZ correction.
        """
        schedule = PulseSchedule()
        
        for gate in circuit.gates:
            if gate.is_two_qubit:
                # SSZ compensation for two-qubit gates
                q1, q2 = gate.qubits
                phi_corr = self.get_ssz_compensation(q1, q2, gate.type)
                
                # Virtual Z-rotation on higher qubit
                higher_qubit = q2 if self.is_higher(q2, q1) else q1
                self.frame_tracker[higher_qubit] += phi_corr
            
            # Translate gate to pulse sequence
            pulses = self.gate_to_pulses(gate)
            
            # Apply frame correction to pulses
            corrected_pulses = self.apply_frame_corrections(pulses)
            schedule.append(corrected_pulses)
        
        return schedule
    
    def get_ssz_compensation(self, q1, q2, gate_type):
        """
        Retrieve precomputed SSZ compensation from calibration.
        """
        key = (q1, q2, gate_type)
        if key in self.calibration.compensation_phases:
            return self.calibration.compensation_phases[key]
        else:
            # Fallback: Compute on-the-fly
            return self.compute_compensation(q1, q2, gate_type)
```

### 6.2.5 Overhead Analysis

SSZ compensation has minimal overhead:

| Aspect | Overhead | Rationale |
|--------|----------|------------|
| **Memory** | O(N²) | ΔD matrix for N qubits |
| **Compute time (calibration)** | O(N²) | Once per installation |
| **Compute time (per gate)** | O(1) | Lookup in precomputed table |
| **Gate time** | +0 ns | Virtual Z-rotation is instantaneous |
| **Additional errors** | +0 | No physical pulses |
| **Circuit depth** | +0 | No additional gates |

**Comparison with other corrections:**

| Correction Type | Overhead (Time) | Overhead (Error) |
|-----------------|-----------------|-------------------|
| SSZ | 0 | 0 |
| Dynamical Decoupling | +10-50% | +1-5% |
| Error Correction | +100-1000% | - |
| Real-time Calibration | +5-20% | +0.1-1% |

SSZ compensation is thus the "cheapest" form of correction—it literally costs nothing.

---

## 6.4 Quantum Network Architecture — Extended Discussion

### 6.4.1 Height Exchange Protocol

For SSZ-aware quantum networks, a standardized protocol for height information exchange must be defined:

```python
class SSZNetworkProtocol:
    """
    Protocol for SSZ metadata exchange in quantum networks.
    
    Message types:
    - HEIGHT_ANNOUNCE: Node shares its height
    - HEIGHT_REQUEST: Node queries height of another
    - COMPENSATION_NEGOTIATE: Agreement on compensation responsibility
    """
    
    def on_link_establishment(self, local_node, remote_node):
        """
        Called when establishing a quantum connection.
        """
        # 1. Height exchange
        local_height = self.get_local_height()
        remote_height = self.request_height(remote_node)
        
        delta_h = remote_height - local_height
        
        # 2. Compensation negotiation
        # Convention: Lower node is reference
        if local_height < remote_height:
            # Local node is reference, remote compensates
            self.send_message(remote_node, COMPENSATION_REQUEST, delta_h)
        else:
            # Remote is reference, local compensates
            self.local_compensation = self.compute_compensation(delta_h)
        
        # 3. Confirmation
        self.log_ssz_metadata(local_node, remote_node, delta_h)
    
    def compute_compensation(self, delta_h):
        """
        Calculate compensation parameters for link.
        
        Returns:
            CompensationParams with Φ_corr formula and update frequency
        """
        # For optical links
        omega_optical = 2 * np.pi * 429e12  # 429 THz
        
        # Compensation rate (rad/s)
        compensation_rate = omega_optical * R_S_EARTH * delta_h / R_EARTH**2
        
        return CompensationParams(
            rate=compensation_rate,
            method='continuous',  # or 'discrete'
            update_interval_ms=1.0  # For continuous: update every ms
        )
```

### 6.4.2 Error Budget Allocation

In a complete quantum network, various error sources compete for the limited error budget:

```
Total Fidelity Budget: 1 - F_target = 10⁻³ (99.9% Fidelity)

Allocation:
├── Photon link loss: 30%     → 3×10⁻⁴
├── Gate errors (local): 25%  → 2.5×10⁻⁴
├── Decoherence (T₂): 20%     → 2×10⁻⁴
├── SSZ residual: 5%          → 5×10⁻⁵
├── Timing jitter: 10%        → 1×10⁻⁴
└── Other: 10%                → 1×10⁻⁴
```

**SSZ Residual:**

The SSZ residual is the remaining error after compensation, caused by:
- Height measurement uncertainty: δh
- Frequency uncertainty: δω
- Timing uncertainty: δt

```
ε_SSZ = ω × r_s × δh / R² × t + r_s × Δh / R² × t × δω/ω + ω × r_s × Δh / R² × δt
```

For typical uncertainties (δh = 1 cm, δω/ω = 10⁻⁶, δt = 1 μs):
```
ε_SSZ ≈ 10⁻⁶ rad (for optical links at 1 m)
```

This is far below the allocated budget of 5×10⁻⁵ rad → SSZ compensation is sufficiently precise.

---

© 2025 Carmen Wrede & Lino Casu
