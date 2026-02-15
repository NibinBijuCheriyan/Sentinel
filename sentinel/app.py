import streamlit as st
import pandas as pd
from datetime import datetime
from database import SessionLocal, Post, init_db
from ingestors.twitter_mock import TwitterMockIngestor
from ingestors.reddit import RedditIngestor
from risk_engine import RiskEngine
from fpdf import FPDF
import base64

# Page Config
st.set_page_config(page_title="Sentinel - Risk Intelligence", layout="wide", page_icon="🛡️")

# Initialize
if 'db_init' not in st.session_state:
    init_db()
    st.session_state['db_init'] = True

if 'risk_engine' not in st.session_state:
    st.session_state['risk_engine'] = RiskEngine()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Sidebar
st.sidebar.title("🛡️ Sentinel")
st.sidebar.info("Social Media Risk Intelligence")

# Tabs
tab1, tab2, tab3 = st.tabs(["📥 Content Intake", "🚨 Review Queue", "qh Reports"])

# --- TAB 1: INTAKE ---
with tab1:
    st.header("New Account Scan")
    
    col1, col2 = st.columns(2)
    with col1:
        source = st.selectbox("Platform", ["Twitter/X (Mock)", "Reddit"])
    with col2:
        handle = st.text_input("Username / Handle")

    # Reddit API Credentials (optional for demo if using mock)
    client_id = st.text_input("Reddit Client ID (Optional for Mock)", type="password")
    client_secret = st.text_input("Reddit Client Secret (Optional for Mock)", type="password")
    
    if st.button("Start Scan"):
        if not handle:
            st.error("Please enter a handle.")
        else:
            with st.spinner(f"Scanning {source} for @{handle}..."):
                # Select Ingestor
                ingestor = None
                if source == "Twitter/X (Mock)":
                    ingestor = TwitterMockIngestor()
                elif source == "Reddit":
                    if not client_id or not client_secret:
                        st.warning("Reddit API credentials required for real scan. Using Mock/Stub behavior if credentials fail.")
                    ingestor = RedditIngestor(client_id=client_id, client_secret=client_secret, user_agent="Sentinel/1.0")

                # Fetch Posts
                df = ingestor.fetch_posts(handle)
                
                if df.empty:
                    st.warning("No posts found or access denied.")
                else:
                    st.success(f"Fetched {len(df)} posts.")
                    
                    # Analyze and Store
                    db = SessionLocal()
                    risk_engine = st.session_state['risk_engine']
                    
                    progress_bar = st.progress(0)
                    for i, row in df.iterrows():
                        # Analyze
                        analysis = risk_engine.analyze_text(row['content'])
                        
                        # Store in DB (Check duplicate first)
                        existing = db.query(Post).filter(Post.url == row['url']).first()
                        if not existing:
                            new_post = Post(
                                source=row['source'],
                                handle=row['handle'],
                                date=row['date'],
                                content=row['content'],
                                url=row['url'],
                                risk_score=analysis['risk_score'],
                                flags=",".join(analysis['flags']),
                                reviewed=False
                            )
                            db.add(new_post)
                        
                        progress_bar.progress((i + 1) / len(df))
                    
                    db.commit()
                    db.close()
                    st.success("Analysis Complete. Check Review Queue.")

# --- TAB 2: REVIEW QUEUE ---
with tab2:
    st.header("Risk Review Queue")
    
    db = SessionLocal()
    # Filters
    min_score = st.slider("Minimum Risk Score", 0.0, 1.0, 0.0)
    show_reviewed = st.checkbox("Show Reviewed Posts", value=False)
    
    query = db.query(Post).filter(Post.risk_score >= min_score)
    if not show_reviewed:
        query = query.filter(Post.reviewed == False)
        
    posts = query.order_by(Post.risk_score.desc()).all()
    
    st.metric("Pending Reviews", len(posts))
    
    for post in posts:
        with st.expander(f"🔴 [{post.risk_score:.2f}] {post.source} @{post.handle}: {post.content[:50]}..."):
            st.write(f"**Content:** {post.content}")
            st.write(f"**Flags:** {post.flags}")
            st.write(f"**Date:** {post.date}")
            st.markdown(f"[Link]({post.url})")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Mark Safe / False Positive", key=f"safe_{post.id}"):
                    post.reviewed = True
                    post.reviewer_notes = "Marked Safe"
                    db.commit()
                    st.rerun()
            with col2:
                if st.button("Confirm Risk", key=f"risk_{post.id}"):
                    post.reviewed = True
                    post.reviewer_notes = "Confirmed Risk"
                    db.commit()
                    st.rerun()
    
    db.close()

# --- TAB 3: REPORTS ---
with tab3:
    st.header("Generate Report")
    
    if st.button("Download PDF Report"):
        db = SessionLocal()
        high_risk = db.query(Post).filter(Post.risk_score >= 0.7).all()
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        pdf.cell(200, 10, txt="Sentinel Risk Report", ln=1, align='C')
        pdf.cell(200, 10, txt=f"Generated: {datetime.now()}", ln=1, align='C')
        pdf.ln(10)
        
        for post in high_risk:
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(200, 10, txt=f"Risk Score: {post.risk_score:.2f} | Handle: @{post.handle} ({post.source})", ln=1)
            pdf.set_font("Arial", size=10)
            try:
                # Basic sanitization for PDF (latin-1)
                content = post.content.encode('latin-1', 'replace').decode('latin-1')
                pdf.multi_cell(0, 10, txt=f"Content: {content}")
                pdf.cell(200, 10, txt=f"Flags: {post.flags}", ln=1)
                pdf.ln(5)
            except Exception as e:
                pass
                
        # Save to temp file matching known path or just return bytes?
        # Streamlit download button needs bytes
        # pyFPDF's output() returns string in Py2, bytes/string in Py3 depending on args.
        # We'll save to a file for simplicity.
        pdf.output("report.pdf")
        
        with open("report.pdf", "rb") as f:
            st.download_button("Download PDF", f, file_name="sentinel_report.pdf")
        
        db.close()
