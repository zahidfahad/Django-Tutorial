FROM python:3.8

WORKDIR /opt/app

# python stuff
ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

# python env
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
COPY entrypoint.sh /usr/local/bin
RUN chmod +x /usr/local/bin/entrypoint.sh
CMD ["entrypoint.sh"]