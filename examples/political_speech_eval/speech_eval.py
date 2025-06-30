import argparse
import re
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class EvaluationResult:
    category_scores: Dict[str, Dict[str, float]] = field(default_factory=dict)

    def total(self) -> Dict[str, float]:
        return {
            cat: sum(scores.values()) for cat, scores in self.category_scores.items()
        }


class SpeechEvaluator:
    def __init__(self) -> None:
        self.emotion_words = ["기쁨", "슬픔", "감사", "분노", "희망"]
        self.ethical_words = ["신뢰", "책임", "윤리", "정의", "공정"]
        self.future_words = ["미래", "향후", "비전"]
        self.action_words = ["합시다", "해 주세요", "참여", "행동"]

    @staticmethod
    def _count_keywords(text: str, keywords: List[str]) -> int:
        return sum(text.count(k) for k in keywords)

    def evaluate_rhetoric(self, text: str) -> Dict[str, float]:
        scores = {}
        scores["strategic_rhetoric"] = min(text.count("?"), 5) / 5 * 20
        avg_sentence_len = sum(len(s) for s in re.split(r"[.!?]", text) if s) / max(
            len(re.split(r"[.!?]", text)), 1
        )
        scores["clarity"] = max(0, 20 - (avg_sentence_len - 40) * 0.5)
        scores["emotional_effect"] = (
            min(text.count("!") + self._count_keywords(text, self.emotion_words), 5)
            / 5
            * 20
        )
        unique_words = len(set(text.split()))
        scores["memorable_expression"] = min(unique_words / 100, 1) * 20
        scores["ethical_appeal"] = (
            min(self._count_keywords(text, self.ethical_words), 5) / 5 * 20
        )
        return scores

    def evaluate_logic(self, text: str) -> Dict[str, float]:
        scores = {}
        fallacy_markers = ["항상", "절대", "모든"]
        fallacies = self._count_keywords(text, fallacy_markers)
        scores["avoid_fallacy"] = max(0, 40 - fallacies * 8)
        scores["persuasive_fallacy"] = min(fallacies, 5) / 5 * 20
        scores["audience_impact"] = min(text.count("여러분"), 5) / 5 * 20
        scores["fallacy_compensation"] = max(0, 10 - fallacies * 2)
        scores["overall"] = max(0, 10 - fallacies)
        return scores

    def evaluate_monroe(self, text: str) -> Dict[str, float]:
        scores = {}
        scores["attention"] = min(text.count("여러분") + text.count("존경"), 5) / 5 * 20
        scores["need"] = min(text.count("문제") + text.count("위기"), 5) / 5 * 20
        scores["satisfaction"] = (
            min(text.count("해결") + text.count("계획"), 5) / 5 * 20
        )
        scores["visualization"] = (
            min(self._count_keywords(text, self.future_words), 5) / 5 * 20
        )
        scores["action"] = (
            min(self._count_keywords(text, self.action_words), 5) / 5 * 20
        )
        return scores

    def evaluate_ceremonial(self, text: str) -> Dict[str, float]:
        scores = {}
        scores["social_integration"] = (
            min(text.count("함께") + text.count("통합"), 5) / 5 * 33
        )
        scores["timeliness"] = min(text.count("오늘") + text.count("지금"), 5) / 5 * 33
        positive_words = ["기쁨", "축하", "감사", "발전"]
        scores["positive_values"] = (
            min(self._count_keywords(text, positive_words), 5) / 5 * 34
        )
        return scores

    def evaluate(self, text: str) -> EvaluationResult:
        result = EvaluationResult()
        result.category_scores["rhetoric"] = self.evaluate_rhetoric(text)
        result.category_scores["logic"] = self.evaluate_logic(text)
        result.category_scores["monroe"] = self.evaluate_monroe(text)
        result.category_scores["ceremonial"] = self.evaluate_ceremonial(text)
        return result


def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate political speech transcripts"
    )
    parser.add_argument("path", help="Path to the transcript text file")
    args = parser.parse_args()

    text = load_text(args.path)
    evaluator = SpeechEvaluator()
    result = evaluator.evaluate(text)

    for category, scores in result.category_scores.items():
        total = sum(scores.values())
        print(f"[{category}] total: {total:.1f}")
        for k, v in scores.items():
            print(f"  {k}: {v:.1f}")
    print("\nOverall scores:")
    for category, total in result.total().items():
        print(f"  {category}: {total:.1f}")


if __name__ == "__main__":
    main()
