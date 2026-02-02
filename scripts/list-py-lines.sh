#!/bin/bash
find . -name "*.py" -not -path "*/.venv/*" -exec wc -l {} \; | sort -rn
