import pandas as pd
from main import paragraph_chunker, annotate_chunks, analyze_text
import random
from colorama import init, Fore, Back, Style
init()

def load_test_data():
    """Load your labeled test data"""
    print("Loading test data...")
    
    # Load Kaggle human texts
    import kagglehub
    import os
    path = kagglehub.dataset_download("shanegerami/ai-vs-human-text")
    files = os.listdir(path)
    kaggle_csv = [f for f in files if f.endswith('.csv')][0]
    kaggle_df = pd.read_csv(os.path.join(path, kaggle_csv))
    human_texts = kaggle_df[kaggle_df['generated'] == 0]['text'].tolist()
    
    # Load your ChatGPT AI texts
    ai_df = pd.read_csv('ai_texts_50.csv')
    ai_texts = ai_df['text'].tolist()
    
    # Sample for testing
    human_sample = random.sample(human_texts, 50)
    ai_sample = ai_texts[:50]
    
    return human_sample, ai_sample

def test_word_limits_debug(human_texts, ai_texts, word_limits=[300]):
    """Debug version to see what's actually happening"""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.BLUE} DEBUG TEST {Style.RESET_ALL}")
    
    # Test just 2 human + 2 AI texts
    test_human = human_texts[:2]
    test_ai = ai_texts[:2]
    
    print(f"\n{Fore.YELLOW}=== HUMAN TEXTS ==={Style.RESET_ALL}")
    for i, text in enumerate(test_human):
        print(f"\nHuman {i+1}:")
        print(f"Text preview: {text[:100]}...")
        
        result = analyze_text(text)
        print(f"Raw API result: {result}")
        print(f"Result type: {type(result)}")
        print(f"Result[1]: {result[1]} (type: {type(result[1])})")
        
        try:
            score = float(result[1])
            print(f"Converted score: {score:.6f}")
            
            if score <= 0.99962:
                print(f"{Fore.GREEN}→ Would be ACCEPTED{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}→ Would go to CHUNKING{Style.RESET_ALL}")
        except Exception as e:
            print(f"Error converting score: {e}")
    
    print(f"\n{Fore.YELLOW}=== AI TEXTS ==={Style.RESET_ALL}")
    for i, text in enumerate(test_ai):
        print(f"\nAI {i+1}:")
        print(f"Text preview: {text[:100]}...")
        
        result = analyze_text(text)
        print(f"Raw API result: {result}")
        print(f"Result type: {type(result)}")
        print(f"Result[1]: {result[1]} (type: {type(result[1])})")
        
        try:
            score = float(result[1])
            print(f"Converted score: {score:.6f}")
            
            if score <= 0.99962:
                print(f"{Fore.RED}→ Would be ACCEPTED (BAD!){Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}→ Would go to CHUNKING{Style.RESET_ALL}")
        except Exception as e:
            print(f"Error converting score: {e}")
    
    # ADD THIS: Return empty dict to avoid the error
    return {}

def test_word_limits_full(human_texts, ai_texts, word_limits=[100, 200, 300, 400]):
    """Full test with your current logic"""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.BLUE} WORD LIMIT OPTIMIZATION TEST {Style.RESET_ALL}")
    
    results = {}
    
    for word_limit in word_limits:
        print(f"\n{Fore.YELLOW}Testing word limit: {word_limit}{Style.RESET_ALL}")
        
        # Test smaller subset to save API calls
        test_human = human_texts[:5]  # 5 human texts
        test_ai = ai_texts[:5]        # 5 AI texts
        
        human_correct = 0
        ai_correct = 0
        total_api_calls = 0
        total_chunks_created = 0
        
        # Test human texts
        for i, text in enumerate(test_human):
            try:
                # Step 1: Whole document check
                whole_doc_result = analyze_text(text)
                whole_doc_score = float(whole_doc_result[1])
                total_api_calls += 1
                
                print(f"  Human {i+1}: Whole doc = {whole_doc_score:.6f}")
                
                if whole_doc_score <= 0.99962:
                    # Accepted immediately
                    human_correct += 1
                    print(f"    → {Fore.GREEN}ACCEPTED{Style.RESET_ALL} (no chunking)")
                else:
                    # Go to chunking
                    chunks = paragraph_chunker(text, word_limit=word_limit)
                    annotated = annotate_chunks(chunks)
                    total_chunks_created += len(chunks)
                    total_api_calls += len(chunks)
                    
                    # Check if ANY chunk is red/yellow (your current logic)
                    suspicious_found = any(chunk["band"] in ["red", "yellow"] for chunk in annotated)
                    
                    if suspicious_found:
                        print(f"    → {Fore.RED}REJECTED{Style.RESET_ALL} ({len(chunks)} chunks, found suspicious)")
                    else:
                        human_correct += 1
                        print(f"    → {Fore.GREEN}ACCEPTED{Style.RESET_ALL} ({len(chunks)} chunks, all green)")
                
            except Exception as e:
                print(f"    Error: {e}")
        
        # Test AI texts
        for i, text in enumerate(test_ai):
            try:
                # Step 1: Whole document check
                whole_doc_result = analyze_text(text)
                whole_doc_score = float(whole_doc_result[1])
                total_api_calls += 1
                
                print(f"  AI {i+1}: Whole doc = {whole_doc_score:.6f}")
                
                if whole_doc_score <= 0.99962:
                    # Wrongly accepted
                    print(f"    → {Fore.RED}ACCEPTED{Style.RESET_ALL} (should be rejected!)")
                else:
                    # Go to chunking
                    chunks = paragraph_chunker(text, word_limit=word_limit)
                    annotated = annotate_chunks(chunks)
                    total_chunks_created += len(chunks)
                    total_api_calls += len(chunks)
                    
                    # Check if ANY chunk is red/yellow
                    suspicious_found = any(chunk["band"] in ["red", "yellow"] for chunk in annotated)
                    
                    if suspicious_found:
                        ai_correct += 1
                        print(f"    → {Fore.GREEN}REJECTED{Style.RESET_ALL} ({len(chunks)} chunks, correctly detected)")
                    else:
                        print(f"    → {Fore.RED}ACCEPTED{Style.RESET_ALL} ({len(chunks)} chunks, missed AI!)")
                
            except Exception as e:
                print(f"    Error: {e}")
        
        # Calculate metrics
        total_texts = len(test_human) + len(test_ai)
        human_accuracy = human_correct / len(test_human)
        ai_accuracy = ai_correct / len(test_ai)
        overall_accuracy = (human_correct + ai_correct) / total_texts
        avg_chunks_per_doc = total_chunks_created / total_texts if total_texts > 0 else 0
        
        results[word_limit] = {
            'human_accuracy': human_accuracy,
            'ai_accuracy': ai_accuracy,
            'overall_accuracy': overall_accuracy,
            'avg_chunks_per_doc': avg_chunks_per_doc,
            'total_api_calls': total_api_calls
        }
        
        print(f"{Fore.GREEN}Results for {word_limit} words:")
        print(f"  Human accuracy: {human_accuracy:.2%} ({human_correct}/{len(test_human)})")
        print(f"  AI accuracy: {ai_accuracy:.2%} ({ai_correct}/{len(test_ai)})")
        print(f"  Overall accuracy: {overall_accuracy:.2%}")
        print(f"  Avg chunks per doc: {avg_chunks_per_doc:.1f}")
        print(f"  Total API calls: {total_api_calls}{Style.RESET_ALL}")
    
    return results

def main():
    print(f"{Fore.CYAN}Loading test data...{Style.RESET_ALL}")
    human_texts, ai_texts = load_test_data()
    
    # Phase 1: Quick debug test
    print(f"\n{Fore.YELLOW}PHASE 1: Quick debug test...{Style.RESET_ALL}")
    test_word_limits_debug(human_texts, ai_texts)
    
    # Phase 2: Full optimization test
    print(f"\n{Fore.YELLOW}PHASE 2: Full word limit optimization...{Style.RESET_ALL}")
    results = test_word_limits_full(human_texts, ai_texts)
    
    # Analyze results
    if results:
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{Back.BLUE} OPTIMIZATION SUMMARY {Style.RESET_ALL}")
        
        best_accuracy = 0
        best_word_limit = None
        
        print(f"\n{'Word Limit':<12} {'Human':<8} {'AI':<8} {'Overall':<8} {'Chunks':<8} {'API Calls':<10}")
        print("-" * 65)
        
        for word_limit, metrics in results.items():
            human_acc = metrics['human_accuracy']
            ai_acc = metrics['ai_accuracy']
            overall_acc = metrics['overall_accuracy']
            avg_chunks = metrics['avg_chunks_per_doc']
            api_calls = metrics['total_api_calls']
            
            if overall_acc > best_accuracy:
                best_accuracy = overall_acc
                best_word_limit = word_limit
            
            print(f"{word_limit:<12} {human_acc:<8.1%} {ai_acc:<8.1%} {overall_acc:<8.1%} {avg_chunks:<8.1f} {api_calls:<10}")
        
        print(f"\n{Fore.GREEN}BEST WORD LIMIT: {best_word_limit} words (accuracy: {best_accuracy:.1%}){Style.RESET_ALL}")
    
    print(f"\n{Fore.GREEN}Testing complete!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()