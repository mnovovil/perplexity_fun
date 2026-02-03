#!/bin/bash
# Wrapper entrypoint to activate the conda env and run the Python script
set -e

# Prefer activating the conda environment so stdin is preserved
if [ -f "/opt/conda/etc/profile.d/conda.sh" ]; then
	# shellcheck source=/dev/null
	. /opt/conda/etc/profile.d/conda.sh
	conda activate appenv
	exec python /app/src/query.py "$@"
else
	# Fallback to conda run if activate script not available
	exec conda run -n appenv python /app/src/query.py "$@"
fi
