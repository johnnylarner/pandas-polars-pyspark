FROM python:3.10

WORKDIR /code

COPY dist/ .
RUN pip install ./ppp-*.whl

COPY scripts/ ./scripts
RUN ls

CMD ["python3", "scripts/launch.py"]
