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
    
    return human_texts[:10], ai_texts[:10]  # Just 10 of each for debugging

def debug_chunk_scores():
    """Print ALL chunk scores to see what's happening"""
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.BLUE} CHUNK SCORE DEBUG - PRINTING ALL SCORES {Style.RESET_ALL}")
    
    human_texts, ai_texts = load_test_data()
    
    # Test different word limits
    for target_words in [200, 300, 400]:  # Changed variable name
        print(f"\n{Fore.YELLOW}{'='*50}")
        print(f"TARGET WORDS: {target_words}")  # Updated display
        print(f"{'='*50}{Style.RESET_ALL}")
        
        # Test 2 human texts
        print(f"\n{Fore.BLUE}HUMAN TEXTS:{Style.RESET_ALL}")
        for i, text in enumerate(human_texts[:2]):
            print(f"\n{Fore.CYAN}--- Human Text {i+1} ---{Style.RESET_ALL}")
            print(f"Text preview: {text[:150]}...")
            print(f"Text length: {len(text)} chars, {len(text.split())} words")
            
            # Test whole document first
            try:
                whole_result = analyze_text(text)
                whole_score = float(whole_result[1])
                print(f"\n{Fore.MAGENTA}WHOLE DOCUMENT:{Style.RESET_ALL}")
                print(f"  Score: {whole_score:.6f}")
                print(f"  Label: {whole_result[0]}")
                print(f"  Above threshold (0.99962)? {whole_score > 0.99962}")
            except Exception as e:
                print(f"Error analyzing whole document: {e}")
                continue
            
            # Now test chunks - FIXED PARAMETER NAME
            try:
                chunks = paragraph_chunker(text, target_words=target_words)  # ✅ Fixed
                print(f"\n{Fore.MAGENTA}CHUNKS ({len(chunks)} total):{Style.RESET_ALL}")
                
                for j, chunk in enumerate(chunks):
                    print(f"\n  {Fore.YELLOW}Chunk {j+1}:{Style.RESET_ALL}")
                    print(f"    Words: {len(chunk.split())}")
                    print(f"    Text: {chunk[:100]}...")
                    
                    try:
                        chunk_result = analyze_text(chunk)
                        chunk_score = float(chunk_result[1])
                        
                        # Determine band using your thresholds
                        if chunk_score >= 0.99962:
                            band = "RED"
                            color = Fore.RED
                        elif 0.99960 <= chunk_score < 0.99962:
                            band = "YELLOW"
                            color = Fore.YELLOW
                        else:
                            band = "GREEN"
                            color = Fore.GREEN
                        
                        print(f"    {color}Score: {chunk_score:.6f} ({band}){Style.RESET_ALL}")
                        print(f"    Label: {chunk_result[0]}")
                        
                    except Exception as e:
                        print(f"    Error: {e}")
                        
            except Exception as e:
                print(f"Error chunking text: {e}")
        
        # Test 2 AI texts - SAME FIX
        print(f"\n{Fore.BLUE}AI TEXTS:{Style.RESET_ALL}")
        for i, text in enumerate(ai_texts[:2]):
            print(f"\n{Fore.CYAN}--- AI Text {i+1} ---{Style.RESET_ALL}")
            print(f"Text preview: {text[:150]}...")
            print(f"Text length: {len(text)} chars, {len(text.split())} words")
            
            # Test whole document first
            try:
                whole_result = analyze_text(text)
                whole_score = float(whole_result[1])
                print(f"\n{Fore.MAGENTA}WHOLE DOCUMENT:{Style.RESET_ALL}")
                print(f"  Score: {whole_score:.6f}")
                print(f"  Label: {whole_result[0]}")
                print(f"  Above threshold (0.99962)? {whole_score > 0.99962}")
            except Exception as e:
                print(f"Error analyzing whole document: {e}")
                continue
            
            # Now test chunks - FIXED PARAMETER NAME
            try:
                chunks = paragraph_chunker(text, target_words=target_words)  # ✅ Fixed
                print(f"\n{Fore.MAGENTA}CHUNKS ({len(chunks)} total):{Style.RESET_ALL}")
                
                for j, chunk in enumerate(chunks):
                    print(f"\n  {Fore.YELLOW}Chunk {j+1}:{Style.RESET_ALL}")
                    print(f"    Words: {len(chunk.split())}")
                    print(f"    Text: {chunk[:100]}...")
                    
                    try:
                        chunk_result = analyze_text(chunk)
                        chunk_score = float(chunk_result[1])
                        
                        # Determine band using your thresholds
                        if chunk_score >= 0.99962:
                            band = "RED"
                            color = Fore.RED
                        elif 0.99960 <= chunk_score < 0.99962:
                            band = "YELLOW"
                            color = Fore.YELLOW
                        else:
                            band = "GREEN"
                            color = Fore.GREEN
                        
                        print(f"    {color}Score: {chunk_score:.6f} ({band}){Style.RESET_ALL}")
                        print(f"    Label: {chunk_result[0]}")
                        
                    except Exception as e:
                        print(f"    Error: {e}")
                        
            except Exception as e:
                print(f"Error chunking text: {e}")

def test_your_annotate_function():
    """Test your annotate_chunks function directly"""
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.BLUE} TESTING YOUR ANNOTATE_CHUNKS FUNCTION {Style.RESET_ALL}")
    
    human_texts, ai_texts = load_test_data()
    
    # Test 1 human and 1 AI text
    test_text = human_texts[0]
    print(f"\n{Fore.YELLOW}Testing with Human Text:{Style.RESET_ALL}")
    print(f"Preview: {test_text[:150]}...")
    
    try:
        chunks = paragraph_chunker(test_text, target_words=300)  # ✅ Fixed parameter name
        print(f"Created {len(chunks)} chunks")
        
        # Use your annotate_chunks function
        annotated = annotate_chunks(chunks)
        
        print(f"\n{Fore.MAGENTA}Your annotate_chunks results:{Style.RESET_ALL}")
        for i, chunk_data in enumerate(annotated):
            print(f"Chunk {i+1}:")
            print(f"  Band: {chunk_data.get('band', 'MISSING')}")
            print(f"  Score: {chunk_data.get('raw_score', 'MISSING')}")
            print(f"  Keys: {list(chunk_data.keys())}")
            print(f"  Text preview: {chunk_data.get('chunk', 'MISSING')[:80]}...")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def main():
    print(f"{Fore.CYAN}Starting chunk score debugging...{Style.RESET_ALL}")
    
    # Test 1: Raw chunk scores
    debug_chunk_scores()
    
    # Test 2: Your annotate function
    test_your_annotate_function()
    
    print(f"\n{Fore.GREEN}Debug complete!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()