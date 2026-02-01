## ▶️ 1.create virtual env on windows
cmd
python -m venv myenv


## ▶️ 2. Activate Virtual Environment

### ✅ Windows (Command Prompt)

```bash
myenv\Scripts\activate


if you are unable to activate try below command 
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Install dependencies
pip install -r requirements.txt

Note this might take a lot of time.

Environment Variables

# Required for RAG examples
OPENAI_API_KEY=your-openai-api-key

# LlamaParse (https://cloud.llamaindex.ai/)
LLAMA_CLOUD_API_KEY=llx-your-api-key

# Vectorize.io (https://platform.vectorize.io/)
VECTORIZE_ORGANIZATION_ID=your-org-id
VECTORIZE_API_KEY=your-api-key

# Optional
HF_TOKEN=your-huggingface-token
PINECONE_API_KEY=your-pinecone-key


======================

HomeLoan Disburement Document parsing using LlamaParse

