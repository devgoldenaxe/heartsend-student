import pandas as pd

AVAILABILITY_PENALTIES = {
    "Currently available": 0,
    "Limited Availability": -2,
    "Not currently available": -5
}

WEIGHT_HEALTH_CONDITION_MATCH = 2
WEIGHT_HOBBY_MATCH = 3
WEIGHT_RACE_MATCH = 1
WEIGHT_RELIGION_MATCH = 1
WEIGHT_GENDER_MATCH = 1
WEIGHT_GRADE_SAME = 3
WEIGHT_GRADE_ADJACENT = 2
WEIGHT_LANGUAGE_MATCH = 2
WEIGHT_HOME_TYPE_MATCH = 1
WEIGHT_INTENTION_SAME = 2

def intention_score_kids(intA, intB):
    return WEIGHT_INTENTION_SAME if intA == intB else 0

GRADE_MAP = {
    "K": 0,
    "k": 0,
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8
}

def grade_score(gradeA, gradeB):
    try:
        gA = GRADE_MAP.get(str(gradeA).strip(), -1)
        gB = GRADE_MAP.get(str(gradeB).strip(), -1)
        if gA < 0 or gB < 0:
            return 0
        diff = abs(gA - gB)
        if diff == 0:
            return WEIGHT_GRADE_SAME
        elif diff == 1:
            return WEIGHT_GRADE_ADJACENT
        elif diff == 2:
            return 1
        else:
            return 0
    except:
        return 0

STATE_NEIGHBORS = {
    "AL": ["FL", "GA", "MS", "TN"],
    "AK": [],
    "AZ": ["CA", "NV", "UT", "CO", "NM"],
    "AR": ["MO", "TN", "MS", "LA", "TX", "OK"],
    "CA": ["OR", "NV", "AZ"],
    "CO": ["WY", "NE", "KS", "OK", "NM", "AZ", "UT"],
    "CT": ["NY", "MA", "RI"],
    "DE": ["MD", "PA", "NJ"],
    "FL": ["AL", "GA"],
    "GA": ["FL", "AL", "TN", "NC", "SC"],
    "HI": [],
    "ID": ["WA", "OR", "NV", "UT", "WY", "MT"],
    "IL": ["WI", "IA", "MO", "KY", "IN"],
    "IN": ["MI", "OH", "KY", "IL"],
    "IA": ["MN", "SD", "NE", "MO", "IL", "WI"],
    "KS": ["NE", "CO", "OK", "MO"],
    "KY": ["IN", "OH", "WV", "VA", "TN", "MO", "IL"],
    "LA": ["TX", "AR", "MS"],
    "ME": ["NH"],
    "MD": ["VA", "WV", "PA", "DE"],
    "MA": ["NY", "VT", "NH", "RI", "CT"],
    "MI": ["IN", "OH", "WI"],
    "MN": ["ND", "SD", "IA", "WI"],
    "MS": ["LA", "AR", "TN", "AL"],
    "MO": ["IA", "NE", "KS", "OK", "AR", "TN", "KY", "IL"],
    "MT": ["ID", "WY", "SD", "ND"],
    "NE": ["SD", "WY", "CO", "KS", "MO", "IA"],
    "NV": ["CA", "OR", "ID", "UT", "AZ"],
    "NH": ["ME", "MA", "VT"],
    "NJ": ["NY", "PA", "DE"],
    "NM": ["AZ", "UT", "CO", "OK", "TX"],
    "NY": ["PA", "NJ", "CT", "MA", "VT"],
    "NC": ["GA", "SC", "TN", "VA"],
    "ND": ["MT", "SD", "MN"],
    "OH": ["PA", "WV", "KY", "IN", "MI"],
    "OK": ["KS", "MO", "AR", "TX", "NM", "CO"],
    "OR": ["WA", "ID", "NV", "CA"],
    "PA": ["NY", "NJ", "DE", "MD", "WV", "OH"],
    "RI": ["CT", "MA"],
    "SC": ["GA", "NC"],
    "SD": ["ND", "MN", "IA", "NE", "WY", "MT"],
    "TN": ["KY", "VA", "NC", "GA", "AL", "MS", "AR", "MO"],
    "TX": ["NM", "OK", "AR", "LA"],
    "UT": ["ID", "WY", "CO", "NM", "AZ", "NV"],
    "VT": ["NY", "MA", "NH"],
    "VA": ["MD", "NC", "TN", "KY", "WV"],
    "WA": ["ID", "OR"],
    "WV": ["PA", "MD", "VA", "KY", "OH"],
    "WI": ["MN", "IA", "IL", "MI"],
    "WY": ["MT", "SD", "NE", "CO", "UT", "ID"],
    "DC": ["MD", "VA"]
}

def compute_match_score(userA, userB):
    score = 0
    penaltyA = AVAILABILITY_PENALTIES.get(userA.get("Availability"), 0)
    penaltyB = AVAILABILITY_PENALTIES.get(userB.get("Availability"), 0)
    score += (penaltyA + penaltyB)
    cityA = str(userA.get("city_ascii", "") or "")
    cityB = str(userB.get("city_ascii", "") or "")
    stateA = str(userA.get("state_id", "") or "")
    stateB = str(userB.get("state_id", "") or "")
    if cityA and cityB and cityA.lower() == cityB.lower():
        score += 15
    else:
        if stateA == stateB and stateA:
            score += 5
        else:
            neighbors_of_A = STATE_NEIGHBORS.get(stateA, [])
            if stateB in neighbors_of_A:
                score += 2
    score += grade_score(userA.get("Grade", ""), userB.get("Grade", ""))
    hcA_str = str(userA.get("HealthCondition") or "")
    hcB_str = str(userB.get("HealthCondition") or "")
    setA = set([h.strip().lower() for h in hcA_str.split(",") if h.strip()])
    setB = set([h.strip().lower() for h in hcB_str.split(",") if h.strip()])
    shared_conditions = setA.intersection(setB)
    score += len(shared_conditions) * WEIGHT_HEALTH_CONDITION_MATCH
    hobbyA_str = str(userA.get("Hobbies") or "")
    hobbyB_str = str(userB.get("Hobbies") or "")
    hobbiesA = set([h.strip().lower() for h in hobbyA_str.split(",") if h.strip()])
    hobbiesB = set([h.strip().lower() for h in hobbyB_str.split(",") if h.strip()])
    shared_hobbies = hobbiesA.intersection(hobbiesB)
    score += len(shared_hobbies) * WEIGHT_HOBBY_MATCH
    intA = str(userA.get("Intention", "") or "")
    intB = str(userB.get("Intention", "") or "")
    score += intention_score_kids(intA, intB)
    raceA = str(userA.get("Race", "") or "")
    raceB = str(userB.get("Race", "") or "")
    if raceA and raceA == raceB:
        score += WEIGHT_RACE_MATCH
    relA = str(userA.get("Religion", "") or "")
    relB = str(userB.get("Religion", "") or "")
    if relA and relA == relB:
        score += WEIGHT_RELIGION_MATCH
    genA = str(userA.get("Gender", "") or "")
    genB = str(userB.get("Gender", "") or "")
    if genA and genB and genA.lower() == genB.lower():
        score += WEIGHT_GENDER_MATCH
    langA_str = str(userA.get("Language") or "")
    langB_str = str(userB.get("Language") or "")
    langSetA = set([l.strip().lower() for l in langA_str.split(",") if l.strip()])
    langSetB = set([l.strip().lower() for l in langB_str.split(",") if l.strip()])
    if langSetA and langSetB:
        shared_lang = langSetA.intersection(langSetB)
        if shared_lang:
            score += len(shared_lang) * WEIGHT_LANGUAGE_MATCH
    homeA = str(userA.get("HomeType", "") or "")
    homeB = str(userB.get("HomeType", "") or "")
    if homeA and homeB and homeA.lower() == homeB.lower():
        score += WEIGHT_HOME_TYPE_MATCH
    return score

def recommend_for_user(user, all_users, top_n=5):
    scores = []
    for other in all_users:
        if other.get("email") == user.get("email"):
            continue
        if other.get("Availability", "") == "Not currently available":
            continue
        match_score = compute_match_score(user, other)
        scores.append((other, match_score))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_n]

if __name__ == "__main__":
    excel_file_path = r"C:\Users\MSI\Desktop\work\recommendation system\kids version\synthetic_output.xlsx"
    sheet_name = 0
    df_out = pd.read_excel(excel_file_path, sheet_name=sheet_name)
    list_of_users = df_out.to_dict(orient="records")
    test_user = {
        "first_name": "Dora",
        "last_name": "Explorer",
        "email": "[email protected]",
        "Availability": "Currently available",
        "HealthCondition": "Asthma",
        "Hobbies": "reading books, stargazing, painting",
        "Intention": "Making new friends",
        "Race": "Hispanic or Latino",
        "Religion": "Catholic",
        "Language": "Spanish, English",
        "Grade": "3",
        "HomeType": "Both Parents",
        "city_ascii": "Miami",
        "state_id": "FL",
        "Gender": "Female"
    }
    extended_users = list_of_users + [test_user]
    top_5 = recommend_for_user(test_user, extended_users, top_n=5)
    print(f"Top 5 recommendations for {test_user['first_name']} {test_user['last_name']} ({test_user['email']}):\n")
    for match_user, score in top_5:
        print(f"Name: {match_user.get('first_name','')} {match_user.get('last_name','')}")
        print(f"Email: {match_user.get('email','')}")
        print(f"Score: {score}")
        print("Features:")
        print(f"  Availability: {match_user.get('Availability', '')}")
        print(f"  Grade: {match_user.get('Grade', '')}")
        print(f"  HealthCondition: {match_user.get('HealthCondition', '')}")
        print(f"  Hobbies: {match_user.get('Hobbies', '')}")
        print(f"  Intention: {match_user.get('Intention', '')}")
        print(f"  Race: {match_user.get('Race', '')}")
        print(f"  Religion: {match_user.get('Religion', '')}")
        print(f"  Language: {match_user.get('Language', '')}")
        print(f"  HomeType: {match_user.get('HomeType', '')}")
        print(f"  Location: {match_user.get('city_ascii', '')}, {match_user.get('state_id', '')}")
        print(f"  Gender: {match_user.get('Gender', '')}")
        print("-" * 40)
