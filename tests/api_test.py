import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import kagglehub
import pandas as pd
from main import analyze_text
import random

def load_mixed_data():
    print("Loading data from multiple sources...")
    
    # Load Kaggle data (for human texts)
    print("1. Loading Kaggle human texts...")
    path = kagglehub.dataset_download("shanegerami/ai-vs-human-text")
    
    import os
    files = os.listdir(path)
    kaggle_csv = [f for f in files if f.endswith('.csv')][0]
    
    kaggle_df = pd.read_csv(os.path.join(path, kaggle_csv))
    human_texts_all = kaggle_df[kaggle_df['generated'] == 0]['text'].tolist()
    
    # Load your ChatGPT AI texts
    print("2. Loading ChatGPT AI texts...")
    ai_df = pd.read_csv('csv/ai_texts_50.csv')  # Adjust filename if needed
    ai_texts_all = ai_df['text'].tolist()  # Adjust column name if needed
    
    print(f"Found {len(human_texts_all)} human texts from Kaggle")
    print(f"Found {len(ai_texts_all)} AI texts from ChatGPT")
    
    # Sample equal amounts for fair testing
    sample_size = min(500, len(human_texts_all), len(ai_texts_all))
    
    human_sample = random.sample(human_texts_all, sample_size)
    ai_sample = ai_texts_all[:sample_size]  # Use all your ChatGPT texts
    
    print(f"Testing with {len(human_sample)} human + {len(ai_sample)} AI texts")
    
    return human_sample, ai_sample

def test_ai_detection_accuracy():
    print("Loading mixed data...")
    human_texts, ai_texts = load_mixed_data()
    
    correct_predictions = 0
    total_predictions = 0
    
    # ✅ ADDED: Lists to track all scores
    ai_scores = []
    human_scores = []
    
    # Test human texts (should be classified as human)
    print("\n=== TESTING HUMAN TEXTS (From Kaggle) ===")
    human_correct = 0
    for i, text in enumerate(human_texts):
        try:
            result = analyze_text(text)
            predicted_score = float(result[1])
            
            # ✅ ADDED: Store human scores
            human_scores.append(predicted_score)
            
            is_predicted_ai = predicted_score >= 0.99962
            
            if not is_predicted_ai:  # Correctly identified as human
                correct_predictions += 1
                human_correct += 1
            
            total_predictions += 1
            status = "✅ CORRECT" if not is_predicted_ai else "❌ WRONG"
            print(f"Human {i+1}: Score={predicted_score:.6f}, Predicted={'AI' if is_predicted_ai else 'Human'} {status}")
            
        except Exception as e:
            print(f"Error on human text {i+1}: {e}")
    
    # Test AI texts (should be classified as AI)
    print(f"\n=== TESTING AI TEXTS (From ChatGPT) ===")
    ai_correct = 0
    for i, text in enumerate(ai_texts):
        try:
            result = analyze_text(text)
            predicted_score = float(result[1])
            
            # ✅ ADDED: Store AI scores
            ai_scores.append(predicted_score)
            
            is_predicted_ai = predicted_score >= 0.99962
            
            if is_predicted_ai:  # Correctly identified as AI
                correct_predictions += 1
                ai_correct += 1
            
            total_predictions += 1
            status = "✅ CORRECT" if is_predicted_ai else "❌ WRONG"
            print(f"AI {i+1}: Score={predicted_score:.6f}, Predicted={'AI' if is_predicted_ai else 'Human'} {status}")
            
        except Exception as e:
            print(f"Error on AI text {i+1}: {e}")
    
    # ✅ ADDED: Calculate min/max scores for threshold optimization
    print(f"\n{'='*60}")
    print(f"📊 SCORE ANALYSIS FOR THRESHOLD OPTIMIZATION")
    print(f"{'='*60}")
    
    if human_scores:
        human_min = min(human_scores)
        human_max = max(human_scores)
        human_avg = sum(human_scores) / len(human_scores)
        print(f"🧑 HUMAN SCORES:")
        print(f"  Min: {human_min:.6f}")
        print(f"  Max: {human_max:.6f}")
        print(f"  Avg: {human_avg:.6f}")
        print(f"  Count: {len(human_scores)}")
    
    if ai_scores:
        ai_min = min(ai_scores)
        ai_max = max(ai_scores)
        ai_avg = sum(ai_scores) / len(ai_scores)
        print(f"\n🤖 AI SCORES:")
        print(f"  Min: {ai_min:.6f}")
        print(f"  Max: {ai_max:.6f}")
        print(f"  Avg: {ai_avg:.6f}")
        print(f"  Count: {len(ai_scores)}")
    
    # ✅ ADDED: Threshold recommendations
    if human_scores and ai_scores:
        print(f"\n🎯 THRESHOLD RECOMMENDATIONS:")
        
        # Find optimal threshold (between human max and AI min)
        overlap_start = max(human_scores)
        overlap_end = min(ai_scores)
        
        if overlap_start < overlap_end:
            suggested_threshold = (overlap_start + overlap_end) / 2
            print(f"  Suggested Threshold: {suggested_threshold:.6f}")
            print(f"  (Between human max {overlap_start:.6f} and AI min {overlap_end:.6f})")
        else:
            print(f"  ⚠️  OVERLAP DETECTED!")
            print(f"  Human max ({overlap_start:.6f}) > AI min ({overlap_end:.6f})")
            print(f"  Perfect separation impossible - some errors inevitable")
            
            # Find best compromise
            all_scores = human_scores + ai_scores
            all_scores.sort()
            median_threshold = all_scores[len(all_scores)//2]
            print(f"  Compromise Threshold: {median_threshold:.6f}")
    
    # Calculate detailed results with current threshold
    accuracy = correct_predictions / total_predictions
    human_accuracy = human_correct / len(human_texts)
    ai_accuracy = ai_correct / len(ai_texts)
    
    print(f"\n{'='*60}")
    print(f"📈 CURRENT PERFORMANCE (Threshold: 0.99962)")
    print(f"{'='*60}")
    print(f"Human Detection: {human_correct}/{len(human_texts)} ({human_accuracy:.2%})")
    print(f"AI Detection: {ai_correct}/{len(ai_texts)} ({ai_accuracy:.2%})")
    print(f"Overall Accuracy: {correct_predictions}/{total_predictions} ({accuracy:.2%})")
    
    # Analysis
    false_positives = len(human_texts) - human_correct  # Humans flagged as AI
    false_negatives = len(ai_texts) - ai_correct        # AI not detected
    
    print(f"\n❌ ERROR ANALYSIS:")
    print(f"False Positives (Human→AI): {false_positives} (Hurts students!)")
    print(f"False Negatives (AI→Human): {false_negatives} (Hurts integrity!)")
    
    # ✅ ADDED: Return scores for further analysis
    return {
        'accuracy': accuracy,
        'human_scores': human_scores,
        'ai_scores': ai_scores,
        'human_accuracy': human_accuracy,
        'ai_accuracy': ai_accuracy,
        'false_positives': false_positives,
        'false_negatives': false_negatives
    }

if __name__ == "__main__":
    test_ai_detection_accuracy()