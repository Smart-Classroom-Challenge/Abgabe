FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_DEBUG=True
ENV secret_key=oursecretvalue
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY SmartClassRoom /app
CMD python manage.py runserver 0.0.0.0:8000 --noreload
EXPOSE 8000