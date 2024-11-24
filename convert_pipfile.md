# Pipfile to Conda Environment Converter

When working with both pip and conda package managers, we need to:

1. Maintain Pipfile as single source of truth
2. Generate conda-compatible environment specifications
3. Avoid mixing pip and conda package installations
4. Ensure reproducible builds
5. Keep build environment separate from runtime environment

## Solution Components

### 1. convert_pipfile.py

The Python script that reads a Pipfile and generates an equivalent conda environment.yml. Key features:

- Uses toml to parse Pipfile
- Uses pyyaml to generate valid YAML output
- Automatically includes conda-forge channel
- Preserves Python version requirements
- Hardcodes environment name to 'ice_breaker'

### 2. convert_pipfile.yml

A minimal conda environment specification for running the converter:

```yaml
name: convert_pipfile
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.10
  - pyyaml
  - toml
```

### 3. Makefile

Orchestrates the conversion process:

- Creates temporary conda environment using convert_pipfile.yml
- Runs conversion
- Cleans up after itself

## How It Works

1. The Makefile creates a temporary conda environment using convert_pipfile.yml
2. It activates this environment and runs convert_pipfile.py
3. The script reads your Pipfile and generates an environment.yml
4. The temporary environment is removed

## Usage

To generate environment.yml:

```bash
make environment.yml
```

To clean up:

```bash
make clean
```
