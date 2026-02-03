# Use Miniconda base image
FROM continuumio/miniconda3

WORKDIR /app

COPY requirements.txt .
COPY src/ ./src/

RUN conda create -n appenv python=3.11

RUN /bin/bash -c "source activate appenv && pip install --no-cache-dir -r requirements.txt"

SHELL ["conda", "run", "-n", "appenv", "/bin/bash", "-c"]

CMD ["conda", "run", "-n", "appenv", "python", "./src/query.py"]
