<!-- up docker -->

docker run --name postgres-pgvector -e POSTGRES_USER=boilerplate -e POSTGRES_PASSWORD=boilerplate -e POSTGRES_DB=boilerplate_db -v postgres_data:/var/lib/postgresql/data -p 5432:5432 pgvector/pgvector:pg15

927 uv venv --python 3.12
928 source .venv/bin/
929 source .venv/bin/activate
930 uv pip install langchain langchain-openai langchain-postgres psycopg2-binary python-dotenv

<!-- 931 uv pip install pandas numpy python-pdf2image pypdf2 requests beautifulsoup4 -->

932 uv pip install pandas numpy pypdf2 requests beautifulsoup4
933 uv pip install pdf2image
uv pip install sentence-transformers

uv pip install google-generativeai google-genai google-adk==1.20.0

uv pip install google-genai

uv pip install google-adk==1.20.0
