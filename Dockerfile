FROM python
WORKDIR /telegram_service
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "main.py"]