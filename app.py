import streamlit as st
import re
import random
import string

# Set page config
st.set_page_config(
    page_title="🛡️ SecureKey Guardian - Password Strength Analyzer",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Set page title and custom CSS
st.markdown("""
    <style>
    /* Hide the default Streamlit menu button */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stTextInput > div > div > input {
        font-size: 20px;
    }
    .feedback {
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .weak { background-color: #ffebee; color: #c62828; }
    .moderate { background-color: #fff3e0; color: #ef6c00; }
    .strong { background-color: #e8f5e9; color: #2e7d32; }
    .title {
        font-size: 48px;
        font-weight: bold;
        margin-bottom: 15px;
        text-align: center;
        color: #2e4053;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.15);
        padding: 20px 0;
    }
    .subtitle {
        font-size: 24px;
        font-weight: normal;
        margin-bottom: 25px;
        text-align: center;
        color: #34495e;
    }
    </style>
    """, unsafe_allow_html=True)

# Constants
COMMON_PASSWORDS = {
    'password', 'password123', '123456', 'qwerty', 'admin',
    'letmein', 'welcome', 'monkey', 'abc123', '111111'
}

SAMPLE_PASSWORDS = {
    'weak': 'password123',
    'moderate': 'Password123!',
    'better': 'Purpl3%Elephant',
    'strong': 'Kj#9mP$vN2xQ'
}

PASSWORD_THEMES = {
    '🐾 Animal Theme': {'desc': 'Combine two animals with numbers and symbols', 'example': 'Lion$Tiger42'},
    '🌈 Color Theme': {'desc': 'Mix colors with special characters', 'example': 'Blue#Red&95'},
    '🌍 Travel Theme': {'desc': 'Combine cities or countries with symbols', 'example': 'Paris@Tokyo55'},
    '🍕 Food Theme': {'desc': 'Mix your favorite foods with numbers', 'example': 'Pizza#Sushi23'}
}

def generate_password(length=12):
    """Generate a strong random password."""
    char_sets = {
        'lowercase': string.ascii_lowercase,
        'uppercase': string.ascii_uppercase,
        'digits': string.digits,
        'special': "!@#$%^&*"
    }
    
    # Ensure at least one of each character type
    password = [random.choice(v) for v in char_sets.values()]
    
    # Fill the rest with random characters
    all_chars = ''.join(char_sets.values())
    password.extend(random.choice(all_chars) for _ in range(length - len(password)))
    
    # Shuffle the password
    random.shuffle(password)
    return ''.join(password)

def check_password_strength(password):
    """Check password strength and return score and feedback."""
    score = 0
    feedback = []
    
    # Basic checks dictionary
    checks = {
        'length': {
            'test': lambda p: len(p) >= 12,
            'score': 2,
            'fallback_test': lambda p: len(p) >= 8,
            'fallback_score': 1,
            'message': "❌ Password should be at least 8 characters long (12+ recommended)."
        },
        'case': {
            'test': lambda p: bool(re.search(r"[A-Z]", p) and re.search(r"[a-z]", p)),
            'score': 1,
            'message': "❌ Include both uppercase and lowercase letters."
        },
        'digits': {
            'test': lambda p: bool(re.search(r"\d", p)),
            'score': 1,
            'message': "❌ Add at least one number (0-9)."
        },
        'special': {
            'test': lambda p: bool(re.search(r"[!@#$%^&*]", p)),
            'score': 1,
            'message': "❌ Include at least one special character (!@#$%^&*)."
        }
    }
    
    # Check if password is in common password list
    if password.lower() in COMMON_PASSWORDS:
        feedback.append("❌ This is a commonly used password. Please choose something more unique.")
        return 0, feedback
    
    # Perform basic checks
    for check in checks.values():
        if check.get('fallback_test'):
            if check['test'](password):
                score += check['score']
            elif check['fallback_test'](password):
                score += check['fallback_score']
            else:
                feedback.append(check['message'])
        else:
            if check['test'](password):
                score += check['score']
            else:
                feedback.append(check['message'])
    
    # Pattern checks
    patterns = {
        'repeating': (r"(.)\1\1", "❌ Avoid repeating characters (e.g., 'aaa')."),
        'sequential_letters': (lambda p: any(
            str1.isalpha() and str2.isalpha() and str3.isalpha() and
            ord(str2) - ord(str1) == 1 and ord(str3) - ord(str2) == 1
            for str1, str2, str3 in zip(p[:-2].lower(), p[1:-1].lower(), p[2:].lower())
        ), "❌ Avoid sequential letters (e.g., 'abc')."),
        'sequential_numbers': (lambda p: any(
            str1.isdigit() and str2.isdigit() and str3.isdigit() and
            int(str2) - int(str1) == 1 and int(str3) - int(str2) == 1
            for str1, str2, str3 in zip(p[:-2], p[1:-1], p[2:])
        ), "❌ Avoid sequential numbers (e.g., '123').")
    }
    
    for pattern, (test, message) in patterns.items():
        if callable(test):
            if test(password):
                score -= 1
                feedback.append(message)
        elif re.search(test, password):
            score -= 1
            feedback.append(message)
    
    return max(0, score), feedback

def display_password_strength(score, feedback):
    """Display password strength and feedback."""
    # Display strength meter
    st.write("\n### Password Strength:")
    if score <= 2:
        st.markdown('<p class="feedback weak">❌ Weak Password</p>', unsafe_allow_html=True)
        strength_message = "⚠️ This password could be cracked quickly!"
    elif score <= 3:
        st.markdown('<p class="feedback moderate">⚠️ Moderate Password</p>', unsafe_allow_html=True)
        strength_message = "⏳ This password might take a few hours to crack."
    else:
        st.markdown('<p class="feedback strong">✅ Strong Password</p>', unsafe_allow_html=True)
        strength_message = "🔒 This password would take a very long time to crack!"
    
    # Create a progress bar for visual feedback
    st.progress(score/5)
    
    # Display feedback
    if feedback:
        st.write("\n### Suggestions for Improvement:")
        for item in feedback:
            st.write(item)
    elif score >= 4:
        st.success("🎉 Excellent! Your password meets all security criteria.")
    
    # Display estimated strength
    st.write(strength_message)
    
    return score >= 5  # Return whether password is perfect

def display_achievement(score):
    """Display achievement badge based on score."""
    achievements = {
        5: ("🏆 MASTER PASSWORD CREATOR!", "success", True),
        4: ("🥇 EXPERT PASSWORD SMITH!", "success", False),
        3: ("🥈 SKILLED PASSWORD APPRENTICE!", "warning", False),
        0: ("🎯 Keep practicing! You'll get there!", "error", False)
    }
    
    for threshold, (message, level, show_balloons) in achievements.items():
        if score >= threshold:
            if show_balloons:
                st.balloons()
            getattr(st, level)(message)
            break
    
    # Display score with emoji meter
    st.write("Your Score:", "🔒" * score + "⭕" * (5-score), f"({score}/5)")

def main():
    """Main application function."""
    # Header
    st.markdown('<h1 class="title">🛡️ SecureKey Guardian</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your Personal Password Strength Builder</p>', unsafe_allow_html=True)
    st.write("Transform your passwords from vulnerable to unbreakable!")
    
    # Safety disclaimer
    st.info("⚠️ Practice creating strong passwords without security risks! Use dummy passwords to learn how to enhance your security without entering real credentials.", )
    
    # Main password input and check
    password = st.text_input("Enter your password:", type="password")
    
    # Generate password button
    if st.button("Generate Strong Password"):
        generated_password = generate_password()
        st.code(generated_password, language=None)
        st.info("👆 Copy this password and use it in the checker above to verify its strength!")
    
    if password:
        score, feedback = check_password_strength(password)
        display_password_strength(score, feedback)
    
    # Password Requirements
    with st.expander("Password Requirements 📋"):
        st.write("""
        A strong password should:
        - Be at least 8 characters long (12+ recommended)
        - Contain uppercase & lowercase letters
        - Include at least one digit (0-9)
        - Have one special character (!@#$%^&*)
        - Not be a commonly used password
        - Avoid repeating characters (e.g., 'aaa')
        - Avoid sequential patterns (e.g., 'abc', '123')
        """)
    
    # Security Tips
    st.markdown("---")
    st.markdown("""
        ### 🔐 Password Security Tips:
        1. Never use the same password for multiple accounts
        2. Consider using a password manager
        3. Enable two-factor authentication when possible
        4. Change passwords regularly
        5. Never share your passwords with anyone
    """)
    
    # Interactive Password Evolution Experiment
    st.markdown("---")
    st.markdown("## 🔬 Password Strength Experiment Lab")
    st.write("Let's learn about password strength through a fun experiment!")
    
    with st.expander("🧪 Interactive Password Evolution Experiment"):
        for stage, (desc, password) in enumerate([
            ("Starting with a Basic Password", SAMPLE_PASSWORDS['weak']),
            ("Adding Complexity", SAMPLE_PASSWORDS['moderate']),
            ("Making it Unique", SAMPLE_PASSWORDS['better']),
            ("The Perfect Password", SAMPLE_PASSWORDS['strong'])
        ], 1):
            st.markdown(f"#### {stage}️⃣ {desc}")
            st.code(password)
            if st.button(f"Test '{password}'"):
                score, feedback = check_password_strength(password)
                st.write(f"Score: {score}/5")
                for item in feedback:
                    st.write(item)
    
    # Password Creation Game
    st.markdown("---")
    st.markdown("## 🎮 Password Creation Game")
    st.write("Try creating passwords following these fun themes and test their strength:")
    
    for theme, details in PASSWORD_THEMES.items():
        st.markdown(f"\n{theme}: {details['desc']}")
        st.markdown(f"- Example: `{details['example']}`")
    
    st.markdown("\nRemember: The key is to be creative while following security rules!")
    
    # Password Master Challenge
    st.markdown("## 🏆 Password Master Challenge")
    challenge_password = st.text_input("Create your ultimate password:", type="password", key="challenge")
    if challenge_password:
        score, feedback = check_password_strength(challenge_password)
        display_achievement(score)

if __name__ == "__main__":
    main() 