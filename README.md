# AI CFO Assistant

## API Keys

### OpenAI API Key (Required)
1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Navigate to API keys section
4. Create a new API key
5. Add to `.env` file: `OPENAI_API_KEY=sk-...`

### LangSmith API Key (Optional - for tracing)
1. Go to [smith.langchain.com](https://smith.langchain.com)
2. Sign up or log in
3. Navigate to Settings → API Keys
4. Create a new API key
5. Add to `.env` file: `LANGSMITH_API_KEY=lsv2_...`

## Setup

### Using uv (recommended)
```bash
# Clone and navigate to the project
cd ai-assessment-v3

# Install dependencies
uv sync

# Copy environment file and add your OpenAI API key
cp .env.example .env
# Edit .env and set OPENAI_API_KEY=your-key-here

# Run the application
uv run langgraph dev
```

### Using pip
```bash
# Clone and navigate to the project
cd ai-assessment-v3

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e . "langgraph-cli[inmem]"

# Copy environment file and add your OpenAI API key
cp .env.example .env
# Edit .env and set OPENAI_API_KEY=your-key-here

# Run the application
langgraph dev
```

## Example Queries

### Chat Flow (conversational responses)
- "Hello, how are you?"
- "What can you help me with?"
- "Tell me about yourself"

### Finance Flow - Retriever Tool (searches PDF reports)
- "What were the key performance metrics from the March 2025 report?"
- "Tell me about customer growth mentioned in the April report"
- "Search for strategic initiatives in the company reports"
- "What are the executive summary highlights from June 2025?"

### Finance Flow - Financial Statements Tool (queries CSV data)
- "What was the ARR in March 2025?"
- "Show me the gross margin for April 2025"
- "What's the customer count in May 2025?"
- "What is the cash burn rate in June 2025?"
- "How many employees does the company have in Q1 2025?"

Note: Financial data is available for March-June 2025.