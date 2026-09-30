# Deploy no Google Cloud Run

Este projeto está pronto para ser publicado como um serviço web usando o
`Dockerfile` na raiz. Nenhuma implantação foi feita — os comandos abaixo
publicam o app na sua própria conta do Google Cloud (requer uma conta com
faturamento ativo; o Cloud Run tem uma camada gratuita generosa para projetos
pequenos como este).

## Pré-requisitos

- Uma conta no [Google Cloud](https://console.cloud.google.com/) com um projeto criado
- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) instalada e autenticada (`gcloud init`)

## Passo a passo

```bash
# 1. Defina o projeto do GCP que você vai usar
gcloud config set project SEU_PROJECT_ID

# 2. Ative as APIs necessárias (só precisa rodar uma vez por projeto)
gcloud services enable run.googleapis.com artifactregistry.googleapis.com

# 3. Construa a imagem e publique no Cloud Run em um único comando
gcloud run deploy beaumont-bank \
  --source . \
  --region southamerica-east1 \
  --allow-unauthenticated

# O comando acima builda o Dockerfile, publica a imagem no Artifact Registry
# e sobe o serviço. Ao final, ele imprime uma URL pública (algo como
# https://beaumont-bank-xxxxx-rj.a.run.app) — é esse link que você compartilha
# com o recrutador.
```

## Rodando localmente antes de publicar (recomendado)

```bash
pip install -r requirements.txt
streamlit run app.py
```

Abre em `http://localhost:8501`. Se quiser testar exatamente como vai rodar
no Cloud Run (usando o Docker), com o Docker instalado:

```bash
docker build -t beaumont-bank .
docker run -p 8080:8080 beaumont-bank
```

E acesse `http://localhost:8080`.
