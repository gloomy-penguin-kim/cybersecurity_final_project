FROM ubuntu:latest
#FROM python:3.9-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-pip

RUN apt-get install -y net-tools

COPY requirements.txt .

RUN pip3 install  --break-system-packages --no-cache-dir -r requirements.txt

COPY . .

ADD https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb  msfinstall 
RUN chmod 755 msfinstall 
RUN ./msfinstall

ENV VITE_METASPLOIT_PORT=8085
ENV VITE_METASPLOIT_API_URL=http://0.0.0.0 

EXPOSE 5000
EXPOSE 8085

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8085"]