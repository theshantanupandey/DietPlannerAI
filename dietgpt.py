import anthropic
import streamlit as st

# Initialize Anthropic API
client = anthropic.Anthropic(api_key="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")

def generate_diet_plan_with_claude(user_data):
    try:
        # Create message for Claude
        message = f"""Create a personalized vegetarian diet plan for an Indian user with the following details:

Age: {user_data['age']}
Gender: {user_data['gender']}
Waist Circumference: {user_data['waist_circumference']} cm
Height: {user_data['height']} cm
Weight: {user_data['weight']} kg
Activity Level: {user_data['activity_level']} (1-5)
Alcohol Consumption: {user_data['alcohol_consumption']}
Dairy Products Consumption: {user_data['dairy_consumption']}
Allergies: {user_data['allergies']}
Prescription Drugs: {user_data['prescription_drugs']}
Goal: {user_data['goal']}

Provide a detailed weekly diet plan considering the user's goal and dietary preferences. Also mention what foods will help with what issues that the user has."""

        # Call Anthropic API using the Messages API
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            temperature=0.7,
            messages=[
                {"role": "user", "content": message}
            ]
        )

        # Extract and return the generated text
        diet_plan = response.content[0].text
        return diet_plan
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit Web App
st.title('Personalized Vegetarian Diet Plan Generator for Indians')

# User input form
with st.form("user_input_form"):
    age = st.number_input('Age', min_value=1, max_value=120, value=25)
    gender = st.selectbox('Gender', ['M', 'F'])
    waist_circumference = st.number_input('Waist Circumference (cm)', min_value=50, max_value=200, value=80)
    height = st.number_input('Height (cm)', min_value=100, max_value=250, value=170)
    weight = st.number_input('Weight (kg)', min_value=30, max_value=200, value=70)
    activity_level = st.selectbox('Activity Level', ['sedentary', 'lightly active', 'moderatley active', 'Very Active', 'Extremely Active'])
    alcohol_consumption = st.selectbox('Alcohol Consumption', ['yes', 'no'])
    dairy_consumption = st.selectbox('Dairy Products Consumption', ['yes', 'no'])
    allergies = st.text_input('Allergies (comma separated)')
    prescription_drugs = st.text_input('Prescription Drugs Currently Taken')
    goal = st.selectbox('Goal', ['weight loss', 'maintenance', 'muscle gain'])

    submit_button = st.form_submit_button("Generate Diet Plan")

if submit_button:
    # Collect user data
    user_data = {
        'age': age,
        'gender': gender,
        'waist_circumference': waist_circumference,
        'height': height,
        'weight': weight,
        'activity_level': activity_level,
        'alcohol_consumption': alcohol_consumption,
        'dairy_consumption': dairy_consumption,
        'allergies': allergies,
        'prescription_drugs': prescription_drugs,
        'goal': goal
    }

    with st.spinner('Generating your personalized diet plan...'):
        diet_plan = generate_diet_plan_with_claude(user_data)
        st.write("### Your Personalized Diet Plan")
        st.write(diet_plan)