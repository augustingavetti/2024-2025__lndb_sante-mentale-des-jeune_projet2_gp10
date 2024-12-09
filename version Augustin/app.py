from data import questions, encouragements
from collections import defaultdict
import random

class MentalHealthApp:
    def __init__(self):
        self.users = {}
        self.current_user = None
        self.responses = []
        self.weekly_summaries = []
        self.global_summary = defaultdict(lambda: defaultdict(int))
        self.day_count = 0

    def create_account(self, username, password):
        if username not in self.users:
            self.users[username] = {"password": password, "responses": [], "weekly_summaries": []}
            return True
        return False

    def login(self, username, password):
        if username in self.users and self.users[username]["password"] == password:
            self.current_user = username
            self.responses = self.users[username]["responses"]
            self.weekly_summaries = self.users[username]["weekly_summaries"]
            return True
        return False

    def start_questionnaire(self):
        return questions  # Retourne toutes les questions dans l'ordre

    def submit_response(self, responses):
        self.responses.append(responses)
        self.users[self.current_user]["responses"] = self.responses
        self.day_count += 1
        if self.day_count == 8:
            self.reset_global_summary()
        self.update_global_summary(responses)
        if len(self.responses) % 7 == 0:
            self.generate_weekly_summary()

    def update_global_summary(self, responses):
        for question, response in responses.items():
            self.global_summary[question][response] += 1

    def reset_global_summary(self):
        self.global_summary = defaultdict(lambda: defaultdict(int))
        self.day_count = 0

    def generate_weekly_summary(self):
        weekly_data = self.responses[-7:]
        summary = {}
        for question in questions:
            responses = [day[question] for day in weekly_data]
            summary[question] = max(set(responses), key=responses.count)  # Mode (réponse la plus fréquente)
        encouragement = random.choice(encouragements)
        self.weekly_summaries.append({"data": summary, "encouragement": encouragement})
        self.users[self.current_user]["weekly_summaries"] = self.weekly_summaries

    def get_latest_summary(self):
        if self.weekly_summaries:
            return self.weekly_summaries[-1]
        return None

    def get_overall_summary(self):
        return dict(self.global_summary)
