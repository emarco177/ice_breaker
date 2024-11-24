#!/usr/bin/env python3
import toml
import yaml
from pathlib import Path

def convert_pipfile_to_conda(pipfile_path="Pipfile", output_path="environment.yml"):
    # Read Pipfile
    with open(pipfile_path) as f:
        pipfile = toml.load(f)
    
    # Initialize conda environment structure
    conda_env = {
        "name": Path.cwd().name,  # Use current directory name as environment name
        "channels": [
            "conda-forge",
            "defaults"
        ],
        "dependencies": []
    }
    
    # Add Python version if specified
    if "requires" in pipfile and "python_version" in pipfile["requires"]:
        conda_env["dependencies"].append(f"python={pipfile['requires']['python_version']}")
    
    # Process regular dependencies
    pip_packages = []
    if "packages" in pipfile:
        for package, version in pipfile["packages"].items():
            if version == "*":
                # Try to install via conda first
                conda_env["dependencies"].append(package)
            else:
                # Add to pip section if version is specified
                pip_packages.append(f"{package}{version}")
    
    # Add pip packages if any exist
    if pip_packages:
        conda_env["dependencies"].append({"pip": pip_packages})
    
    # Write environment.yml
    with open(output_path, 'w') as f:
        yaml.dump(conda_env, f, default_flow_style=False, sort_keys=False)

if __name__ == "__main__":
    convert_pipfile_to_conda() 