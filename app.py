import streamlit as st
import pandas as pd

def main():
    st.title("""
    #Phone Usage and its impact on studies
    ##data collection for *project work*""")

    # User inputs
    name = st.text_input("Enter your name:")
    age = st.number_input("Enter your age:", min_value=0, max_value=120, step=1)
    gender = st.radio("Select your gender:", ["Male", "Female", "Other"])
    has_phone = st.radio("Do you own a phone?", ("Yes", "No"))

    os = None
    if has_phone == "Yes":
        os = st.selectbox("Which OS do you use?", ["Android", "iOS"])

    usage_frequency = st.slider("Your average screen time (hours):", 0, 24, 1)
    purpose = st.text_area("What do you primarily use your phone for?")
    activity = st.text_area("What activity do you use most on your phone?")
    help = st.radio("Is your phone helpful for studying?", ("Yes", "No"))
    performance_impact = st.selectbox("Impact on your performance:", ["Improved", "Neutral", "Disimproved"])
    distraction = st.selectbox("Main source of distraction:", ["Short-form content", "Gaming", "Watching movies and web series", "Other"])
    usage_symptoms = st.selectbox("Symptoms you experience from phone usage:", ["None", "Headache", "Sleep disturbance", "Stress and anxiety"])
    symptom_frequency = st.selectbox("Frequency of symptoms:", ["Never", "Rarely", "Sometimes", "Frequently"])

    # Data to be saved
    data = {
        "Name": name,
        "Age": age,
        "Gender": gender,
        "Has Phone": has_phone,
        "OS": os if os else "N/A",
        "Usage Frequency": usage_frequency,
        "Purpose": purpose,
        "Activity": activity,
        "Helpful": help,
        "Performance Impact": performance_impact,
        "Distraction": distraction,
        "Usage Symptoms": usage_symptoms,
        "Symptom Frequency": symptom_frequency,
    }

    # Save button
    if st.button("Submit"):
        # Check if mandatory fields are filled
        if not all([name, purpose, activity]):
            st.error("Please fill all the required fields.")
        else:
            # Load existing data or create a new DataFrame
            try:
                df = pd.read_csv("phone_usage_data.csv")
            except FileNotFoundError:
                df = pd.DataFrame(columns=["Name", "Age", "Gender", "Has Phone", "OS", "Usage Frequency", "Purpose", "Activity", "Helpful", "Performance Impact", "Distraction", "Usage Symptoms", "Symptom Frequency"])

            # Append new data to DataFrame
            new_data = pd.DataFrame(data, index=[0])
            df = pd.concat([df, new_data], ignore_index=True)

            # Save DataFrame to CSV
            df.to_csv("phone_usage_data.csv", index=False)
            st.success("Data saved successfully!")

            # Display the DataFrame in the app
            st.dataframe(df)

            # Create a download button for the CSV file
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Press to Download",
                csv,
                "phone_usage_data.csv",
                "text/csv",
                key='download-csv'
            )

if __name__ == "__main__":
    main()
