import streamlit as st
from PIL import Image
import time
import requests
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Aswin | Portfolio",
    page_icon="👨‍💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- THEME TOGGLE ----------------
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

if 'show_all_repos' not in st.session_state:
    st.session_state.show_all_repos = False

# ---------------- CUSTOM CSS WITH ANIMATIONS ----------------
def get_theme_colors():
    if st.session_state.dark_mode:
        return {
            'bg_primary': '#0F172A',
            'bg_secondary': '#1E293B',
            'bg_card': '#1E293B',
            'text_primary': '#F1F5F9',
            'text_secondary': "#94A3B8",
            'accent': '#2ECC71',
            'accent_hover': '#27AE60',
            'border': '#334155',
            'glow': 'rgba(46, 204, 113, 0.3)',
        }
    else:
        return {
            'bg_primary': '#F8FAFC',
            'bg_secondary': '#FFFFFF',
            'bg_card': '#FFFFFF',
            'text_primary': '#0F172A',
            'text_secondary': "#FFFFFF",
            'accent': '#27AE60',
            'accent_hover': '#2ECC71',
            'border': '#E2E8F0',
            'glow': 'rgba(39, 174, 96, 0.2)',
        }

colors = get_theme_colors()

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    /* Main background */
    .stApp {{
        background: {colors['bg_primary']};
        transition: background 0.3s ease;
    }}
    
    .main {{
        padding-top: 0rem;
        color: {colors['text_primary']};
    }}
    
    /* Typography */
    h1 {{
        color: {colors['accent']};
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 1.5rem;
        animation: fadeInUp 0.8s ease-out;
    }}
    
    h2 {{
        color: {colors['accent']};
        font-weight: 600;
        margin: 2.5rem 0 1.5rem 0;
        letter-spacing: -0.01em;
        animation: fadeInUp 0.8s ease-out;
    }}
    
    h3 {{
        color: {colors['text_primary']};
        font-weight: 600;
    }}
    
    p, li {{
        color: {colors['text_secondary']};
        line-height: 1.7;
        font-size: 1rem;
    }}
    
    /* Animations */
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes slideInLeft {{
        from {{
            opacity: 0;
            transform: translateX(-40px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    
    @keyframes glow {{
        0%, 100% {{
            box-shadow: 0 0 20px {colors['glow']};
        }}
        50% {{
            box-shadow: 0 0 30px {colors['glow']}, 0 0 40px {colors['glow']};
        }}
    }}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background: {colors['bg_secondary']};
        border-right: 1px solid {colors['border']};
        animation: slideInLeft 0.6s ease-out;
    }}
    
    [data-testid="stSidebar"] * {{
        color: {colors['text_primary']} !important;
    }}
    
    [data-testid="stSidebar"] .sidebar-content {{
        padding: 2rem 1rem;
    }}
    
    /* Cards with hover effects */
    .card {{
        background: {colors['bg_card']};
        border-radius: 16px;
        padding: 1rem;
        border: 0.5px solid {colors['border']};
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.8s ease-out;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    
    .card:hover {{
        transform: translateY(-8px);
        border-color: {colors['accent']};
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2), 
                    0 0 30px {colors['glow']};
    }}
    
    /* Metric cards */
    [data-testid="stMetricValue"] {{
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: {colors['text_primary']} !important;
    }}
    
    [data-testid="stMetricLabel"] {{
        font-size: 0.875rem !important;
        color: {colors['text_secondary']} !important;
        font-weight: 500 !important;
    }}
    
    [data-testid="stMetricDelta"] {{
        font-size: 0.8rem !important;
    }}
    
    div[data-testid="metric-container"] {{
        background: {colors['bg_card']};
        border: 1px solid {colors['border']};
        padding: 1.5rem;
        border-radius: 12px;
        transition: all 0.3s ease;
        animation: fadeInUp 0.8s ease-out;
    }}
    
    div[data-testid="metric-container"]:hover {{
        transform: translateY(-4px);
        border-color: {colors['accent']};
        box-shadow: 0 10px 20px {colors['glow']};
    }}
    
    /* Project expanders */
    .streamlit-expanderHeader {{
        background: {colors['bg_card']} !important;
        border: 1px solid {colors['border']} !important;
        border-radius: 12px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        padding: 1.25rem !important;
        transition: all 0.3s ease !important;
        color: {colors['text_primary']} !important;
    }}
    
    .streamlit-expanderHeader:hover {{
        background: {colors['bg_secondary']} !important;
        border-color: {colors['accent']} !important;
        transform: translateX(8px);
        box-shadow: 0 4px 12px {colors['glow']};
    }}
    
    .streamlit-expanderContent {{
        background: {colors['bg_card']};
        border: 1px solid {colors['border']};
        border-top: none;
        border-radius: 0 0 12px 12px;
        padding: 1.5rem;
    }}
    
    /* Buttons */
    .stDownloadButton>button {{
        background: linear-gradient(135deg, {colors['accent']} 0%, {colors['accent_hover']} 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(46, 204, 113, 0.3);
    }}
    
    .stDownloadButton>button:hover {{
        background: linear-gradient(135deg, {colors['accent_hover']} 0%, {colors['accent']} 100%);
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(46, 204, 113, 0.4);
    }}
    
    .stDownloadButton>button p {{
        color: white !important;
    }}
    
    .stDownloadButton>button span {{
        color: white !important;
    }}
    
    /* Theme toggle button */
    .theme-toggle {{
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 999;
        background: {colors['bg_card']};
        border: 1px solid {colors['border']};
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}

    /* Hero section */
    .hero {{
        padding: 4rem 0;
        animation: fadeInUp 0.8s ease-out;
    }}
    
    /* Contact form */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {{
        background: {colors['bg_card']} !important;
        border: 1px solid {colors['border']} !important;
        border-radius: 8px !important;
        color: {colors['text_primary']} !important;
        transition: all 0.3s ease !important;
    }}
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {{
        border-color: {colors['accent']} !important;
        box-shadow: 0 0 0 2px {colors['glow']} !important;
    }}
    
   .stButton>button {{
        background: {colors['bg_card']};
        color: white !important;
        border: 2px solid {colors['accent']};
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stButton>button:hover {{
        background: {colors['accent']};
        color: white !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 16px {colors['glow']};
    }}
    
    .stButton>button p {{
        color: white !important;
    }}
    
    .stButton>button span {{
        color: white !important;
    }}
    
    /* Divider */
    hr {{
        border: none;
        height: 1px;
        background: linear-gradient(90deg, 
            transparent, 
            {colors['border']}, 
            transparent);
        margin: 3rem 0;
    }}
    
    /* Scroll reveal */
    .reveal {{
        opacity: 0;
        transform: translateY(30px);
        transition: all 0.8s ease-out;
    }}
    
    .reveal.active {{
        opacity: 1;
        transform: translateY(0);
    }}
    
    /* Links */
    a {{
        color: {colors['accent']} !important;
        text-decoration: none !important;
        transition: all 0.2s ease;
    }}
    
    a:hover {{
        color: {colors['accent_hover']} !important;
        text-shadow: 0 0 8px {colors['glow']};
    }}
    
    /* Info boxes */
    .stAlert {{
        border-radius: 12px;
        border-left: 4px solid {colors['accent']};
        animation: fadeInUp 0.6s ease-out;
    }}
</style>

<script>
// Scroll reveal animation
document.addEventListener('DOMContentLoaded', function() {{
    const reveals = document.querySelectorAll('.reveal');
    
    function checkReveal() {{
        reveals.forEach(element => {{
            const elementTop = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementTop < windowHeight - 100) {{
                element.classList.add('active');
            }}
        }});
    }}
    
    window.addEventListener('scroll', checkReveal);
    checkReveal();
}});
</script>
""", unsafe_allow_html=True)

# ---------------- GITHUB API FUNCTION ----------------

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_github_repos(username="ASWINa1636", max_repos=None):
    """Fetch repositories from GitHub API"""
    try:
        url = f"https://api.github.com/users/{username}/repos"
        params = {
            "sort": "updated",
            "per_page": max_repos if max_repos else 100,  # Get all repos if max_repos is None
            "type": "owner"
        }
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, params=params,headers=headers, timeout=15)
        
        if response.status_code == 200:
            repos = response.json()
            return repos, None
        elif response.status_code == 403:
            return None, "GitHub API rate limit exceeded. Please try again later."
        elif response.status_code == 404:
            return None, "GitHub user not found. Please check the username."
        else:
            return None, f"GitHub API returned status code: {response.status_code}"
            
    except requests.exceptions.Timeout:
        return None, "Request timed out. Please check your internet connection."
    except requests.exceptions.ConnectionError:
        return None, "Connection error. Please check your internet connection."
    except Exception as e:
        return None, f"Error: {str(e)}"


def format_date(date_string):
    """Format GitHub date to readable format"""
    try:
        date_obj = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
        return date_obj.strftime("%b %d, %Y")
    except:
        return date_string


# ---------------- SIDEBAR ----------------
with st.sidebar:
    try:
        img = Image.open("assets/profile.png")
        st.image(img, width=180)
    except:
        st.image("https://via.placeholder.com/180/2ECC71/FFFFFF?text=AA", width=180)
    
    st.title("A Aswin")
    st.markdown("---")
    st.markdown("📍 **Chennai, India**")
    st.markdown("📧 aswinanand1636@gmail.com")
    st.markdown("[🐙 GitHub](https://github.com/ASWINa1636)")
    st.markdown("[💼 LinkedIn](https://linkedin.com/in/aswin-a-954107292/)")
    
    st.markdown("---")
    st.markdown("### 🎯 Quick Links")
    try:
        with open("assets/resume.pdf", "rb") as file:
            st.download_button(
                label="⬇️ Download Resume",
                data=file,
                file_name="Aswin_Resume.pdf",
                mime="application/pdf"
            )
    except:
        st.download_button(
            label="⬇️ Download Resume",
            data="Sample Resume Content",
            file_name="Aswin_Resume.pdf",
            mime="application/pdf"
        )

# ---------------- HERO SECTION ----------------
st.title("👋 Hi, I'm Aswin")
st.markdown("""
<p style='font-size: 1.25rem; line-height: 1.8; margin-bottom: 2rem;'>
I'm an <strong>Electronics & Communication Engineering student</strong> 
with a strong interest in <strong>problem-solving, system design, and practical engineering</strong>. 
I focus on <strong>building real-world solutions</strong> by combining theory with hands-on implementation.
</p>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- STATS SECTION ----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Projects Built", "10+", "Real-world")

with col2:
    st.metric("Core Skills", "5+", "Python, C++")

with col3:
    st.metric("Engineering Focus", "Systems", "Hands-on")

with col4:
    st.metric("GitHub Repos", "11+", "Active")

st.markdown("---")

# ---------------- SKILLS SECTION ----------------
st.header("🛠 Skills & Expertise")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>💻 Programming</h3>
        <ul>
            <li>Python (Advanced)</li>
            <li>C++ (Intermediate)</li>
            <li>SQL (Intermediate)</li>
            <li>Bash Scripting</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


with col2:
    st.markdown("""
    <div class="card">
        <h3>⚙️ Core Domains</h3>
        <ul>
            <li>Backend Systems</li>
            <li>Multithreading</li>
            <li>Embedded Systems</li>
            <li>VLSI Design</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


with col3:
    st.markdown("""
    <div class="card">
        <h3>🔧 Tools & Tech</h3>
        <ul>
            <li>SQLite / PostgreSQL</li>
            <li>Git & GitHub</li>
            <li>Linux / Ubuntu</li>
            <li>Streamlit / Flask</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


st.markdown("---")

#----------- GitHub Auto-Fetched Projects Section------

st.markdown("### 🚀 Latest GitHub Projects")
st.markdown("*Automatically fetched from GitHub*")

# Determine how many repos to show
repos_to_display = 6 if not st.session_state.show_all_repos else None
result = fetch_github_repos(max_repos=repos_to_display)
github_repos = fetch_github_repos(max_repos=repos_to_display)

# Unpack the result
if result:
    github_repos, error_message = result
else:
    github_repos, error_message = None, "Unable to fetch repositories"
   # Display repos in grid with better spacing
if error_message:
    st.warning(f"⚠️ {error_message}")
    st.info("💡 **Tip:** You can manually add your GitHub projects or try refreshing the page.")
elif github_repos and len(github_repos) > 0:
    # Display repos in grid with better spacing
    for i in range(0, len(github_repos), 3):
        cols = st.columns(3)
        for idx, repo in enumerate(github_repos[i:i+3]):
            with cols[idx]:
                st.markdown(f"""
                <div class="card" style="min-height: 320px; display: flex; flex-direction: column; margin-bottom: 2rem;">
                    <h4 style="margin-top: 0; color: {colors['accent']};">
                        📦 {repo['name'][:35]}{'...' if len(repo['name']) > 35 else ''}
                    </h4>
                    <p style="flex-grow: 1; font-size: 0.9rem; margin: 0.5rem 0; line-height: 1.6;">
                        {repo['description'][:120] + '...' if repo['description'] and len(repo['description']) > 120 else repo['description'] or 'No description available'}
                    </p>
                    <div style="margin-top: auto; padding-top: 1rem;">
                        <p style="font-size: 0.85rem; margin: 0.5rem 0; color: {colors['text_secondary']};">
                            <strong style="color: {colors['text_primary']};">Language:</strong> {repo['language'] or 'N/A'}<br>
                            <strong style="color: {colors['text_primary']};">⭐ Stars:</strong> {repo['stargazers_count']} | 
                            <strong style="color: {colors['text_primary']};">🍴 Forks:</strong> {repo['forks_count']}<br>
                            <strong style="color: {colors['text_primary']};">Updated:</strong> {format_date(repo['updated_at'])}
                        </p>
                        <a href="{repo['html_url']}" target="_blank" style="text-decoration: none;">
                            <div style="background: linear-gradient(135deg, {colors['accent']} 0%, {colors['accent_hover']} 100%); 
                                        color: white; padding: 0.75rem; border-radius: 8px; text-align: center; 
                                        margin-top: 1rem; font-weight: 600; transition: all 0.3s ease;">
                                View on GitHub →
                            </div>
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Show More / Show Less Button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if not st.session_state.show_all_repos:
            if st.button("📂 Show All Projects", use_container_width=True, key="show_more"):
                st.session_state.show_all_repos = True
                st.rerun()
        elif st.session_state.show_all_repos:
            if st.button("📁 Show Less", use_container_width=True, key="show_less"):
                st.session_state.show_all_repos = False
                st.rerun()
else:
    st.info("📭 No repositories found or user has no public repositories.")


st.markdown("---")


# ---------------- RESUME SECTION ----------------
st.header("📄 Resume / CV")

col1, = st.columns([1])
with col1:
    st.markdown("""
    <div class="card" style="text-align: center;">
        <p>Download my complete resume with detailed project descriptions and work experience.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,1,1])
with col2:
    try:
        with open("assets/resume.pdf", "rb") as file:
            st.download_button(
                label="⬇️ Download Resume (PDF)",
                data=file,
                file_name="Aswin_Resume.pdf",
                mime="application/pdf"
            )
    except:
        st.download_button(
            label="⬇️ Download Resume (PDF)",
            data="Sample Resume Content",
            file_name="Aswin_Resume.pdf",
            mime="application/pdf"
        )
st.markdown("---")
    
# ---------------- CONTACT SECTION ----------------
st.header("📬 Get In Touch")

st.markdown("""
<div class="card">
    <h3 style="margin-top: 0;">Let's Connect!</h3>
    <p>I'm always open to discussing new projects, creative ideas, or opportunities to be part of your vision.</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3>📧 Email</h3>
        <p><a href="mailto:aswinanand1636@gmail.com">aswinanand1636@gmail.com</a></p>
        <h3>🌐 Social Media</h3>
        <p>
            • <a href="https://www.linkedin.com/in/aswin-a-954107292/" target="_blank">💼 LinkedIn</a><br>
            • <a href="https://github.com/ASWINa1636" target="_blank">🐙 GitHub</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown('<div class="card reveal">', unsafe_allow_html=True)
    st.subheader("💌 Send a Message")
    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Message", height=150)
        submit = st.form_submit_button("Send Message")
        
        if submit:
            if name and email and message:
                st.success("✅ Message sent successfully! I'll get back to you soon.")
                st.balloons()
            else:
                st.error("❌ Please fill in all fields.")
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ---------------- FOOTER ----------------
st.markdown(f"""
<div style='text-align: center'>
    <p style='margin: 0;'>Made with ❤️ using Streamlit | © 2025 A Aswin</p>
    <p style='font-size: 0.9rem; margin: 0.5rem 0 0 0;'>Last updated: January 2025</p>
</div>
""", unsafe_allow_html=True)