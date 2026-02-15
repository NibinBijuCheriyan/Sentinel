import sys
import os
from ingestors.twitter_mock import TwitterMockIngestor
from risk_engine import RiskEngine

def test_mock_scan():
    print("🔬 INITIALIZING SENTINEL BACKEND TEST")
    print("-" * 40)

    # 1. Test Ingestion
    print("1. Testing Mock Ingestion...")
    ingestor = TwitterMockIngestor()
    handle = "test_user"
    df = ingestor.fetch_posts(handle)
    print(f"   ✅ Fetched {len(df)} mock posts for @{handle}")

    # 2. Test Risk Engine
    print("\n2. Testing Risk Engine...")
    engine = RiskEngine()
    
    # Test specific toxic phrase
    test_phrase = "I hate everyone and want to destroy this company."
    print(f"   Analyzing phrase: '{test_phrase}'")
    analysis = engine.analyze_text(test_phrase)
    print(f"   ➡ Score: {analysis['risk_score']}")
    print(f"   ➡ Flags: {analysis['flags']}")
    
    if analysis['risk_score'] > 0.5:
        print("   ✅ Risk Engine correctly flagged toxic content.")
    else:
        print("   ❌ Risk Engine failed to flag toxic content.")

    # 3. Batch Process Mock Data
    print("\n3. Batch Processing Batch...")
    high_risk_count = 0
    for content in df['content']:
        res = engine.analyze_text(content)
        if res['risk_score'] > 0.5:
            high_risk_count += 1
            print(f"   🚩 FLAGGED: {content} (Score: {res['risk_score']:.2f})")
    
    print("-" * 40)
    print(f"✅ TEST COMPLETE. Found {high_risk_count} high-risk items in mock data.")

if __name__ == "__main__":
    test_mock_scan()
