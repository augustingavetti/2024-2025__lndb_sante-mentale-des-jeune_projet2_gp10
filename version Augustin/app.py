import random
from data import questions, encouragements
from dictionary import emotion_dict

class MentalHealthApp:
    def __init__(self):
        self.users = {}
        self.admin_code = "1234"
        self.current_user = None
        self.responses = []
        self.weekly_summaries = []

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
        daily_questions = random.sample(questions, 5)  # Sélectionne 5 questions aléatoires
        return daily_questions

    def submit_response(self, responses):
        self.responses.append(responses)
        self.users[self.current_user]["responses"] = self.responses
        if len(self.responses) % 7 == 0:
            self.generate_weekly_summary()

    def generate_weekly_summary(self):
        weekly_data = self.responses[-7:]
        summary = {emotion: sum(day[emotion] for day in weekly_data) / 7 for emotion in emotion_dict}
        encouragement = random.choice(encouragements)
        self.weekly_summaries.append({"data": summary, "encouragement": encouragement})
        self.users[self.current_user]["weekly_summaries"] = self.weekly_summaries

    def get_latest_summary(self):
        if self.weekly_summaries:
            return self.weekly_summaries[-1]
        return None

    def get_overall_summary(self):
        if len(self.weekly_summaries) >= 7:
            overall_data = {emotion: sum(week["data"][emotion] for week in self.weekly_summaries[-7:]) / 7 
                            for emotion in emotion_dict}
            return overall_data
        return None

    def is_admin(self, code):
        return code == self.admin_code