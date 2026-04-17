import json
import math
from termcolor import colored

# ---------- LOAD DATA ----------
with open("users_dataset.json", "r") as f:
    tutors = json.load(f)

# ---------- GET LEARNER INPUT ----------
print(colored("🎓 Welcome to SkillSwap AI Tutor Matcher", "cyan", attrs=["bold"]))
learner_name = input("Enter your name: ").strip()
learner_email = input("Enter your email: ").strip()
learner_dept = input("Enter your department (e.g., AIML, CSE, ECE, CIVIL, EEE): ").strip().upper()
learner_mode = input("Preferred learning mode (Online / Offline / Hybrid / Any): ").strip().capitalize()
skill = input("Enter the skill you want to learn (e.g., Python, C++, ML, Leadership): ").strip().title()

preferred_mode = input("Do you want tutors with a specific mode? (Online/Offline/Hybrid/Any): ").strip().capitalize()
preferred_dept = input("Do you want tutors from a specific department? (Dept name / Any): ").strip().upper()

# ---------- FILTERING ----------
filtered_tutors = [
    t for t in tutors
    if (preferred_mode == "Any" or t["preferred_mode"] == preferred_mode)
    and (preferred_dept == "Any" or t["department"] == preferred_dept)
]

if not filtered_tutors:
    print(colored("⚠️ No tutors match your filters. Showing all tutors instead.", "yellow"))
    filtered_tutors = tutors

# ---------- MATCHING LOGIC ----------
recommended_tutors = []

for tutor in filtered_tutors:
    skills = [s.lower() for s in tutor["skills_can_teach"]]

    skill_match = 1.0 if skill.lower() in skills else 0.6 if any(skill.lower() in s for s in skills) else 0.0

    dept_bonus = 0.1 if tutor["department"] == learner_dept else 0
    mode_bonus = 0.05 if (tutor["preferred_mode"] == learner_mode or learner_mode == "Any") else 0
    rating_weight = tutor.get("rating", 4.0) / 5
    activity_weight = tutor.get("activity_score", 0.5)
    experience = tutor.get("experience", 1)

    base_score = (skill_match * 0.5) + (rating_weight * 0.25) + (activity_weight * 0.15) + (dept_bonus + mode_bonus)
    final_score = round(min(base_score + math.log1p(experience) * 0.05, 1), 3)

    # Skill test info (optional)
    test_info = tutor.get("skill_tests", {}).get(skill, {})
    badge = test_info.get("badge", "N/A")
    score = test_info.get("score", "N/A")

    # Explanation generation
    reason = []
    if tutor["department"] == learner_dept:
        reason.append("Same department")
    if tutor["rating"] >= 4.5:
        reason.append("High rating")
    if tutor["activity_score"] >= 0.8:
        reason.append("Highly active")
    if badge != "N/A":
        reason.append("Completed skill test")
    explanation = ", ".join(reason) if reason else "Strong skill match"

    # Confidence label
    confidence = "High" if final_score > 0.9 else "Medium" if final_score > 0.75 else "Low"

    recommended_tutors.append({
        "name": tutor["name"],
        "email": tutor["email"],
        "department": tutor["department"],
        "preferred_mode": tutor["preferred_mode"],
        "final_score": final_score,
        "badge": badge,
        "skill_score": score,
        "reason": explanation,
        "confidence": confidence
    })

# ---------- SORT RESULTS ----------
recommended_tutors.sort(key=lambda x: x["final_score"], reverse=True)

# ---------- DISPLAY RESULTS ----------
print("\n" + colored(f"📚 Skill Recommendation Results for: {skill}", "magenta", attrs=["bold"]))
if not recommended_tutors:
    print(colored("No suitable tutors found.", "red"))
else:
    for i, tutor in enumerate(recommended_tutors[:3], 1):
        print(colored(f"\n#{i}. 👩‍🏫 {tutor['name']} ({tutor['email']})", "cyan", attrs=["bold"]))
        print(colored(f"   🏫 Dept: {tutor['department']} | Mode: {tutor['preferred_mode']}", "yellow"))
        print(colored(f"   📈 Score: {tutor['final_score']} | Badge: {tutor['badge']} ({tutor['skill_score']})", "green"))
        print(colored(f"   🔍 Reason: {tutor['reason']}", "white"))
        print(colored(f"   🤖 Confidence: {tutor['confidence']}", "blue"))

# ---------- SAVE OUTPUT ----------
output = {
    "learner_name": learner_name,
    "learner_email": learner_email,
    "requested_skill": skill,
    "recommendations": recommended_tutors[:3]
}

with open(f"recommendations_{skill.lower()}.json", "w") as f:
    json.dump(output, f, indent=4)

print(colored("\n✅ Top tutor recommendations saved successfully!", "green", attrs=["bold"]))
