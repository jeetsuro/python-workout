FROM python:3.9 AS backend-builder
WORKDIR /opt
#COPY simple.py /opt
COPY *.py /opt 
COPY Requirements.txt /opt
RUN pip install --no-cache-dir -r /opt/Requirements.txt

FROM python:3.9-slim
WORKDIR /opt
COPY --from=backend-builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=backend-builder /opt /opt
EXPOSE 8080
ARG color=red
ENV APP_COLOR=${color} 
CMD [ --color ${APP_COLOR}  ] 
ENTRYPOINT ["python", "simple.py"]