# ai_model/dataset/generate_dataset.py
from faker import Faker
import random
import json
import math

fake = Faker()

skills = [
    "Python", "C++", "Machine Learning", "Data Science", "UI/UX Design",
    "Web Development", "Video Editing", "Public Speaking", "Graphic Design",
    "Photography", "Cloud Computing", "Cybersecurity", "SQL", "ReactJS", "AI",
    "Teamwork", "Conflict resolution", "Networking", "Relationship building",
    "Decision-making", "Time management", "Problem-solving", "Critical thinking",
    "Adaptability", "Communication", "Leadership", "Emotional intelligence",
    "Presentation skills", "Project management", "Product management",
    "Business development", "Sales", "Marketing", "Finance", "Accounting",
    "Taxation", "Legal", "HR", "Recruitment", "Training", "Performance management",
    "Employee relations"
]

departments = ["AIML", "CSE", "ISE", "ECE", "EEE", "MECH", "CIVIL"]
modes = ["Online", "Offline", "Hybrid"]

# helper to assign badge based on score
def get_badge(score):
    if score >= 85:
        return "Expert"
    elif score >= 70:
        return "Advanced"
    elif score >= 50:
        return "Intermediate"
    else:
        return "Beginner"

def generate_user(user_id):
    name = fake.first_name()
    email_prefix = name.lower() + str(random.randint(1, 99))
    email = f"{email_prefix}@vvce.ac.in"

    can_teach = random.sample(skills, k=3)
    want_to_learn = random.sample([s for s in skills if s not in can_teach], k=3)

    skill_tests = {}
    for skill in can_teach:
        score = random.randint(40, 100)
        skill_tests[skill] = {
            "score": score,
            "badge": get_badge(score)
        }

    return {
        "user_id": user_id,
        "name": name,
        "email": email,
        "skills_can_teach": can_teach,
        "skills_want_to_learn": want_to_learn,
        "rating": round(random.uniform(3.0, 5.0), 2),
        "activity_score": round(random.uniform(0.5, 1.0), 2),
        "experience": random.randint(0, 5),
        "department": random.choice(departments),
        "preferred_mode": random.choice(modes),
        "availability_hours_per_week": random.randint(4, 12),
        "communication_score": round(random.uniform(0.6, 1.0), 2),
        "personality_score": round(random.uniform(0.6, 1.0), 2),
        "skill_tests": skill_tests
    }

# generate dataset of 500 users
users = [generate_user(i) for i in range(1, 501)]

with open("users_dataset.json", "w") as f:
    json.dump(users, f, indent=4)

print("✅ Dataset generated successfully: users_dataset.json (500 users)")
