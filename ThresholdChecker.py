class ThresholdChecker:
    def __init__(self, threshold : float):
        self.threshold = threshold


    def check_score(self, score: float) -> bool:
        result = score > self.threshold
        print(f"Too much AI: {result}")
        return result
        