import streamlit as st
import openai

# Set your OpenAI API key here
openai.api_key = st.secrets["INSANIYA"]

# Streamlit app
st.title("Health Report Generator")
def generate_wellness_plan(problem, medical_history, medications, age, gender, sleep_pattern, activity_level, custom,
                            plan_duration, customization_options):
    wellness_prompt = ""
    if plan_duration == "Full Week":
        wellness_prompt = f"""
        Problem: {problem}
        Medical History: {medical_history}
        Medications: {medications}
        Age: {age}
        Gender: {gender}
        Sleep Pattern: {sleep_pattern}
        Physical Activity Level: {activity_level}
        set of instructions you need to follow: {custom}

        give me a personalized wellness plan for a week based on the provided information in a structured tabular format.Give a special note at the end.
        """
    else:
        wellness_prompt = f"""
        Problem: {problem}
        Medical History: {medical_history}
        Medications: {medications}
        Age: {age}
        Gender: {gender}
        Sleep Pattern: {sleep_pattern}
        Physical Activity Level: {activity_level}
        set of instructions you need to follow: {custom}

        give me a personalized wellness plan for today based on the provided information.    
        """

    # Add customization options to the prompt
    wellness_prompt += f"\nCustomization Options: {customization_options}"

    return wellness_prompt

# Input form
name = st.text_input("Name:")
gender = st.radio("Gender:", ["Male", "Female", "Other"])
age = st.number_input("Age:")
problem = st.text_input("Health condition:")

# Button to generate report
if st.button("Generate Report"):
    # Generate the report using OpenAI API
    prompt = f"Act as a  medical professional.Use the {age}, {gender}, {problem} to generate a personalized Health Report\n\n\nAI Instructions :\n\n1.Use the following REPORT FORMAT \'name:{name}\n \nGender:{gender}\n \nAge:{age} \nAbout the condition you are facing: \n\nCAUSES:\n\nCURES:\n\nPrescribed Medicines:\'\n\n2. Make it like a real report in a structed points for prescribed medicines\n\n3. Use the given 4 inputs to generate the report in the specified format"


    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=300
    )

    generated_report = response['choices'][0]['text']

    # Display the generated report
    st.subheader("Generated Report:")
    st.markdown(generated_report)
medical_history = st.text_area("Provide a brief medical history:")
medications = st.text_area("List any medications you are currently taking:")
sleep_pattern = st.text_area("describe your sleeping pattern")
activity_level = st.selectbox("Select your physical activity level:", ["Low", "Moderate", "High"])
personalization = st.text_area("you can add your customization")
plan_duration = st.radio("Select plan duration:", ["Full Week", "Today"])

if st.button("Generate Wellness Plan"):
    # Generate the wellness plan using OpenAI API
    wellness_prompt = generate_wellness_plan(problem, medical_history, medications, age, gender, sleep_pattern, activity_level, personalization, plan_duration, "")
    response = openai.Completion.create(
    engine="gpt-3.5-turbo-instruct",
    prompt=wellness_prompt,
    max_tokens=300
    )
    wellness_plan = response['choices'][0]['text']

    st.subheader("Generated Wellness Plan:")
    st.write(wellness_plan)
