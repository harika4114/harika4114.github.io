# Vidya Margam (విద్యా మార్గం)

A Telugu-language AI assistant helping first-generation college students in Telangana navigate admissions, scholarships, and hostel applications.

## Google tech stack
- **Gemini 1.5 Pro API** — multilingual reasoning and Telugu response generation
- **Vertex AI Search** — RAG over indexed TS ePASS, TSBIE, and welfare scheme documents
- **Google Search grounding** — live deadlines and updated scheme info
- **Cloud Translation API** — Telugu/English normalisation
- **Firebase** (Auth + Firestore) — phone-based auth, conversation history
- **Cloud Functions** — serverless backend orchestration

---

## Project structure

```
vidya-margam/
├── backend/
│   └── functions/
│       ├── main.py           # Cloud Function entry point
│       └── requirements.txt
└── frontend/
    └── src/
        └── App.jsx           # React chat UI
```

---

## Setup

### 1. Google Cloud setup
```bash
# Create project
gcloud projects create vidya-margam --name="Vidya Margam"
gcloud config set project vidya-margam

# Enable APIs
gcloud services enable \
  aiplatform.googleapis.com \
  translate.googleapis.com \
  discoveryengine.googleapis.com \
  cloudfunctions.googleapis.com \
  firebase.googleapis.com
```

### 2. Vertex AI Search — index your documents
1. Go to Vertex AI Search in Cloud Console
2. Create a new Search app → Document search
3. Upload PDFs: TS ePASS guidelines, TSBIE circulars, BC/SC Welfare scheme docs
4. Copy the Datastore ID into your environment variables

### 3. Deploy the Cloud Function
```bash
cd backend/functions

gcloud functions deploy vidya_margam \
  --runtime python311 \
  --trigger-http \
  --allow-unauthenticated \
  --set-env-vars GCP_PROJECT=vidya-margam,DATASTORE_ID=your-datastore-id \
  --set-secrets GEMINI_API_KEY=gemini-api-key:latest
```

### 4. Run the frontend
```bash
cd frontend
npm install
npm run dev
```

Update `BACKEND_URL` and `firebaseConfig` in `App.jsx` with your actual values.

---

## Sample queries (Telugu)
- నాకు BC scholarship కి ఎలా apply చేయాలి?
- EAMCET counselling కి ఏ documents కావాలి?
- Government hostel కి ఎలా apply చేయాలి?
- Fee reimbursement last date ఎప్పుడు?

---

Built for Gen AI Academy APAC — Meet the Builders campaign.
