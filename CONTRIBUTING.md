# Contributing to SSZ-Qubits

Thank you for your interest in contributing to SSZ-Qubits! This document provides guidelines for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How to Contribute](#how-to-contribute)
3. [Development Setup](#development-setup)
4. [Code Style](#code-style)
5. [Testing](#testing)
6. [Pull Request Process](#pull-request-process)
7. [License](#license)

---

## Code of Conduct

This project adheres to the principles of the **Anti-Capitalist Software License v1.4**. By contributing, you agree that your contributions will be licensed under the same terms.

### Our Values

- **Open Science**: We believe scientific knowledge should be freely accessible
- **Collaboration**: We welcome contributions from researchers worldwide
- **Ethical Use**: This software must not be used for military, surveillance, or exploitative purposes

---

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/error-wtf/ssz-qubits/issues)
2. If not, create a new issue with:
   - Clear title describing the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Python version and OS
   - Relevant code snippets or error messages

### Suggesting Features

1. Open an issue with the `[Feature Request]` prefix
2. Describe the feature and its use case
3. Explain how it relates to SSZ theory or qubit applications

### Contributing Code

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

---

## Development Setup

### Prerequisites

- Python 3.8+
- Git

### Installation

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ssz-qubits.git
cd ssz-qubits

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest matplotlib numpy
```

### Verify Installation

```bash
# Run tests
python run_tests.py

# Run demo
python demo.py
```

---

## Code Style

### Python Style

- Follow [PEP 8](https://pep8.org/) guidelines
- Use meaningful variable names
- Maximum line length: 100 characters
- Use type hints where appropriate

### Documentation

- All functions must have docstrings (NumPy style)
- Include parameter types and return values
- Add examples for complex functions

### Example

```python
def xi_segment_density(r: float, M: float) -> float:
    """
    Calculate SSZ segment density Xi at radius r.
    
    Parameters
    ----------
    r : float
        Radial distance from center [m]
    M : float
        Central mass [kg]
        
    Returns
    -------
    float
        Segment density Xi (dimensionless)
        
    Examples
    --------
    >>> xi = xi_segment_density(R_EARTH, M_EARTH)
    >>> print(f"Xi = {xi:.6e}")
    Xi = 6.961078e-10
    """
    r_s = schwarzschild_radius(M)
    return r_s / (2 * r)
```

---

## Testing

### Running Tests

```bash
# Run all tests
python run_tests.py

# Run with pytest (verbose)
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_ssz_physics.py -v

# Run specific test
python -m pytest tests/test_ssz_physics.py::TestSegmentDensity -v
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Include both positive and edge case tests

### Test Categories

| Category | Description | File |
|----------|-------------|------|
| Physics | SSZ formulas and calculations | `test_ssz_physics.py` |
| Edge Cases | Extreme values, error handling | `test_edge_cases.py` |
| Applications | Qubit-specific functions | `test_ssz_qubit_applications.py` |
| Validation | Experimental validation | `test_validation.py` |

---

## Pull Request Process

### Before Submitting

1. ✅ All tests pass (`python run_tests.py`)
2. ✅ Code follows style guidelines
3. ✅ New functions have docstrings
4. ✅ New features have tests
5. ✅ Documentation is updated if needed

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] All existing tests pass
- [ ] New tests added for new functionality

## Related Issues
Closes #XX (if applicable)
```

### Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, your PR will be merged

---

## Areas for Contribution

### High Priority

- [ ] Experimental validation with real qubit hardware
- [ ] Integration with quantum computing frameworks (Qiskit, Cirq)
- [ ] Performance optimizations for large qubit arrays
- [ ] Additional visualization tools

### Medium Priority

- [ ] Extended documentation and tutorials
- [ ] More comprehensive test coverage
- [ ] Support for different gravitational environments (Moon, Mars)
- [ ] Quantum error correction integration

### Research Contributions

- [ ] Strong field regime validation
- [ ] Multi-body gravitational effects
- [ ] Time-dependent segment analysis
- [ ] Quantum communication protocols

---

## Contact

- **Email**: [mail@error.wtf](mailto:mail@error.wtf)
- **GitHub**: [github.com/error-wtf](https://github.com/error-wtf)
- **Issues**: [github.com/error-wtf/ssz-qubits/issues](https://github.com/error-wtf/ssz-qubits/issues)

---

## License

By contributing to SSZ-Qubits, you agree that your contributions will be licensed under the **Anti-Capitalist Software License v1.4**.

See [LICENSE](LICENSE) for the full license text.

---

© 2025 Carmen Wrede & Lino Casu

**Thank you for contributing to SSZ-Qubits!**
