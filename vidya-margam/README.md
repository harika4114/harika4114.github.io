# Vidya Margam - AI-Powered Educational Platform

An intelligent educational platform combining Google Translate API, Vertex AI Search (RAG), and Gemini to provide context-aware answers with multi-language support.

## 🚀 Features

- **Real-time Translation**: Seamlessly communicate in multiple languages (Telugu, Hindi, English, etc.)
- **RAG-Enhanced Responses**: Document-grounded answers using Vertex AI Search
- **Intelligent Chat**: Google Gemini 2.0 with Search grounding for accurate, sourced responses
- **Cloud-Native**: Serverless backend on Google Cloud Functions
- **React Frontend**: Modern UI with real-time streaming and Firebase integration

## 📋 Prerequisites

- Google Cloud Project with billing enabled
- Node.js 18+ and Python 3.10+
- Firebase project
- The following GCP APIs enabled:
  - Cloud Translation API
  - Vertex AI Search API
  - Cloud Functions API
  - Generative AI API

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/vidya-margam.git
cd vidya-margam
```

### 2. Set Up GCP APIs

```bash
export PROJECT_ID="your-gcp-project-id"
export REGION="us-central1"

gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable translate.googleapis.com
gcloud services enable discoveryengine.googleapis.com
gcloud services enable generativelanguage.googleapis.com
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 3. Create Vertex AI Search Datastore

```bash
# Upload your educational PDFs to Vertex AI Search
# Get your Datastore ID from the console
export DATASTORE_ID="your-datastore-id"
```

### 4. Deploy Backend Cloud Function

```bash
cd backend/functions

# Install dependencies
pip install -r requirements.txt

# Deploy the function
gcloud functions deploy vidya-margam-handler \
  --runtime python311 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point handle_request \
  --set-env-vars PROJECT_ID=$PROJECT_ID,DATASTORE_ID=$DATASTORE_ID,REGION=$REGION
```

### 5. Set Up Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local with Firebase config
cat > .env.local << 'EOF'
VITE_FIREBASE_API_KEY=your-api-key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VITE_FIREBASE_APP_ID=your-app-id
VITE_FUNCTION_URL=https://your-region-your-project-id.cloudfunctions.net/vidya-margam-handler
EOF

# Start development server
npm run dev
```

## 📁 Project Structure

```
vidya-margam/
├── backend/
│   └── functions/
│       ├── main.py
│       └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── ...
│   ├── package.json
│   └── vite.config.js
├── vidya-margam-blog/
│   ├── _config.yml
│   ├── _posts/
│   └── index.md
└── README.md
```

## 🔑 Environment Variables

**Backend (.env or Cloud Function env vars):**
- `PROJECT_ID`: Your GCP project ID
- `DATASTORE_ID`: Vertex AI Search Datastore ID
- `REGION`: GCP region (e.g., us-central1)

**Frontend (.env.local):**
- All `VITE_FIREBASE_*` variables
- `VITE_FUNCTION_URL`: Cloud Function endpoint

## 🎯 How It Works

1. **User Input**: Student asks a question in their preferred language
2. **Translation**: Question translated to English for processing
3. **RAG Retrieval**: Vertex AI Search finds relevant educational materials
4. **LLM Processing**: Gemini generates answer grounded in retrieved documents
5. **Response Translation**: Answer translated back to student's language
6. **Delivery**: Real-time streaming response in the chat interface

## 📚 API Documentation

### Cloud Function Endpoint

**POST** `/vidya-margam-handler`

```json
{
  "question": "What is photosynthesis?",
  "language": "te",
  "userId": "user123"
}
```

**Response:**
```json
{
  "answer": "Photosynthesis is...",
  "sources": ["PDF: Chapter 5.pdf", "PDF: Chapter 6.pdf"],
  "language": "te"
}
```

## 🚢 Deployment

### Deploy to Firebase Hosting (Frontend)

```bash
cd frontend
npm run build
firebase deploy --only hosting
```

### Update Cloud Function

```bash
cd backend/functions
gcloud functions deploy vidya-margam-handler --runtime python311
```

## 📝 Blog

Read about the development journey in the [Vidya Margam Blog](./vidya-margam-blog/index.md)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Google Cloud for AI/ML APIs
- Firebase for backend services
- React community for excellent tooling

---

**Made with ❤️ to make education accessible to everyone**
