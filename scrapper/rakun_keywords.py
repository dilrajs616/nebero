from rakun2 import RakunKeyphraseDetector

def get_keywords(document, num_keywords=10, merge_threshold=1, alpha=0.3, token_prune_len=1):
    hyperparameters = {
        "num_keywords": num_keywords,
        "merge_threshold": merge_threshold,
        "alpha": alpha,
        "token_prune_len": token_prune_len
    }

    keyword_detector = RakunKeyphraseDetector(hyperparameters)
    out_keywords = keyword_detector.find_keywords(document, input_type="string")

    keywords = [item[0] for item in out_keywords]

    return keywords
