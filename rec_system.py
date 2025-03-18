import requests
import datetime
cache = {}

def get_students(schoolId, version):
    now = datetime.datetime.now()
    
    if schoolId in cache:
        students, timestamp = cache[schoolId]
        if now - timestamp < datetime.timedelta(days=1):
            print("Returning cached data.")
            return students

    # If no valid cached data is available, fetch new data.
    print("Fetching new data.")
    students = fetch_all_employee_details(schoolId, version)
    cache[schoolId] = (students, now)
    return students
 
page_count = 1000
def fetch_all_employee_details(School_id , version):
    url = "https://employment-db-copy.bubbleapps.io/version-test/api/1.1/obj/profiledetails"
    if version == "live":
        url = "https://employment-db-copy.bubbleapps.io/api/1.1/obj/profiledetails"
        
    headers = {
        "Authorization": "Bearer 5e0e72029a8522ea3334be9c03098501"
    }
    params = {
        "constraints": '[{"key": "School", "constraint_type": "equals", "value": "'+School_id+'"}]',
        "cursor": 0,
        "limit": page_count
    }
    print(School_id)
    all_results = []
    
    while True:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            break
        
        data = response.json().get("response", {})
        results = data.get("results", [])
        
        # Extract specific fields from each result
        # extracted_fields = [{'_id': result.get('_id', 'N/A'), 'School': result.get('School', 'N/A')} for result in results]
        all_results.extend(results)
        
        remaining = data.get("remaining", 0)
        cursor = data.get("cursor", 0)
        
        if remaining <= 0:
            break
        
        params["cursor"] = cursor + page_count
        # break
            
    return all_results

AVAILABILITY_PENALTIES = {
    "Currently available": 0,
    "Limited availability": -2,
    "Currently Not available": -5
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
    cityA = str(userA.get("City", "") or "")
    cityB = str(userB.get("City", "") or "")
    stateA = str(userA.get("State", "") or "")
    stateB = str(userB.get("State", "") or "")
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
    hcA_str = str(userA.get("Health_Condition") or "")
    hcB_str = str(userB.get("Health_Condition") or "")
    setA = set([h.strip().lower() for h in hcA_str.split(",") if h.strip()])
    setB = set([h.strip().lower() for h in hcB_str.split(",") if h.strip()])
    shared_conditions = setA.intersection(setB)
    score += len(shared_conditions) * WEIGHT_HEALTH_CONDITION_MATCH
    hobbyA_str = str(userA.get("Hobby") or "")
    hobbyB_str = str(userB.get("Hobby") or "")
    hobbiesA = set([h.strip().lower() for h in hobbyA_str.split(",") if h.strip()])
    hobbiesB = set([h.strip().lower() for h in hobbyB_str.split(",") if h.strip()])
    shared_hobbies = hobbiesA.intersection(hobbiesB)
    score += len(shared_hobbies) * WEIGHT_HOBBY_MATCH
    intA = str(userA.get("Intentions", "") or "")
    intB = str(userB.get("Intentions", "") or "")
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
        print("-----")
        print(other.get("_id"))
        print(other.get("Availability", ""))
        if other.get("_id") == user.get("_id"):
            continue
        print("--1---")
        if other.get("Availability") == "Currently Not available":
            continue
        print("--2---")
        match_score = compute_match_score(user, other)
        print(match_score)
        scores.append((other, match_score))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_n]

def module(School_id, user_id , version = "test"):
    #excel_file_path = r"C:\Users\MSI\Desktop\work\recommendation system\kids version\synthetic_output.xlsx"
    #sheet_name = 0
    print(version)
    df_out = get_students(School_id , version)
    print(df_out[0])
    #list_of_users = df_out.to_dict(orient="records")
    # test_user = {

    #     "Full name": "Dora",
    #     "Employee Email": "[email protected]",
    #     "Availability": "Currently available",
    #     "Health Condition": "Asthma",
    #     "Hobbies": "reading books, stargazing, painting",
    #     "Intention": "Making new friends",
    #     "Race": "Hispanic or Latino",
    #     "Religion": "Catholic",
    #     "Language": "Spanish, English",
    #     "Grade": "3",
    #     "Home type": "Both Parents",
    #     "City": "Miami",
    #     "state_id": "FL",
    #     "Gender": "Female"
    # }
   # 4) Get the top 5 recommended matches for the test user

    # extended_users = df_out + [test_user]
    # print(df_out[0])
    # print(len(df_out))
    # for item in df_out:
    #     print("id: " + item["_id"])
    test_user = next((item for item in df_out if item['_id'] == user_id), None)
    # Now let's retrieve top 5 for the test_user
    ids = []
    if test_user:
        top_5 = recommend_for_user(test_user, df_out, top_n=20)
        ids = [item['_id'] for item, score in top_5]
        
        print(f"Top 5 recommendations for {test_user['Full name']} :\n")
        for match_user, score in top_5:
            print(f"Name: {match_user['Full name']}")
            print(f"Score: {score}")
            print("Features:")
            print(f"  Availability: {match_user.get('Availability', '')}")
            print(f"  Grade: {match_user.get('Grade', '')}")
            print(f"  Health_Condition: {match_user.get('Health Condition', '')}")
            print(f"  Hobby: {match_user.get('hobbies', '')}")
            print(f"  Intentions: {match_user.get('Intention', '')}")
            print(f"  Race: {match_user.get('Race', '')}")
            print(f"  Religion: {match_user.get('Religion', '')}")
            print(f"  Language: {match_user.get('Language', '')}")
            print(f"  Home type: {match_user.get('Home type', '')}")
            print(f"  Location: {match_user.get('State', '')}, {match_user.get('State_id', '')}")
            print(f"  Gender: {match_user.get('Gender', '')}")
            print("-" * 40)

    # print(type(top_5))
    print(ids)
    return ids


# if __name__ == "__main__":
    # module("1713359491751x498199104691896300","1740565185084x758238934404231000")

