FROM node:20-slim AS webapp-build
WORKDIR /webapp
COPY webapp/package*.json ./
RUN npm install
COPY webapp/ ./
RUN npm run build

FROM python:3.12-slim AS base
WORKDIR /srv
ENV PYTHONUNBUFFERED=1 PYTHONPATH=/srv
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY --from=webapp-build /webapp/dist ./webapp/dist

EXPOSE 3008

CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "3008"]
