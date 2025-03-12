import streamlit as st
import re
import random
import string

# Configure Streamlit's behavior and security settings
st.set_page_config(
    page_title="🛡️ SecureKey Guardian",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "# SecureKey Guardian\nA secure password strength analyzer and generator."
    }
)

# Add security headers and configure browser features
st.markdown("""
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#2e4053">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Permissions-Policy" content="ambient-light-sensor=(), battery=(), document-domain=(), layout-animations=(), oversized-images=(), sync-xhr=(), wake-lock=(), vr=()">
    <meta http-equiv="Content-Security-Policy" content="default-src 'self' 'unsafe-inline' 'unsafe-eval' data: blob:; connect-src 'self' https:; img-src 'self' data: https:; frame-ancestors 'none';">
    """, unsafe_allow_html=True)

# Custom CSS with improved styling, form handling, and cross-browser compatibility
st.markdown("""
    <style>
    /* Reset and base styles */
    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        -webkit-text-size-adjust: 100%;
        text-size-adjust: 100%;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Override Streamlit's default padding */
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        margin-top: 0 !important;
    }

    .stApp > header {
        display: none;
    }

    /* Base styles */
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0;
        min-height: 100vh;
        min-height: -webkit-fill-available;
        min-height: stretch;
        background-color: #ffffff; /* White background for the app */
    }
    
    /* Scrollbar styling */
    * {
        scrollbar-width: thin;
        -webkit-scrollbar-width: thin;
    }
    
    *::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    *::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    *::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 4px;
    }
    
    /* Desktop-optimized container */
    .container {
        width: 100%;
        max-width: 1200px;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
    }
    
    /* Two-column layout for desktop */
    .desktop-grid {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 1.5rem;
        align-items: start;
        margin: 1rem 0 1.5rem;
    }
    
    @media (max-width: 768px) {
        .desktop-grid {
            grid-template-columns: 1fr;
        }
    }
    
    /* Form styles with accessibility improvements */
    .form-group {
        background: #f8f9fa;
        border-radius: 12px;
        padding: clamp(20px, 3vw, 30px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }
    
    .form-label {
        display: block;
        margin-bottom: 12px;
        font-size: clamp(16px, 2vw, 18px);
        color: #2e4053;
        font-weight: 600;
    }
    
    .password-input {
        width: 100%;
        padding: 12px 16px;
        border: 2px solid #e0e3e8;
        border-radius: 8px;
        font-size: clamp(16px, 2vw, 18px);
        margin-bottom: 12px;
        transition: all 0.3s ease;
        background-color: white;
    }
    
    .password-input:focus {
        outline: none;
        border-color: #2e4053;
        box-shadow: 0 0 0 3px rgba(46,64,83,0.1);
    }
    
    .help-text {
        font-size: 14px;
        color: #666;
        margin-top: 8px;
    }
    
    /* Button improvements */
    .stButton button {
        background-color: #2e4053 !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        max-width: 300px !important;
        margin: 1rem auto !important;
        cursor: pointer;
    }
    
    .stButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(46,64,83,0.2) !important;
    }
    
    /* Card improvements */
    .theme-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: transform 0.3s ease;
    }
    
    .theme-card:hover {
        transform: translateY(-2px);
    }
    
    /* Section spacing improvements */
    .section {
        margin: 1rem 0;
        position: relative;
    }
    
    .section:not(:last-child)::after {
        content: "";
        position: absolute;
        bottom: -0.5rem;
        left: 20%;
        right: 20%;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e0e3e8, transparent);
    }
    
    /* Section title improvements */
    .section h2 {
        font-size: clamp(24px, 3vw, 32px);
        color: #2e4053;
        margin-bottom: 1rem;
    }
    
    /* Divider styling */
    hr {
        border: none;
        border-top: 2px solid #f0f2f5;
        margin: 2rem 0;
    }
    
    /* Info box improvements */
    .stAlert {
        border-radius: 12px !important;
        padding: 0.4rem 0.75rem !important;
        margin: 0.1rem 0 0.5rem !important;
    }
    
    /* Progress bar enhancements */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #ff6b6b 0%, #ffd93d 50%, #6bcb77 100%) !important;
        border-radius: 8px !important;
    }
    
    /* Title styles */
    .title {
        font-size: clamp(36px, 8vw, 56px); /* Increased base size for larger mobile */
        font-weight: bold;
        margin: 1rem 0; /* Increased margin for spacing */
        text-align: center;
        color: #2e4053; /* Dark text color */
        padding: 0;
        line-height: 1.2; /* Adjusted line height */
    }
    
    /* New line below title */
    .title-line {
        width: 100%; /* Full width */
        height: 2px; /* Thickness of the line */
        background-color: #2e4053; /* Color of the line */
        margin: 0.5rem auto; /* Margin for spacing */
    }
    
    /* Subtitle styles */
    .subtitle {
        font-size: clamp(16px, 3vw, 24px); /* Responsive font size */
        font-weight: normal; /* Normal weight */
        margin: 0.5rem 0; /* Increased margin for spacing */
        text-align: center;
        color: #34495e; /* Darker subtitle color */
        line-height: 1.3; /* Adjusted line height */
    }
    
    /* Expander improvements */
    .streamlit-expanderHeader {
        margin: 0.75rem 0;
        padding: 0.75rem;
        background: transparent !important;
    }
    
    .streamlit-expanderContent {
        font-size: clamp(14px, 2vw, 16px);
    }
    
    /* Theme grid improvements */
    .theme-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Media Queries */
    @media screen and (max-width: 768px) {
        .stApp {
            padding: 0;
        }
        
        form {
            padding: 15px;
        }
        
        .feedback {
            padding: 12px;
        }
        
        .title {
            font-size: clamp(28px, 3vw, 24px);
            margin: 0 0 0.5rem;
        }
        
        .subtitle {
            font-size: clamp(12px, 2vw, 16px);
            margin: 0 0 0.3rem;
        }
        
        .heading-gradient {
            font-size: clamp(11px, 1.8vw, 14px);
            margin: 0.25rem 0 0.3rem;
        }
    }
    
    @media screen and (max-width: 480px) {
        .stApp {
            padding: 0 5px;
        }
        
        .theme-grid {
            grid-template-columns: 1fr;
        }
        
        .title {
            font-size: clamp(18px, 3vw, 24px); /* Smaller font size for mobile */
            margin: 0.5rem 0; /* Adjusted for mobile */
        }
        
        .subtitle {
            font-size: clamp(12px, 2vw, 16px); /* Smaller font size for mobile */
            margin: 0.5rem 0; /* Adjusted for mobile */
        }
        
        .heading-gradient {
            font-size: clamp(10px, 2vw, 14px); /* Smaller font size for mobile */
            margin: 0.4rem 0; /* Adjusted for mobile */
        }

        .safety-disclaimer {
            font-size: clamp(10px, 1.5vw, 12px); /* Smaller font size for mobile */
            margin: 0.4rem 0; /* Adjusted for mobile */
        }
    }
    
    /* Challenge section improvements */
    .challenge-section {
        background: linear-gradient(135deg, #2e4053 0%, #34495e 100%);
        padding: 1.5rem;
        border-radius: 16px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 2px solid rgba(255,255,255,0.1);
    }
    
    .challenge-title {
        color: white !important;
        text-align: center;
        font-size: clamp(24px, 4vw, 36px);
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        font-weight: bold;
        background: none;
        -webkit-text-fill-color: white;
    }
    
    .challenge-description {
        color: rgba(255,255,255,0.95);
        text-align: center;
        font-size: clamp(16px, 2vw, 18px);
        margin-bottom: 1.5rem;
        line-height: 1.6;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Button spacing */
    .stButton button {
        margin: 1rem auto !important;
    }
    
    /* Remove experiment lab box */
    .experiment-lab {
        margin: 1.5rem 0;
        padding: 0;
        background: transparent;
    }
    
    /* Remove password game box */
    .password-game {
        margin: 1.5rem 0;
        padding: 0;
    }
    
    /* Gradient heading styles */
    .heading-gradient {
        font-size: clamp(14px, 2.5vw, 22px); /* Responsive font size */
        font-weight: 600; /* Semi-bold for emphasis */
        background: linear-gradient(90deg, #2e4053, #34495e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 0.5rem 0; /* Adjusted margin for spacing */
        padding: 0;
        line-height: 1.2; /* Adjusted line height */
    }
    
    /* Safety disclaimer styles */
    .safety-disclaimer {
        font-size: clamp(12px, 2vw, 16px); /* Responsive font size */
        color: #ffcc00; /* Optional: Change color for emphasis */
        text-align: center;
        margin: 1rem 0; /* Increased margin for spacing */
        line-height: 1.3; /* Adjusted line height */
    }
    
    /* Footer styles */
    .footer {
        text-align: center;
        padding: 1rem 0;
        color: #2e4053;
        font-size: 0.9rem;
        font-weight: 500;
        opacity: 0.9;
        margin-top: auto;
    }

    /* Hover effects */
    .title:hover {
        background-color: rgba(46, 64, 83, 0.1); /* Light background on hover */
    }

    .subtitle:hover {
        color: #2e4053; /* Darker color on hover */
    }

    .heading-gradient:hover {
        transform: scale(1.02); /* Slightly enlarge on hover */
    }

    /* Media Queries for Mobile */
    @media screen and (max-width: 400px) {
        .title {
            font-size: 36px; /* Increased size for mobile below 400px */
            margin: 0.5rem 0; /* Adjusted for mobile */
        }
        
        .subtitle {
            font-size: 14px; /* Fixed size for mobile below 400px */
            margin: 0.5rem 0; /* Adjusted for mobile */
        }
        
        .heading-gradient {
            font-size: 12px; /* Fixed size for mobile below 400px */
            margin: 0.4rem 0; /* Adjusted for mobile */
        }

        .safety-disclaimer {
            font-size: 10px; /* Fixed size for mobile below 400px */
            margin: 0.4rem 0; /* Adjusted for mobile */
        }
    }

    /* Media Queries for larger mobile devices */
    @media screen and (max-width: 480px) {
        .title {
            font-size: clamp(16px, 3vw, 24px); /* Smaller font size for mobile */
            margin: 0.5rem 0; /* Adjusted for mobile */
        }
        
        .subtitle {
            font-size: clamp(12px, 2vw, 16px); /* Smaller font size for mobile */
            margin: 0.5rem 0; /* Adjusted for mobile */
        }
        
        .heading-gradient {
            font-size: clamp(10px, 2vw, 14px); /* Smaller font size for mobile */
            margin: 0.4rem 0; /* Adjusted for mobile */
        }

        .safety-disclaimer {
            font-size: clamp(10px, 1.5vw, 12px); /* Smaller font size for mobile */
            margin: 0.4rem 0; /* Adjusted for mobile */
        }
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
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<h1 class="title">🛡️ SecureKey Guardian</h1>', unsafe_allow_html=True)
    st.markdown('<div class="title-line"></div>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your Personal Password Strength Builder</p>', unsafe_allow_html=True)
    
    # Add gradient heading and safety disclaimer with reduced spacing
    st.markdown('<h3 class="heading-gradient">Strengthen your password from being vulnerable to unbreakable</h3>', unsafe_allow_html=True)
    st.info("⚠️ Practice creating strong passwords without security risks! Use dummy passwords to learn how to enhance your security without entering real credentials.")
    
    # Main content grid with reduced top margin
    st.markdown('<div class="desktop-grid" style="margin-top: 1rem;">', unsafe_allow_html=True)
    
    # Left column - Password checker and generator
    st.markdown('<div class="main-column">', unsafe_allow_html=True)
    
    # Unified Password Testing Section
    st.markdown("### 🔒 Test Your Password")
    st.markdown("Enter a password below or generate a strong one to test its strength!")
    
    # Single password input field
    password = st.text_input("Enter or paste a password:", type="password", key="password_input", 
                           help="Enter any password to check its strength",
                           placeholder="Type or paste a password here")
    
    # Generate password button
    if st.button("🎲 Generate Strong Password", key="generate_btn"):
        generated_password = generate_password()
        st.code(generated_password, language=None)
        st.info("👆 Copy this password and paste it above to verify its strength!")
    
    if password:
        score, feedback = check_password_strength(password)
        display_password_strength(score, feedback)
        display_achievement(score)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close main-column
    
    # Right column - Requirements and tips
    st.markdown('<div class="side-column">', unsafe_allow_html=True)
    
    with st.expander("📋 Password Requirements", expanded=True):
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
    
    with st.expander("🔐 Security Tips", expanded=True):
        st.markdown("""
        1. Never use the same password for multiple accounts
        2. Consider using a password manager
        3. Enable two-factor authentication when possible
        4. Change passwords regularly
        5. Never share your passwords with anyone
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close side-column
    st.markdown('</div>', unsafe_allow_html=True)  # Close desktop-grid
    
    # Interactive sections with improved spacing
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown("## 🔬 Password Strength Experiment Lab")
    st.write("Learn about password strength through these examples:")
    
    with st.expander("🧪 Interactive Password Evolution"):
        for stage, (desc, password) in enumerate([
            ("Starting with a Basic Password", SAMPLE_PASSWORDS['weak']),
            ("Adding Complexity", SAMPLE_PASSWORDS['moderate']),
            ("Making it Unique", SAMPLE_PASSWORDS['better']),
            ("The Perfect Password", SAMPLE_PASSWORDS['strong'])
        ], 1):
            st.markdown(f"#### {stage}️⃣ {desc}")
            st.code(password)
            if st.button(f"Test '{password}'", key=f"test_btn_{stage}"):
                score, feedback = check_password_strength(password)
                st.write(f"Score: {score}/5")
                for item in feedback:
                    st.write(item)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Password Creation Game with improved spacing
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown("## 🎮 Password Creation Game")
    st.write("Try creating passwords following these fun themes and test them in the password checker above:")
    
    st.markdown('<div class="theme-grid">', unsafe_allow_html=True)
    for theme, details in PASSWORD_THEMES.items():
        st.markdown(f"""
            <div class="theme-card">
                <h3>{theme}</h3>
                <p>{details['desc']}</p>
                <p><code>{details['example']}</code></p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Master Challenge with improved spacing
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown("""
        <div class="challenge-section">
            <h2 class="challenge-title">🏆 Ultimate Password Master Challenge</h2>
            <p class="challenge-description">
                Ready to showcase your password mastery? Create the ultimate secure password that combines 
                all the best practices you've learned. Aim for that perfect score and prove you're a true 
                Password Security Master! Remember to include:
                <br><br>
                • Complex character combinations
                <br>
                • Unique patterns and memorable elements
                <br>
                • Proper length and diversity
                <br>
                • No common patterns or sequences
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Master Challenge input with improved styling
    master_password = st.text_input(
        "Create your ultimate password:", 
        type="password",
        key="master_challenge",
        help="Show us your best password creation skills!",
        placeholder="Create your strongest password here"
    )
    
    if master_password:
        score, feedback = check_password_strength(master_password)
        
        # Special handling for perfect scores
        if score == 5:
            st.balloons()
            st.markdown("""
                <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, rgba(46,125,50,0.1), rgba(46,125,50,0.2)); border-radius: 12px; margin: 1rem 0;">
                    <h2 style="color: #2e7d32; margin-bottom: 0.75rem;">🎉 CONGRATULATIONS! 🎉</h2>
                    <p style="font-size: 1.2rem; color: #2e7d32; margin: 0;">
                        You've achieved password perfection! Your masterful creation demonstrates expert-level understanding of password security.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        display_password_strength(score, feedback)
        display_achievement(score)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)  # Close container
    
    # Add footer
    st.markdown('<div class="footer">Designed and created by Tuba Nafees</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 