# Kanun (قانون) - Citizen Legal Empowerment & Knowledge Engine

A civic tech platform that converts Pakistani legal documents into a searchable vector database, providing plain-language legal answers in English and Roman Urdu.

## Features

- **Natural Language Search**: Ask legal questions in plain English
- **Plain-Language Answers**: AI-powered explanations of complex legal jargon
- **Roman Urdu Support**: Legal answers in Roman Urdu for wider accessibility
- **Comprehensive Database**: 958+ federal laws, Constitution, PPC, CrPC
- **Contributor System**: Community-driven content submission
- **Daily Automation**: Automatic detection of new laws and regulations

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python FastAPI |
| **Frontend** | React + Vite + Tailwind CSS |
| **Vector DB** | Qdrant (self-hosted) |
| **Database** | PostgreSQL 16 |
| **Embeddings** | BAAI/bge-base-en-v1.5 (local) |
| **LLM** | LiteLLM + OpenAI API |
| **Storage** | Cloudflare R2 |

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (for Qdrant)
- PostgreSQL 16

### Installation

```bash
# Clone the repository
git clone https://github.com/TahaKhan556/pak-legal-engine.git
cd pak-legal-engine

# Start Qdrant and Redis
docker compose up -d

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create database
createdb pak_legal

# Run migrations
alembic upgrade head

# Ingest dataset
python -m app.tasks.bulk_ingestion

# Start backend
python run.py

# Frontend setup (new terminal)
cd frontend
npm install
npm run dev
```

### Environment Variables

Copy `.env.example` to `.env` and fill in:

```bash
cp .env.example .env
```

## Data Sources

| Source | Content | Records |
|--------|---------|---------|
| HuggingFace ipfs_pakistan_laws | Federal laws with article-level breakdown | 958 laws |
| Pakistan Code | Official federal legislation | 600+ laws |
| KP Code | Khyber Pakhtunkhwa provincial laws | 572 laws |
| Sindh Assembly | Sindh provincial acts | 60+ recent acts |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/search` | Natural language search |
| `GET` | `/api/v1/documents` | List documents |
| `GET` | `/api/v1/documents/stats` | Get statistics |
| `POST` | `/api/v1/contribute` | Submit content |
| `GET` | `/api/v1/admin/dashboard` | Admin dashboard |

## Deployment

### VPS Deployment

```bash
# Install dependencies
npm install -g pm2

# Start services
pm2 start ecosystem.config.js

# Configure nginx
sudo cp nginx/kanun.8.jugaar.ai.conf /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# Get SSL certificate
sudo certbot --nginx -d kanun.8.jugaar.ai
```

## Project Structure

```
pak-legal-engine/
├── backend/           # FastAPI backend
│   ├── app/          # Application code
│   ├── scrapers/      # Web scrapers
│   └── tasks/         # Background tasks
├── frontend/         # React frontend
│   └── src/          # Source code
├── scrapers/         # Official source scrapers
├── nginx/            # Nginx configs
└── docker-compose.yml
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Pakistan Code (pakistancode.gov.pk) for official legal documents
- HuggingFace datasets for pre-cleaned legal data
- The civic tech community in Pakistan
