from abc import ABC, abstractmethod


class Sport(ABC):
    def __init__(self, name: str, participant_label: str = "Team"):
        self.name = name
        self.participant_label = participant_label

    @abstractmethod
    def validate_score(self, score_str: str) -> bool:
        pass


class Soccer(Sport):
    def __init__(self): super().__init__("Soccer", "Team")

    def validate_score(self, score_str: str) -> bool:
        try:
            a, b = map(int, score_str.split('-'))
            return 0 <= a <= 30 and 0 <= b <= 30
        except:
            return False


class Basketball(Sport):
    def __init__(self): super().__init__("Basketball", "Team")

    def validate_score(self, score_str: str) -> bool:
        try:
            a, b = map(int, score_str.split('-'))
            return 30 <= a <= 250 and 30 <= b <= 250
        except:
            return False


class Billiards(Sport):
    def __init__(self): super().__init__("Billiards", "Player")

    def validate_score(self, score_str: str) -> bool:
        try:
            a, b = map(int, score_str.split('-'))
            return 0 <= a <= 50 and 0 <= b <= 50
        except:
            return False


class Formula1(Sport):
    def __init__(self): super().__init__("Formula 1", "Driver")

    def validate_score(self, score_str: str) -> bool:
        try:
            a, b = score_str.split('-')
            return a.strip().isdigit() and b.strip().isdigit()
        except:
            return False


class CustomSport(Sport):
    def __init__(self, name): super().__init__(name, "Participant")

    def validate_score(self, score_str: str) -> bool:
        try:
            a, b = score_str.split('-')
            return a.strip().isdigit() and b.strip().isdigit()
        except:
            return False


def test_sports():
    sports = [Soccer(), Basketball(), Billiards(),
              Formula1(), CustomSport("Chess")]

    sample_scores = {
        "Soccer": "3-2",
        "Basketball": "120-110",
        "Billiards": "25-30",
        "Formula1": "1-2",
        "Chess": "1-0"
    }

    for sport in sports:
        score = sample_scores.get(sport.get_name(), "0-0")
        print(f"{sport.get_name()} ({sport.participant_label}) - Score '{score}' valid? {sport.validate_score(score)}")


if __name__ == "__main__":
    test_sports()
