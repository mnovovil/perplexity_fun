# Use Miniconda base image
FROM continuumio/miniconda3

WORKDIR /app

COPY requirements.txt .
COPY src/ ./src/
COPY entrypoint.sh ./entrypoint.sh

RUN conda create -n appenv python=3.11

RUN /bin/bash -c "source activate appenv && pip install --no-cache-dir -r requirements.txt"

RUN chmod +x /app/entrypoint.sh

SHELL ["conda", "run", "-n", "appenv", "/bin/bash", "-c"]

ENTRYPOINT ["/app/entrypoint.sh"]
CMD []
