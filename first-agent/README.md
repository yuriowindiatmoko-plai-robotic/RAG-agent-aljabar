============================================================  
 🍽️ FIXED RAG PIPELINE WITH DATA LOADING
============================================================
🚀 Initializing RAG Pipeline...
✓ Loading embedding model...
Embedding dimension: 384
✓ Configuring Gemini API...
Using model: gemini-2.5-flash-lite
✓ Connecting to PostgreSQL...
Connected successfully
✓ Setting up database...
Installing pgvector extension...
Table exists, checking schema...
Table created/verified
✅ RAG Pipeline initialized!

    📊 Current documents in database: 1

    📝 Clearing existing documents and reloading fresh data...
      ✓ Cleared 1 old documents
    📥 Loading new sample documents...

    📥 Loading 15 documents...
      ✓ Loaded 5/15 documents...
      ✓ Loaded 10/15 documents...
      ✓ Loaded 15/15 documents...
    ✅ Successfully loaded 15/15 documents

    📊 Final document count: 15

    ============================================================
    TESTING RAG PIPELINE
    ============================================================

    📝 Question: What are the main causes of climate change?
    ✓ Retrieved 3 documents
      1. Climate Change Causes (similarity: 0.778)
      2. Renewable Energy Sources (similarity: 0.341)
      3. Git Version Control (similarity: 0.156)
    🤖 Generating answer...

    ============================================================
    Answer: The main causes of climate change are:

    1.  Burning fossil fuels (coal, oil, gas) for energy
    2.  Industrial processes and manufacturing
    3.  Deforestation and land use changes
    4.  Agriculture and livestock farming
    5.  Transportation and vehicle emissions

    📝 Question: How does React work for web development?
    ✓ Retrieved 3 documents
      1. Web Development with React (similarity: 0.745)
      2. Python Programming (similarity: 0.241)
      3. Natural Language Processing (similarity: 0.225)
    🤖 Generating answer...

    ============================================================
    Answer: React is a JavaScript library for building user interfaces, maintained by Meta. It enables creating interactive, dynamic web applications with
     a component-based architecture. Key concepts include components, JSX, state management, props, hooks, and the Virtual DOM for efficient rendering.

    📝 Question: What is Docker and why use containers?
    ✓ Retrieved 3 documents
      1. Docker and Containers (similarity: 0.789)
      2. Kubernetes Orchestration (similarity: 0.516)
      3. API Development with FastAPI (similarity: 0.243)
    🤖 Generating answer...

    ============================================================
    Answer: Docker is a platform for developing, shipping, and running applications in containers. Containers offer several benefits, including
    portability (runs anywhere Docker is installed), isolation (separate environments for each app), efficiency (lightweight compared to VMs), consistency
     (same environment across dev/prod), and scalability (easy to scale horizontally).

    📝 Question: Tell me about neural networks
    ✓ Retrieved 3 documents
      1. Neural Networks Explained (similarity: 0.763)
      2. Machine Learning Basics (similarity: 0.581)
      3. Natural Language Processing (similarity: 0.298)
    🤖 Generating answer...
    Error generating answer: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to:
     https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit.
    * Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 20, model: gemini-2.5-flash-lite
    Please retry in 36.585692118s. [links {
      description: "Learn more about Gemini API quotas"
      url: "https://ai.google.dev/gemini-api/docs/rate-limits"
    }
    , violations {
      quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
      quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
      quota_dimensions {
        key: "model"
        value: "gemini-2.5-flash-lite"
      }
      quota_dimensions {
        key: "location"
        value: "global"
      }
      quota_value: 20
    }
    , retry_delay {
      seconds: 36
    }
    ]

    ============================================================
    Answer: Unable to generate answer

    📝 Question: How does Kubernetes help with container orchestration?
    ✓ Retrieved 3 documents
      1. Kubernetes Orchestration (similarity: 0.745)
      2. Docker and Containers (similarity: 0.540)
      3. Cloud Computing with AWS (similarity: 0.272)
    🤖 Generating answer...
    Error generating answer: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to:
     https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit.
    * Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 20, model: gemini-2.5-flash-lite
    Please retry in 36.456254704s. [links {
      description: "Learn more about Gemini API quotas"
      url: "https://ai.google.dev/gemini-api/docs/rate-limits"
    }
    , violations {
      quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
      quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
      quota_dimensions {
        key: "model"
        value: "gemini-2.5-flash-lite"
      }
      quota_dimensions {
        key: "location"
        value: "global"
      }
      quota_value: 20
    }
    , retry_delay {
      seconds: 36
    }
    ]

    ============================================================
    Answer: Unable to generate answer

    📝 Question: What are the main AWS cloud services?
    ✓ Retrieved 3 documents
      1. Cloud Computing with AWS (similarity: 0.820)
      2. Kubernetes Orchestration (similarity: 0.445)
      3. Docker and Containers (similarity: 0.321)
    🤖 Generating answer...
    Error generating answer: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to:
     https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit.
    * Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 20, model: gemini-2.5-flash-lite
    Please retry in 36.284266843s. [links {
      description: "Learn more about Gemini API quotas"
      url: "https://ai.google.dev/gemini-api/docs/rate-limits"
    }
    , violations {
      quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
      quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
      quota_dimensions {
        key: "model"
        value: "gemini-2.5-flash-lite"
      }
      quota_dimensions {
        key: "location"
        value: "global"
      }
      quota_value: 20
    }
    , retry_delay {
      seconds: 36
    }
    ]

    ============================================================
    Answer: Unable to generate answer

    📝 Question: How does Git version control work?
    ✓ Retrieved 3 documents
      1. Git Version Control (similarity: 0.738)
      2. Docker and Containers (similarity: 0.185)
      3. Kubernetes Orchestration (similarity: 0.184)
    🤖 Generating answer...
    Error generating answer: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to:
     https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit.
    * Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 20, model: gemini-2.5-flash-lite
    Please retry in 36.143388502s. [links {
      description: "Learn more about Gemini API quotas"
      url: "https://ai.google.dev/gemini-api/docs/rate-limits"
    }
    , violations {
      quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
      quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
      quota_dimensions {
        key: "model"
        value: "gemini-2.5-flash-lite"
      }
      quota_dimensions {
        key: "location"
        value: "global"
      }
      quota_value: 20
    }
    , retry_delay {
      seconds: 36
    }
    ]

    ============================================================
    Answer: Unable to generate answer

    📝 Question: Explain FastAPI for building APIs
    ✓ Retrieved 3 documents
      1. API Development with FastAPI (similarity: 0.772)
      2. Python Programming (similarity: 0.255)
      3. Web Development with React (similarity: 0.235)
    🤖 Generating answer...
    Error generating answer: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to:
     https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit.
    * Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 20, model: gemini-2.5-flash-lite
    Please retry in 35.980731484s. [links {
      description: "Learn more about Gemini API quotas"
      url: "https://ai.google.dev/gemini-api/docs/rate-limits"
    }
    , violations {
      quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
      quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
      quota_dimensions {
        key: "model"
        value: "gemini-2.5-flash-lite"
      }
      quota_dimensions {
        key: "location"
        value: "global"
      }
      quota_value: 20
    }
    , retry_delay {
      seconds: 35
    }
    ]

    ============================================================
    Answer: Unable to generate answer

    ✅ RAG Pipeline test completed!
    /home/yurio/Public/PROJECT/RAG-AGENT-ALJABAR/first-agent/fix_rag_pipeline.py:15: FutureWarning:

    All support for the `google.generativeai` package has ended. It will no longer be receiving
    updates or bug fixes. Please switch to the `google.genai` package as soon as possible.
    See README for more details:

    https://github.com/google-gemini/deprecated-generative-ai-python/blob/main/README.md

      import google.generativeai as genai
    WARNING:  database "boilerplate_db" has a collation version mismatch
    DETAIL:  The database was created using collation version 2.41, but the operating system provides version 2.36.
    HINT:  Rebuild all objects in this database that use the default collation and run ALTER DATABASE boilerplate_db REFRESH COLLATION VERSION, or build
    PostgreSQL with the right library version.

The RAG pipeline is working great! The retrieval is finding the right documents with high similarity scores:- Climate Change query found "Climate Change
Causes" (0.778 similarity)

- React query found "Web Development with React" (0.745 similarity)
- Docker query found "Docker and Containers" (0.789 similarity)
- Neural Networks query found "Neural Networks Explained" (0.763 similarity)
- Kubernetes query found "Kubernetes Orchestration" (0.745 similarity)
- AWS query found "Cloud Computing with AWS" (0.820 similarity)
- Git query found "Git Version Control" (0.738 similarity)
- FastAPI query found "API Development with FastAPI" (0.772 similarity)The first 3 answers were successfully generated! The remaining ones failed due to
  hitting the Gemini API rate limit (20 requests/day for free tier).Let me mark the todo as completed and summarize the results for the user.

● RAG Pipeline is working! 🎉

The retrieval system is finding the correct documents with high similarity scores:

- Climate Change → 0.778 similarity
- React → 0.745 similarity
- Docker → 0.789 similarity
- Neural Networks → 0.763 similarity
- Kubernetes → 0.745 similarity
- AWS → 0.820 similarity
- Git → 0.738 similarity
- FastAPI → 0.772 similarity

The first 3 queries successfully generated answers! The rest hit the Gemini API free tier rate limit (20 requests/day).

a summary of what was accomplished and the current status.

Here's what fix:

1. Database Schema Issue - Added UNIQUE constraint to title column so ON CONFLICT works properly
2. Duplicate Load Call - Removed duplicate load_documents() call
3. Fixed get_document_count() - Now returns integer instead of tuple
4. Added 15 diverse documents covering:

   - Climate Change, Renewable Energy
   - Machine Learning, Neural Networks, NLP
   - Python, React, FastAPI
   - Docker, Kubernetes
   - AWS, Databases, Git
   - Data Science (Pandas)
   - Cybersecurity

Current Issues

| Issue                          | Severity | Fix                                                           |
| ------------------------------ | -------- | ------------------------------------------------------------- |
| Gemini API quota exceeded      | Warning  | Free tier: 20 requests/day. Wait ~36s or upgrade              |
| Deprecated google.generativeai | Warning  | Should migrate to google.genai                                |
| DB collation mismatch          | Info     | Run: ALTER DATABASE boilerplate_db REFRESH COLLATION VERSION; |

The RAG retrieval is working perfectly - it's finding relevant documents with high similarity scores! The LLM generation also works
(proved by first 3 successful answers). You just need to wait for the rate limit to reset or add rate limiting/retry logic.
