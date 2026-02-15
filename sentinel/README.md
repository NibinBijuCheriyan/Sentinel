# Sentinel - Social Media Risk Intelligence 🛡️

**Sentinel** is a risk-monitoring system for HR and Compliance teams. It ingests public posts from social media (Reddit, Twitter/X), analyzes them for toxicity and high-risk keywords, and presents a dashboard for human review.

## Features
- **Multi-Platform Ingestion**: Support for Reddit (via PRAW) and Mock Twitter (for demo).
- **Risk Engine**: Uses `unitary/toxic-bert` for ML-based toxicity detection + Regex for keyword matching.
- **Review Dashboard**: Streamlit interface to review, flag, or dismiss posts.
- **PDF Reporting**: Export high-risk posts for external reporting.

## 🚀 Quick Start (Local)

### Prerequisites
- Python 3.8+
- Git

### Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd sentinel
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Dashboard**:
    ```bash
    streamlit run app.py
    ```
    Access the app at `http://localhost:8501`.

## 🐳 Running with Docker

1.  **Build the image**:
    ```bash
    docker build -t sentinel .
    ```

2.  **Run the container**:
    ```bash
    docker run -p 8501:8501 sentinel
    ```

## Usage
1.  **Scan**: Go to the "Content Intake" tab, select a source (e.g., Reddit), and enter a username.
2.  **Review**: Check the "Review Queue" for flagged items.
3.  **Report**: Generate a PDF summary in the "Reports" tab.

## Disclaimer
Sentinel is an internal tool for risk awareness. It does not replace human judgment.
