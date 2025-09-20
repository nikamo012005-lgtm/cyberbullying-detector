import streamlit as st
import re
from collections import Counter
import matplotlib.pyplot as plt

# --------------------------
# 1️⃣ Mappings: Toxic → Safe
mapping_dict = {
    # Example subset from your mapping
    "dumb": "smart",
    "stupid": "clever",
    "idiot": "genius",
    "moron": "bright",
    "fool": "wise",
    "loser": "winner",
    "ugly": "beautiful",
    "fat": "fit",
    "skinny": "healthy",
    "freak": "unique",
    "shut up": "speak kindly",
    "go away": "come closer",
    "die": "live",
    "kill yourself": "stay strong",
    "nobody likes you": "everyone appreciates you",
    # Add all the mappings you have here...
}

# --------------------------
# 2️⃣ Full toxic word/phrase list (~500 words)
full_toxic_list = [
"dumb","stupid","idiot","moron","fool","loser","simpleton","imbecile","silly","brainless",
"clueless","weakling","pathetic","wimp","crybaby","idiot kid","retard","nitwit","slowpoke",
"blockhead","bonehead","halfwit","dimwit","dork","nerd","weirdo","freak","goof","twit",
"dummy","ignoramus","sap","foolish","numbskull","dunce","goner","worthless","spineless",
"coward","baby","small-minded","trash","loserass","noob","scrub","fail","lame","lowlife",
"pushover","jerk","jerkface","brat","bratty","brathead","wretched","scumbag","lowbrain",
"weak","pathetic loser","sad excuse","trashbag","bum","flunky","loser kid","lowlife trash",
"joke","joke ass","zero","brain-dead","dim","cretin",
"ugly","fat","skinny","freak","pig","troll","disgusting","hideous","gross","ugly duckling",
"shorty","chubby","lanky","anorexic","beefy","tubby","flat","scrawny","hideous face",
"deformed","freaky","nasty","ugly ass","buttface","noseface","pigface","fatty","cellulite",
"lardass","blob","whale","monster","repulsive","troll face","freakshow","scumbag body",
"overweight","underweight","ugly ass face","lumpy","hunchback","saggy","toothless","greasy",
"dirty","homely","stinky","smelly","puke","ugly ass body","blobfish","porker",
"shut up","go away","die","kill yourself","nobody likes you","you're worthless","go cry",
"stop talking","leave me alone","suck it","eat shit","get lost","crawl away","fade away",
"stop existing","go rot","die slowly","jump off","self-destruct","vanish","disappear","useless",
"worthless piece of trash","die now","off yourself","kill it","die kid","rot in hell",
"drop dead","die freak","go to hell","piss off","fuck off","leave","leave forever",
"stop breathing","go jump","end it","nobody cares","crawl back","die bitch","go die loser",
"fuck","fucking","fucker","asshole","bitch","bastard","crap","shit","damn","hell","dick",
"dickhead","pussy","cunt","motherfucker","balls","wanker","prick","jerk","jerkface","bitchface",
"dumbfuck","son of a bitch","cock","cockhead","asshat","twat","dickwad","dickweed","shithole",
"shitter","jackass","douche","douchebag","fag","faggot","retard","hellhole","piss","piss off",
"screw you","bloody","bollocks","bugger","tosser","wazzock","knobhead","arsehole","prissy",
"twitface","shitbag","shithead","fucknut","fuckwit","cuntface","fuckboy","shitforbrains",
"hellhole","jerkoff","dickbrain","bollockshead","cockface","dickface","wank","wankface",
"assface","fucktard","asswipe","dickbag","pussyface","prickface","cockwad","dickwad",
"fuckhead","bastardface","cocksucker","shitfuck","assmunch","turd","shitstain",
"noob","newbie","trash","bot","hacker loser","fake","lame","tryhard","fail","scrub",
"ragequit","camper","exploit abuser","cheapshot","k/d whore","loot stealer","griefing",
"trash player","casual","p2w loser","git gud","lagger","spawn camper","newbie idiot","troll",
"feeder","ragebaby","weak player","feeder kid","wimp gamer","low-rank","ragequit kid","toxic",
"git","clutcher loser","pay-to-win loser","trash noob","spammer",
"you suck","i hate you","pathetic loser","kill yourself","you're trash","nobody cares about you",
"you're disgusting","idiot fuck","stop existing","you're worthless","get a life","go rot",
"die loser","sad excuse","worthless piece of shit","ugly ass","fuck you","screw you","go die",
"i don't like you","you're a joke","pathetic ass","worthless kid","loser trash","die freak",
"creep","go cry loser","shut your mouth","nobody wants you","crawl away loser","go jump off",
"die slowly","fade away loser","loser ass","dumbass","crybaby kid","you suck at life","weak ass",
"you're a waste","loserface","pathetic excuse","go die now","stop breathing","you're a failure",
"worthless freak","fuckface","wimp ass","loser kid","pathetic idiot","go disappear",
"slut","whore","hoe","bitch","skank","tramp","dickgirl","cockslut","fucktoy","pussywhip",
"cumdump","tease","horny","fuckable","slutbag","sex toy","dickhole","slutface","whoreface",
"fuckgirl","slutty","fuckboy","player","cockslapper","pussyface","fuckbuddy","sexed",
"fucker kid","slutty bitch","fuckme","sexual predator","teaseface","whorebag","dickslap"
]

# --------------------------
# 3️⃣ Detection + Safe Conversion
def detect_and_convert(text):
    text_lower = text.lower()
    found_toxic = []
    unmapped_toxic = []
    safe_text = text

    for word in full_toxic_list:
        if re.search(rf'\b{re.escape(word)}\b', text_lower):
            found_toxic.append(word)
            if word in mapping_dict:
                # Replace toxic word with safe word
                safe_text = re.sub(rf'\b{re.escape(word)}\b', mapping_dict[word], safe_text, flags=re.IGNORECASE)
            else:
                unmapped_toxic.append(word)

    # Determine message type
    if found_toxic:
        message_type = "Toxic"
    elif text.strip() != "":
        message_type = "Safe"
    else:
        message_type = "Neutral"

    return {
        "original": text,
        "safe_version": safe_text,
        "found_toxic_words": found_toxic,
        "unmapped_toxic_words": unmapped_toxic,
        "type": message_type
    }

# --------------------------
# 4️⃣ Streamlit App
st.title("Cyberbullying & Harassment Detector 💬")

text = st.text_area("Enter a message or comment to analyze:")

if st.button("Analyze"):
    result = detect_and_convert(text)

    st.subheader("Analysis Results")
    st.write("*Message Type:*", result["type"])
    st.write("*Original Message:*", result["original"])
    st.write("*Safe Version:*", result["safe_version"])

    if result["found_toxic_words"]:
        st.warning(f"Toxic / Offensive Words Detected: {', '.join(result['found_toxic_words'])}")
    if result["unmapped_toxic_words"]:
        st.error(f"Unmapped Toxic Words (No safe word available): {', '.join(result['unmapped_toxic_words'])}")
    if not result["found_toxic_words"]:
        st.success("No toxic words detected!")

    # ----------------------
    # Pie Chart: Safe vs Toxic vs Neutral
    counts = Counter([result["type"]])
    labels = ["Safe", "Toxic", "Neutral"]
    sizes = [counts.get(label, 0) for label in labels]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['green','red','gray'])
    ax1.axis('equal')
    st.pyplot(fig1)
