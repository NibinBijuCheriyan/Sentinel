# Sentinel

Social Media Risk Intelligence Platform

---

## Overview

Sentinel is a risk intelligence system designed for HR and compliance teams. It ingests public social media content for a specified user handle, processes each post through a multi-layered analysis engine combining machine learning and rule-based classification, and surfaces flagged content in a prioritized review queue. Completed reviews can be exported as a downloadable PDF report.

The platform ships with a live Reddit integration and a mock Twitter/X ingestor for demonstration purposes.

---

## Table of Contents

- [Architecture](#architecture)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Running with Docker](#running-with-docker)
- [Testing](#testing)
- [License](#license)

---

## Architecture

```
User Input (Handle + Platform)
        |
        v
+-------------------+
|    Ingestors       |
|  Twitter/X (Mock)  |
|  Reddit (Live)     |
+-------------------+
        |
        v
+-------------------+
|   Risk Engine      |
|  Keyword Matching  |
|  BERT Toxicity ML  |
+-------------------+
        |
        v
+-------------------+
|    Database        |
|  SQLite + ORM      |
+-------------------+
        |
        v
+-------------------+
|    Dashboard       |
|  Content Intake    |
|  Review Queue      |
|  PDF Reports       |
+-------------------+
```

---

## Key Features

**Multi-Platform Data Ingestion**
Modular ingestor system built on a shared base class interface. The Twitter/X mock ingestor generates realistic sample data for development and demonstration. The Reddit ingestor connects to the Reddit API via PRAW and retrieves a user's recent comments and submissions.

**ML-Powered Risk Scoring**
The risk engine uses the `unitary/toxic-bert` model from Hugging Face Transformers for toxicity classification. ML predictions are combined with rule-based keyword matching against a configurable list of sensitive terms. The final composite score is normalized to a 0.0--1.0 range.

**Prioritized Review Queue**
Posts are displayed in descending order of risk score. Reviewers can filter by minimum score threshold and toggle between pending and reviewed items. Each post can be marked as a false positive (safe) or confirmed risk, with reviewer notes persisted to the database.

**PDF Report Generation**
A one-click export generates a formatted PDF document containing all posts with a risk score at or above 0.70. The report includes timestamps, source metadata, content excerpts, and flag details.

**Duplicate Detection**
Ingested posts are deduplicated by URL before storage, preventing redundant entries when the same handle is scanned multiple times.

---

## Technology Stack

| Component          | Technology                                       |
|--------------------|--------------------------------------------------|
| Frontend           | Streamlit 1.31+                                  |
| ML Pipeline        | PyTorch 2.0+, Hugging Face Transformers 4.30+    |
| Data Ingestion     | PRAW 7.7+ (Reddit API)                           |
| Database           | SQLite via SQLAlchemy 2.0+                        |
| Reporting          | FPDF 1.7+                                        |
| Data Processing    | pandas 2.2+, scikit-learn 1.3+, matplotlib 3.8+  |
| Containerization   | Docker (Python 3.9-slim base)                     |

---

## Project Structure

```
sentinel/
├── app.py                  # Streamlit application entry point
│                           # Three tabs: Content Intake, Review Queue, Reports
├── risk_engine.py          # Risk analysis engine
│                           # BERT toxicity model + keyword matching
├── database.py             # SQLAlchemy ORM models and session factory
│                           # Post model with risk metadata fields
├── ingestors/
│   ├── __init__.py         # Package initialization and exports
│   ├── base.py             # Abstract base class for all ingestors
│   ├── reddit.py           # Live Reddit ingestor using PRAW
│   └── twitter_mock.py     # Mock Twitter/X ingestor with sample data
├── test_backend.py         # Backend integration test suite
├── requirements.txt        # Python dependency manifest
└── Dockerfile              # Container build configuration
```

---

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Docker (optional, for containerized deployment)
- Reddit API credentials (optional, only required for live Reddit scanning)

---

## Installation

1. Clone the repository and navigate to the Sentinel directory:

    ```bash
    cd sentinel
    ```

2. Create and activate a virtual environment (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate        # Linux / macOS
    venv\Scripts\activate           # Windows
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

> Note: The `unitary/toxic-bert` model will be downloaded automatically on first launch. This requires an active internet connection and approximately 500 MB of disk space.

---

## Configuration

**Reddit API Credentials**

Reddit credentials are entered directly in the Streamlit interface at scan time. No environment files or configuration files are required for the mock Twitter ingestor.

To use the live Reddit ingestor:

1. Create or log in to a Reddit account.
2. Navigate to [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps).
3. Register a new application (select "script" as the type).
4. Copy the generated Client ID and Client Secret.
5. Enter both values in the Sentinel UI when performing a Reddit scan.

**Database**

Sentinel uses a local SQLite database (`sentinel.db`) created automatically at first launch. No external database server is required.

---

## Usage

Start the application:

```bash
streamlit run app.py
```

The dashboard will be available at `http://localhost:8501`.

**Workflow:**

1. **Content Intake** -- Select a platform (Twitter/X Mock or Reddit), enter a username, and initiate a scan. Posts are fetched, analyzed, and stored in the database.
2. **Review Queue** -- Filter results by minimum risk score. Review each flagged post and mark it as safe or confirmed risk.
3. **Reports** -- Generate and download a PDF report of all high-risk posts (score >= 0.70).

---

## Running with Docker

Build and run the container:

```bash
docker build -t sentinel .
docker run -p 8501:8501 sentinel
```

The application will be available at `http://localhost:8501`.

To pre-download the ML model during build (recommended for production), uncomment the corresponding line in the `Dockerfile`:

```dockerfile
RUN python -c "from transformers import pipeline; pipeline('text-classification', model='unitary/toxic-bert')"
```

---

## Testing

Run the backend integration test to validate the ingestion and risk analysis pipeline without launching the full UI:

```bash
python test_backend.py
```

This test performs the following:

1. Initializes the mock Twitter ingestor and fetches sample posts.
2. Loads the risk engine and analyzes a known toxic phrase.
3. Batch-processes the full mock dataset and reports the number of flagged items.

---

## License

This project is provided as-is for educational and internal use. No license file is currently included. Contact the repository owner for licensing inquiries.
