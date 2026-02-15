import re
import torch
from transformers import pipeline

class RiskEngine:
    def __init__(self):
        # Load toxicity model (lightweight if possible, or use API)
        # Using a small BERT model for toxicity
        try:
            self.toxicity_pipeline = pipeline("text-classification", model="unitary/toxic-bert", top_k=None)
        except Exception as e:
            print(f"Error loading model: {e}")
            self.toxicity_pipeline = None

        self.sensitive_keywords = [
            "hate", "kill", "attack", "stupid", "idiot", "destroy", "leaked", "confidential", 
            # Add more specific risk keywords here
        ]
        
    def analyze_text(self, text: str) -> dict:
        result = {
            "risk_score": 0.0,
            "flags": [],
            "sentiment": "Neutral"
        }
        
        if not text:
            return result
            
        # 1. Keyword Matching
        for keyword in self.sensitive_keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text.lower()):
                result["flags"].append(f"Keyword: {keyword}")
                result["risk_score"] += 0.3

        # 2. ML Toxicity Analysis
        if self.toxicity_pipeline:
            try:
                # Truncate text to 512 tokens approx
                analysis = self.toxicity_pipeline(text[:512])
                # analysis is list of lists [[{'label': 'toxic', 'score': 0.9}, ...]]
                for item in analysis[0]:
                    if item['label'] == 'toxic' and item['score'] > 0.7:
                        result["flags"].append("ML: Toxic")
                        result["risk_score"] += item['score']
                    elif item['label'] == 'severe_toxic' and item['score'] > 0.5:
                        result["flags"].append("ML: Severe Toxic")
                        result["risk_score"] += item['score'] * 1.5
            except Exception as e:
                print(f"Analysis error: {e}")

        # Cap score
        result["risk_score"] = min(result["risk_score"], 1.0)
        
        return result
