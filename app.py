import streamlit as st
import re
from collections import Counter
import pandas as pd
import plotly.express as px

# --------------------------
# Toxic Words by Category
toxic_words_dict = {
    "Swear": ["fuck","fucker","bitch","asshole","shit","damn","hell"],
    "Insult": ["dumb","stupid","idiot","moron","fool","dunce","moronic","brainless","idiotic",
               "ignorant","simpleton","dimwit","jerk","twit","scumbag","weirdo","slob","geek","ugly"],
    "Threat/Mock": ["shut up","go away","die","kill yourself","nobody likes you","worthless",
                    "drop dead","get lost","leave me alone","screw you","hate you","you're pathetic",
                    "you're a joke","you suck","you are trash","you're useless","you have no life",
                    "i hate you","you are disgusting","you are gross","go kill yourself",
                    "noob","trash","pathetic","lame","weird","nerd","creepy","sad","suck","fail",
                    "tryhard","clown","troll"],
    "Body-shaming": ["fat","skinny","overweight","obese","chubby","flabby","bony","short","tall","gross",
                      "hideous","unattractive","beanpole","lardass","skinny-fat","chunky","plump","bulky",
                      "scruffy","ugly face","fat face","skinny legs","bald","unattractive smile","gross hair"]
}

# Merge all words into one list for detection
toxic_words = [word for words in toxic_words_dict.values() for word in words]

# --------------------------
# Detection + Toxicity Scoring
def analyze_text(text):
    text_lower = text.lower()
    found_toxic = []

    for word in toxic_words:
        if re.search(rf'\b{re.escape(word)}\b', text_lower):
            found_toxic.append(word)

    # Scoring
    score = len(found_toxic)
    if score == 0:
        category = "Safe"
    elif score <= 2:
        category = "Mildly Toxic"
    elif score <= 4:
        category = "Moderately Toxic"
    else:
        category = "Highly Toxic"

    return {
        "original": text,
        "highlighted": highlight_toxic(text, found_toxic),
        "found_toxic_words": found_toxic,
        "score": score,
        "category": category
    }

# --------------------------
# Highlight toxic words with category colors (HTML span)
def highlight_toxic(text, toxic_list):
    highlighted = text
    for word in set(toxic_list):
        for cat, words in toxic_words_dict.items():
            if word.lower() in words:
                color = {
                    "Swear": "red",
                    "Insult": "orange",
                    "Threat/Mock": "purple",
                    "Body-shaming": "blue"
                }[cat]
                highlighted = re.sub(
                    rf'\b{re.escape(word)}\b',
                    f"<span style='color:{color}; font-weight:bold'>{word}</span>",
                    highlighted,
                    flags=re.IGNORECASE
                )
    return highlighted

# --------------------------
# Streamlit App
st.title("Cyberbullying & Toxicity Detector 💬")
st.write("Analyze conversations for toxic language and visualize results.")

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []

text = st.text_area("Enter a message or comment to analyze:")

if st.button("Analyze"):
    result = analyze_text(text)

    # Store message in session history
    st.session_state.history.append({
        "Message": result["original"],
        "Toxic Words": ', '.join(result["found_toxic_words"]),
        "Score": result["score"],
        "Message Category": result["category"]
    })

    # ----------------------
    # Layout: columns for results and chart
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Analysis Results")
        st.write("*Message Type:*", result["category"])
        st.write("*Toxicity Score (0–10):*", result["score"])
        st.markdown("*Original Message with Highlights:*")
        st.markdown(result["highlighted"], unsafe_allow_html=True)

        if result["found_toxic_words"]:
            st.warning(f"Toxic Words Detected: {', '.join(result['found_toxic_words'])}")
        else:
            st.success("No toxic words detected!")

    # ----------------------
    # Bar chart only if toxic words exist
    with col2:
        if result["found_toxic_words"]:
            category_counts = {"Swear":0, "Insult":0, "Threat/Mock":0, "Body-shaming":0}
            for word in result["found_toxic_words"]:
                for cat, words in toxic_words_dict.items():
                    if word in words:
                        category_counts[cat] += 1

            df_stack = pd.DataFrame({
                "Category": list(category_counts.keys()),
                "Count": list(category_counts.values()),
                "Toxicity": ["Total"]*len(category_counts)
            })

            fig = px.bar(
                df_stack,
                x="Toxicity",
                y="Count",
                color="Category",
                color_discrete_map={
                    "Swear":"red",
                    "Insult":"orange",
                    "Threat/Mock":"purple",
                    "Body-shaming":"blue"
                },
                text="Count"
            )

            fig.update_traces(textposition='inside')
            fig.update_layout(
                title="Toxic Words by Category",
                yaxis_title="Count",
                xaxis_title="",
                barmode='stack',
                template="plotly_white",
                showlegend=True,
                yaxis=dict(range=[0,10])
            )

            st.plotly_chart(fig, use_container_width=True)

    # ----------------------
    # Pie chart (multi-color for toxic words)
    if result["found_toxic_words"]:
        pie_counts = {"Swear":0, "Insult":0, "Threat/Mock":0, "Body-shaming":0}
        for word in result["found_toxic_words"]:
            for cat, words in toxic_words_dict.items():
                if word in words:
                    pie_counts[cat] += 1
        # Only non-zero categories
        df_pie = pd.DataFrame({
            "Category": [k for k, v in pie_counts.items() if v > 0],
            "Count": [v for v in pie_counts.values() if v > 0]
        })
        fig_pie = px.pie(
            df_pie,
            names='Category',
            values='Count',
            title='Toxic Words Breakdown by Category',
            color='Category',
            color_discrete_map={
                "Swear":"red",
                "Insult":"orange",
                "Threat/Mock":"purple",
                "Body-shaming":"blue"
            },
            hole=0.3
        )
    else:
        df_pie = pd.DataFrame({"Category":["Safe"], "Count":[1]})
        fig_pie = px.pie(
            df_pie,
            names='Category',
            values='Count',
            title='Message Toxicity',
            color='Category',
            color_discrete_map={"Safe":"green"},
            hole=0.3
        )

    fig_pie.update_traces(textposition='inside', pull=[0.05]*len(df_pie))
    st.plotly_chart(fig_pie)

    # ----------------------
    # Eye-catching final overall message
    current_toxic_count = result["score"]

    if current_toxic_count >= 5:
        final_message = "❌➡ *OVERALL CONVERSATION: HIGHLY TOXIC!* ⚠💀"
        st.markdown(f"<h2 style='color:red;text-align:center;'>{final_message}</h2>", unsafe_allow_html=True)
    elif result["category"] == "Highly Toxic":
        final_message = "❌➡ *OVERALL CONVERSATION: HIGHLY TOXIC!* ⚠💀"
        st.markdown(f"<h2 style='color:red;text-align:center;'>{final_message}</h2>", unsafe_allow_html=True)
    elif result["category"] == "Moderately Toxic":
        final_message = "⚠➡ *OVERALL CONVERSATION: MODERATELY TOXIC!* 🔥"
        st.markdown(f"<h2 style='color:orange;text-align:center;'>{final_message}</h2>", unsafe_allow_html=True)
    elif result["category"] == "Mildly Toxic":
        final_message = "⚠➡ *OVERALL CONVERSATION: MILDLY TOXIC!* ⚡"
        st.markdown(f"<h2 style='color:gold;text-align:center;'>{final_message}</h2>", unsafe_allow_html=True)
    else:
        final_message = "✅➡ *OVERALL CONVERSATION: SAFE!* 🌟🎉"
        st.markdown(f"<h2 style='color:green;text-align:center;'>{final_message}</h2>", unsafe_allow_html=True)

    # ----------------------
    # CSV download at the end
    df_history = pd.DataFrame(st.session_state.history)
    csv = df_history.to_csv(index=False, encoding='utf-8')
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    st.download_button(
        "📥 Download Full Conversation Report as CSV",
        data=csv,
        file_name="conversation_report.csv",
        mime="text/csv"
    )
    st.markdown("</div>", unsafe_allow_html=True)
# redeploy update
