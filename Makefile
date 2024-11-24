SHELL := /usr/bin/bash
.ONESHELL:  # Required to keep all commands in same shell
CONDA_ACTIVATE := source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate

environment.yml: Pipfile convert_pipfile.py convert_pipfile.yml
	# Create and activate temporary conda environment
	conda env create -f convert_pipfile.yml
	$(CONDA_ACTIVATE) convert_pipfile
	# Run the conversion script
	python convert_pipfile.py
	# Clean up temporary environment - deactivate first
	conda deactivate
	conda env remove -n convert_pipfile

.PHONY: clean
clean:
	rm -f environment.yml
	conda env remove -n convert_pipfile
