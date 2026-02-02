# Mini RAG Implementation Roadmap

## Project Overview
Build and host a small RAG (Retrieval-Augmented Generation) application that allows users to input text, store it in a cloud-hosted vector database, retrieve relevant chunks using a retriever + reranker pipeline, and answer queries via an LLM with inline citations.

## Tech Stack (Locked)
- **Backend**: FastAPI
- **Frontend**: React
- **Vector Database**: Pinecone (cloud-hosted)
- **Embedding Model**: OpenAI text-embedding-3-small
- **Reranker**: Jina Reranker
- **LLM Provider**: Groq (Llama or Mixtral)
- **Deployment**: Render (backend) + Vercel (frontend)

## Success Criteria
- ✅ Working URL with no console errors on first load
- ✅ Query → retrieval → reranking → LLM answer with visible citations
- ✅ 5 Q/A evaluation pairs with precision/recall notes
- ✅ Complete README with architecture diagram
- ✅ API keys server-side only with .env.example provided

## No-Scope-Creep Rule
Focus on core RAG functionality. Avoid adding auth, multiple file formats, advanced UI features, or optimization experiments until v1 is complete.

---

## Phase 0: Project Setup & Architecture Lock ✓
**Goal**: Initialize project structure and lock down technical decisions

### Tasks:
- [x] Confirm final tech stack (see above)
- [x] Define chunking strategy: 1000 tokens with 12% overlap (120 tokens)
- [x] Define retrieval strategy: Top-20 with MMR, then rerank to Top-5
- [x] Define citation format: inline numeric citations [1], [2]
- [x] Create project directory structure
- [x] Initialize git repository

**Deliverables**: Project structure, roadmap.md (this file)

---

## Phase 1: Backend Skeleton
**Goal**: Set up FastAPI project with basic endpoints and environment configuration

### Tasks:
- [x] Initialize FastAPI project with proper structure
  ```
  backend/
  ├── app/
  │   ├── __init__.py
  │   ├── main.py
  │   ├── routers/
  │   ├── services/
  │   └── models/
  ├── requirements.txt
  └── .env.example
  ```
- [x] Create core endpoints:
  - `GET /health` - Health check
  - `POST /ingest` - Accept text input and store in vector DB
  - `POST /query` - Accept query and return answer with citations
- [x] Set up environment variable loading (python-dotenv)
- [x] Create `.env.example` with required keys:
  - `OPENAI_API_KEY`
  - `PINECONE_API_KEY`
  - `PINECONE_ENVIRONMENT`
  - `JINA_API_KEY`
  - `GROQ_API_KEY`
- [x] Add Pydantic models for request/response validation
- [x] Test all endpoints with basic responses

**Deliverables**: Working FastAPI app with 3 endpoints, .env.example

---

## Phase 2: Chunking & Metadata
**Goal**: Implement text chunking logic with metadata preservation

### Chunking Strategy:
- **Method**: Hybrid sentence-based chunking with token limits
- **Chunk size**: 1000 tokens (using tiktoken with cl100k_base encoding)
- **Overlap**: 12% (120 tokens)
- **Metadata**: source, title, section, position (chunk index)

### Tasks:
- [x] Install tiktoken for token counting
- [x] Implement `chunker.py` service:
  - Split text into sentences
  - Group sentences into ~1000 token chunks
  - Add 120-token overlap between consecutive chunks
- [x] Attach metadata to each chunk:
  ```python
  {
    "text": "...",
    "source": "user_input",
    "title": "Document Title",
    "section": "Introduction",
    "position": 0,
    "token_count": 987
  }
  ```
- [x] Write unit tests for chunker:
  - Test overlap calculation
  - Test boundary conditions (very short/long text)
  - Verify metadata attachment
- [x] Integrate chunker into `/ingest` endpoint

**Deliverables**: Working chunker with tests, metadata schema

---

## Phase 3: Embeddings & Vector DB
**Goal**: Set up Pinecone index and implement embedding generation + storage

### Pinecone Configuration:
- **Dimension**: 1536 (for text-embedding-3-small)
- **Metric**: cosine
- **Index name**: `mini-rag-index`
- **Pod type**: starter (free tier)

### Tasks:
- [ ] Create Pinecone index via dashboard or API
- [ ] Implement `embedding_service.py`:
  - Generate embeddings using OpenAI API
  - Batch processing for multiple chunks
  - Error handling and retry logic
- [ ] Implement `vector_store.py`:
  - Upsert chunks with deterministic IDs (hash of text + metadata)
  - Store full metadata alongside vectors
- [ ] Update `/ingest` endpoint:
  - Accept text input
  - Chunk text
  - Generate embeddings
  - Upsert to Pinecone
  - Return success confirmation with chunk count
- [ ] Test ingestion with sample documents
- [ ] Verify vectors in Pinecone dashboard

**Deliverables**: Working ingestion pipeline, Pinecone index with test data

---

## Phase 4: Retrieval Strategy
**Goal**: Implement semantic search with MMR (Maximal Marginal Relevance)

### Retrieval Configuration:
- **Initial retrieval**: Top-20 chunks
- **Method**: MMR (diversity-aware retrieval)
- **Lambda**: 0.5 (balance relevance and diversity)

### Tasks:
- [ ] Implement `retrieval_service.py`:
  - Embed user query using same OpenAI model
  - Retrieve top-20 chunks from Pinecone with MMR
  - Include metadata and scores in results
- [ ] Add logging for retrieved chunks (for debugging)
- [ ] Create helper function to format retrieved chunks
- [ ] Test retrieval with various queries
- [ ] Verify diversity in retrieved results

**Deliverables**: Working retrieval service with MMR, logged outputs

---

## Phase 5: Reranking
**Goal**: Implement Jina Reranker to improve relevance of retrieved chunks

### Reranking Configuration:
- **Model**: Jina Reranker v2
- **Input**: Top-20 chunks from retrieval
- **Output**: Top-5 reranked chunks

### Tasks:
- [ ] Implement `reranker_service.py`:
  - Send query + retrieved chunks to Jina Reranker API
  - Parse relevance scores
  - Sort chunks by reranker score
  - Return top-5 chunks
- [ ] Add error handling for API failures (fallback to retrieval scores)
- [ ] Log reranker scores alongside retrieval scores
- [ ] Compare before/after reranking results
- [ ] Integrate reranker into query pipeline

**Deliverables**: Working reranker service, top-5 selection logic

---

## Phase 6: LLM Answering & Citations
**Goal**: Generate grounded answers with inline citations using Groq LLM

### Citation Format:
- Inline numeric citations: `[1]`, `[2]`, etc.
- Map to source snippets shown below answer
- Example: "The capital of France is Paris [1]."

### Tasks:
- [ ] Implement `llm_service.py`:
  - Construct grounded prompt with numbered sources
  - Call Groq API (llama-3.1-70b or mixtral-8x7b)
  - Parse response and extract answer
- [ ] Design prompt template:
  ```
  You are a helpful assistant. Answer the question based ONLY on the provided sources.
  Cite sources using [1], [2], etc.
  
  Sources:
  [1] {chunk_1_text}
  [2] {chunk_2_text}
  ...
  
  Question: {query}
  Answer:
  ```
- [ ] Implement citation extraction:
  - Parse `[1]`, `[2]` from answer
  - Map to chunk metadata
  - Return citations with source info
- [ ] Handle no-answer cases:
  - If LLM cannot answer from sources, return polite message
  - Example: "I cannot find a direct answer in the provided context."
- [ ] Update `/query` endpoint:
  - Accept query
  - Retrieve chunks
  - Rerank chunks
  - Generate answer with citations
  - Return answer + citations + source snippets

**Deliverables**: Complete query pipeline with LLM answering and citations

---

## Phase 7: Frontend Development
**Goal**: Build React frontend for text input, querying, and displaying results

### UI Components:
1. **Text Input Area**: Paste or type text to ingest
2. **Query Box**: Enter questions
3. **Answer Panel**: Display answer with inline citations
4. **Citations Panel**: Show source snippets with metadata
5. **Metrics Display**: Show latency and token/cost estimates

### Tasks:
- [ ] Initialize React app (Vite + TypeScript)
- [ ] Create layout with three sections:
  - Ingest panel (left/top)
  - Query panel (center)
  - Results panel (right/bottom)
- [ ] Implement `/ingest` UI:
  - Text area for input
  - Optional title/source fields
  - "Ingest" button
  - Success/error feedback
- [ ] Implement `/query` UI:
  - Query input box
  - "Ask" button
  - Loading state
- [ ] Implement results display:
  - Answer text with highlighted citations
  - Expandable source snippets
  - Citation links to sources
- [ ] Add metrics display:
  - Request latency (ms)
  - Token count estimate
  - Cost estimate (rough)
- [ ] Style with Tailwind CSS or similar
- [ ] Add error handling and loading states
- [ ] Make responsive for mobile

**Deliverables**: Working React frontend with all required features

---

## Phase 8: Hosting & Deployment
**Goal**: Deploy backend and frontend to free hosting platforms

### Backend Deployment (Render):
- [ ] Create `render.yaml` for backend service
- [ ] Set environment variables in Render dashboard
- [ ] Deploy FastAPI app
- [ ] Test all endpoints on hosted URL
- [ ] Enable CORS for frontend domain

### Frontend Deployment (Vercel):
- [ ] Create `vercel.json` configuration
- [ ] Set environment variable for backend API URL
- [ ] Deploy React app
- [ ] Test full flow on production URLs
- [ ] Verify API keys are NOT exposed in frontend

### Security:
- [ ] Ensure all API keys are server-side only
- [ ] Add rate limiting to prevent abuse
- [ ] Add input validation and sanitization
- [ ] Review CORS settings

**Deliverables**: Live URLs for frontend and backend, .env.example for local setup

---

## Phase 9: Evaluation & Documentation
**Goal**: Create evaluation dataset, test system, and write comprehensive README

### Evaluation (5 Q/A Pairs):
- [ ] Create gold dataset with:
  - Sample document
  - 5 questions with expected answers
  - Source citations for each answer
- [ ] Run queries through system
- [ ] Manually evaluate:
  - **Correctness**: Is the answer accurate?
  - **Completeness**: Are all relevant points covered?
  - **Citation Faithfulness**: Do citations match sources?
  - **No-hallucination**: Is everything grounded in sources?
- [ ] Calculate rough metrics:
  - Precision: % of correct facts in answer
  - Recall: % of expected facts included
  - Citation accuracy: % of correct citations
- [ ] Document results in `evaluation.md`

### README:
- [ ] Write comprehensive README.md with:
  - **Project Title & Description**
  - **Architecture Diagram** (system flow)
  - **Tech Stack** (with versions)
  - **Setup Instructions**:
    - Prerequisites
    - Installation steps
    - Environment variables
    - Database setup
  - **Quick Start Guide**:
    - Running locally
    - Ingesting documents
    - Querying
  - **Configuration**:
    - Chunking params (1000 tokens, 12% overlap)
    - Retrieval strategy (MMR, top-20)
    - Reranking (Jina, top-5)
    - LLM settings (Groq, model name)
  - **API Documentation**:
    - Endpoint descriptions
    - Request/response examples
  - **Deployment**:
    - Backend (Render)
    - Frontend (Vercel)
  - **Evaluation Results**:
    - Q/A pairs summary
    - Metrics
  - **Remarks**:
    - Limitations (token limits, cost constraints)
    - Trade-offs made (why these models/services)
    - Future improvements
  - **License & Credits**

### Architecture Diagram Elements:
```
User Input → FastAPI Backend
            ↓
    Chunking (1000 tokens, 12% overlap)
            ↓
    OpenAI Embeddings (text-embedding-3-small)
            ↓
    Pinecone Vector DB (upsert)

User Query → FastAPI Backend
            ↓
    OpenAI Embeddings (same model)
            ↓
    Pinecone Retrieval (MMR, top-20)
            ↓
    Jina Reranker (top-5)
            ↓
    Groq LLM (grounded prompt)
            ↓
    Answer + Citations → React Frontend
```

**Deliverables**: evaluation.md, complete README.md with diagram, remarks section

---

## Phase 10: Final Polish & Submission
**Goal**: Ensure all submission requirements are met

### Submission Checklist:
- [ ] Live URLs working without errors
- [ ] Public GitHub repository with:
  - Clean commit history
  - .gitignore (no API keys committed)
  - README with architecture diagram
  - .env.example
- [ ] README includes:
  - Setup instructions
  - Architecture diagram
  - Resume/portfolio link
- [ ] Index configuration documented (Pinecone settings)
- [ ] Remarks section complete:
  - Provider limits encountered
  - Trade-offs made
  - What you'd do next
- [ ] Test submission checklist:
  - Working URL ✓
  - Query flow works ✓
  - Minimal eval (5 Q/A pairs) ✓
  - README complete ✓

**Deliverables**: Submission-ready project

---

## Timeline Estimate
- **Phase 0-1**: 2-3 hours (setup)
- **Phase 2-3**: 3-4 hours (chunking + embeddings)
- **Phase 4-6**: 4-5 hours (retrieval + reranking + LLM)
- **Phase 7**: 4-6 hours (frontend)
- **Phase 8**: 2-3 hours (deployment)
- **Phase 9-10**: 3-4 hours (eval + docs)

**Total**: ~20-25 hours

---

## Key Decisions & Trade-offs

### Why these choices?
1. **Pinecone**: Free tier, managed service, MMR support
2. **OpenAI embeddings**: High quality, standard 1536 dimensions
3. **Jina Reranker**: Free tier available, good performance
4. **Groq**: Fast inference, free tier generous
5. **FastAPI**: Fast development, auto-generated docs
6. **React + Vite**: Modern, fast builds, good DX
7. **Render + Vercel**: Free tiers, easy deployment

### Trade-offs:
- **Free tier limits**: May need to add rate limiting
- **No auth**: Open to abuse, but simpler for demo
- **No file upload**: Text-only simplifies scope
- **Fixed chunk size**: Works for most content, but not optimal for all
- **No async processing**: Ingestion is synchronous, may timeout on large docs

### What's next (out of scope for v1):
- User authentication
- Multi-file upload support
- PDF/Word parsing
- Conversation history
- Advanced reranking (cross-encoder fine-tuning)
- Streaming responses
- Cost tracking dashboard
- A/B testing different retrieval strategies

---

## Resources & References
- [Pinecone Docs](https://docs.pinecone.io/)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [Jina Reranker](https://jina.ai/reranker/)
- [Groq API Docs](https://console.groq.com/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)

---

## Notes
- Keep API keys in environment variables only
- Log all retrieval/reranking scores for debugging
- Test with edge cases (very short queries, no-answer scenarios)
- Monitor API usage to stay within free tiers
- Use deterministic IDs for vector upserts (avoid duplicates)
