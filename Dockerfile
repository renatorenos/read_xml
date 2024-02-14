# Define a imagem base
FROM renatorenos/clientoracledb21-python310

COPY ora/* /usr/lib/oracle/21/client64/lib/network/admin/
# COPY xml/* xml/
# COPY *.py /app/

# Instalação do Python
RUN python3.10 -m pip install --upgrade pip
RUN pip install loguru
RUN pip install lxml
RUN pip install python-dotenv

# Defina o diretÃ³rio de trabalho como o diretÃ³rio do seu aplicativo
WORKDIR /app

CMD ["tail", "-f", "/dev/null"]