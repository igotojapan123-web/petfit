"""
PetFit - AI-powered Virtual Pet Clothing Fitting Service
Premium Design with Clear User Flow
"""

import streamlit as st
from PIL import Image, ImageDraw, ImageFilter
import io

# Page config
st.set_page_config(
    page_title="PetFit",
    page_icon="🐕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Premium CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * {
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
    }

    html, body, .stApp {
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }

    .stApp {
        background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
    }
    #MainMenu, footer, header { visibility: hidden; }

    /* Main container */
    .main .block-container {
        max-width: 100% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        overflow-x: hidden !important;
    }

    /* Premium Button Styles */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        padding: 12px 28px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        white-space: nowrap;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    }

    /* Step Indicator */
    .step-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0;
        margin: 40px auto;
        max-width: 100%;
        overflow-x: auto;
        padding: 10px 0;
        flex-wrap: wrap;
    }
    .step {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 0 20px;
        min-width: 100px;
    }
    .step-circle {
        width: 56px;
        height: 56px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 12px;
        transition: all 0.3s ease;
        flex-shrink: 0;
    }
    .step-circle.active {
        background: linear-gradient(135deg, #5bb5e0 0%, #3a9fd1 100%);
        color: white;
        box-shadow: 0 8px 24px rgba(91, 181, 224, 0.4);
    }
    .step-circle.inactive {
        background: #e8ecef;
        color: #999;
    }
    .step-circle.completed {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    .step-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #1a1a1a;
        text-align: center;
        white-space: nowrap;
    }
    .step-desc {
        font-size: 0.75rem;
        color: #888;
        margin-top: 4px;
        text-align: center;
        white-space: nowrap;
    }
    .step-line {
        width: 50px;
        height: 3px;
        background: #e8ecef;
        margin-bottom: 30px;
        flex-shrink: 0;
    }
    .step-line.completed {
        background: linear-gradient(90deg, #10b981, #5bb5e0);
    }

    /* Premium Cards */
    .premium-card {
        background: white;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.06);
        border: 1px solid rgba(0,0,0,0.04);
        transition: all 0.3s ease;
        overflow: hidden;
    }
    .premium-card:hover {
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }

    /* Product Cards */
    .product-card {
        background: linear-gradient(180deg, #e8f4fc 0%, #d4ecf7 100%);
        border-radius: 16px;
        padding: 16px;
        min-height: 220px;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 1px solid rgba(91, 181, 224, 0.2);
        position: relative;
        overflow: hidden;
    }
    .product-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(91, 181, 224, 0.25);
    }
    .product-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #5bb5e0, #3a9fd1);
        opacity: 0;
        transition: opacity 0.3s;
    }
    .product-card:hover::before {
        opacity: 1;
    }

    .product-badge {
        display: inline-block;
        background: white;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        color: #1a1a1a;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    /* Fitting Result Cards */
    .fitting-card {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 16px;
        padding: 16px;
        text-align: center;
        border: 1px solid #e8ecef;
        transition: all 0.3s ease;
        overflow: hidden;
    }
    .fitting-card:hover {
        border-color: #5bb5e0;
        box-shadow: 0 8px 24px rgba(91, 181, 224, 0.15);
    }
    .fitting-label {
        font-size: 0.8rem;
        color: #666;
        margin-top: 12px;
        font-weight: 600;
    }

    /* Info Cards */
    .info-card {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        padding: 20px;
        border-radius: 16px;
        border-left: 4px solid #f59e0b;
        overflow: hidden;
    }
    .info-card-title {
        font-weight: 700;
        color: #92400e;
        margin-bottom: 8px;
        font-size: 0.95rem;
    }
    .info-card-desc {
        color: #78716c;
        font-size: 0.85rem;
        line-height: 1.6;
    }

    /* Size Badge */
    .size-badge {
        display: inline-block;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 10px 24px;
        border-radius: 30px;
        font-size: 1.8rem;
        font-weight: 800;
        box-shadow: 0 8px 24px rgba(16, 185, 129, 0.4);
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 40px 20px;
        color: #888;
        border-top: 1px solid #f0f0f0;
        margin-top: 60px;
    }

    /* Flow Arrow */
    .flow-arrow {
        font-size: 2rem;
        color: #5bb5e0;
        margin: 0 16px;
    }

    /* Hero Section Fix */
    .hero-section {
        background: linear-gradient(135deg, #b8dff5 0%, #89c4e8 50%, #5bb5e0 100%);
        padding: 60px 40px;
        margin: 0 -2rem;
        border-radius: 0 0 30px 30px;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .step-container {
            flex-direction: column;
            gap: 16px;
        }
        .step-line {
            width: 3px;
            height: 30px;
            margin: 0;
        }
        .step {
            padding: 8px 0;
        }
        .hero-section {
            padding: 40px 20px;
        }
        .premium-card {
            padding: 16px;
        }
        .product-card {
            min-height: 180px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'pet_info' not in st.session_state:
    st.session_state.pet_info = None
if 'pet_image' not in st.session_state:
    st.session_state.pet_image = None
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None
if 'show_fitting' not in st.session_state:
    st.session_state.show_fitting = False

def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# Size recommendation
def recommend_size(chest_cm):
    chest = float(chest_cm) if chest_cm else 0
    if chest < 30: return "XS", "Chest under 30cm"
    elif chest < 38: return "S", "Chest 30-38cm"
    elif chest < 45: return "M", "Chest 38-45cm"
    elif chest < 55: return "L", "Chest 45-55cm"
    else: return "XL", "Chest over 55cm"

# AI Fitting simulation
def simulate_fitting(pet_image, clothes_color, view="front"):
    if pet_image is None:
        return None
    img = pet_image.copy().convert('RGBA')
    width, height = img.size

    if view == "front":
        alpha, box = 90, (int(width*0.1), int(height*0.2), int(width*0.9), int(height*0.85))
    elif view == "side":
        alpha, box = 80, (int(width*0.15), int(height*0.25), int(width*0.95), int(height*0.8))
    else:
        alpha, box = 85, (int(width*0.05), int(height*0.15), int(width*0.95), int(height*0.9))

    overlay = Image.new('RGBA', img.size, (*clothes_color, alpha))
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse(box, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(20))

    result = Image.composite(Image.blend(img, overlay, 0.4), img, mask)
    return result.convert('RGB')

# Header
def render_header():
    col1, col2, col3 = st.columns([1, 4, 1])

    with col1:
        if st.button("**PetFit**", key="logo", use_container_width=True):
            navigate_to('main')

    with col2:
        nav_cols = st.columns(5)
        with nav_cols[0]:
            st.markdown("<p style='text-align:center; color:#666;'>How it Works</p>", unsafe_allow_html=True)
        with nav_cols[1]:
            st.markdown("<p style='text-align:center; color:#666;'>Features</p>", unsafe_allow_html=True)
        with nav_cols[2]:
            st.markdown("<p style='text-align:center; color:#666;'>Reviews</p>", unsafe_allow_html=True)
        with nav_cols[3]:
            if st.button("Try Demo", key="service_nav_header", use_container_width=True):
                st.session_state.logged_in = True
                navigate_to('service')

    with col3:
        if st.button("Log In", key="login_nav", type="primary"):
            navigate_to('login')

    st.markdown("<hr style='margin:0; border:none; border-top:1px solid #eee;'>", unsafe_allow_html=True)

# Step Indicator Component
def render_step_indicator(current_step):
    steps = [
        {"num": 1, "icon": "📸", "label": "Upload Photo", "desc": "Add your pet's photo"},
        {"num": 2, "icon": "🛍️", "label": "Choose Clothes", "desc": "Browse our collection"},
        {"num": 3, "icon": "✨", "label": "See Result", "desc": "AI virtual fitting"}
    ]

    html = '<div class="step-container">'
    for i, step in enumerate(steps):
        if step["num"] < current_step:
            circle_class = "completed"
            icon = "✓"
        elif step["num"] == current_step:
            circle_class = "active"
            icon = step["icon"]
        else:
            circle_class = "inactive"
            icon = step["icon"]

        html += f'''
        <div class="step">
            <div class="step-circle {circle_class}">{icon}</div>
            <div class="step-label">{step["label"]}</div>
            <div class="step-desc">{step["desc"]}</div>
        </div>
        '''

        if i < len(steps) - 1:
            line_class = "completed" if step["num"] < current_step else ""
            html += f'<div class="step-line {line_class}"></div>'

    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# ============== MAIN PAGE ==============
def render_main_page():
    render_header()

    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div style="max-width: 100%; text-align: center;">
            <p style="color: rgba(255,255,255,0.9); font-size: 0.85rem; font-weight: 600; letter-spacing: 2px; margin-bottom: 16px;">
                AI-POWERED PET FASHION
            </p>
            <h1 style="font-size: 2.5rem; font-weight: 800; color: white; line-height: 1.2; margin-bottom: 20px;">
                Dress Your Pup with Style!
            </h1>
            <p style="color: rgba(255,255,255,0.95); font-size: 1rem; line-height: 1.7; margin-bottom: 24px;">
                See how clothes look on your pet before you buy.<br>
                AI virtual fitting in seconds.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.5, 1.5, 4])
    with col1:
        if st.button("Try Demo Free", key="try_demo", type="primary", use_container_width=True):
            st.session_state.logged_in = True
            navigate_to('service')
    with col2:
        st.button("Watch Video", key="watch_video", use_container_width=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # How It Works Section
    st.markdown("""
    <h2 style="text-align: center; font-size: 2.2rem; font-weight: 800; margin-bottom: 8px;">How It Works</h2>
    <p style="text-align: center; color: #666; margin-bottom: 48px; font-size: 1.1rem;">Try virtual fitting in 3 simple steps</p>
    """, unsafe_allow_html=True)

    # Step cards
    step_cols = st.columns(3)
    steps_data = [
        {"num": "01", "icon": "📸", "title": "Upload Pet Photo", "desc": "Take a photo of your pet or upload from gallery. Works best with front-facing photos."},
        {"num": "02", "icon": "👕", "title": "Choose Clothing", "desc": "Browse our collection and pick the style you like. We have sweaters, jackets, and more."},
        {"num": "03", "icon": "✨", "title": "See AI Fitting", "desc": "Our AI shows how the clothes look on your pet from multiple angles instantly."}
    ]

    for i, step in enumerate(steps_data):
        with step_cols[i]:
            st.markdown(f"""
            <div class="premium-card" style="text-align: center; height: 280px;">
                <p style="font-size: 3rem; font-weight: 800; color: #e8ecef; margin-bottom: 8px;">{step["num"]}</p>
                <p style="font-size: 2.5rem; margin-bottom: 16px;">{step["icon"]}</p>
                <h3 style="font-weight: 700; margin-bottom: 12px;">{step["title"]}</h3>
                <p style="color: #666; font-size: 0.9rem; line-height: 1.6;">{step["desc"]}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # CTA
    col_center = st.columns([2, 1, 2])
    with col_center[1]:
        if st.button("Start Now →", key="start_now", type="primary", use_container_width=True):
            st.session_state.logged_in = True
            navigate_to('service')

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Products Preview
    st.markdown("""
    <h2 style="text-align: center; font-size: 2.2rem; font-weight: 800; margin-bottom: 8px;">Popular Items</h2>
    <p style="text-align: center; color: #666; margin-bottom: 40px;">Trending styles for your furry friend</p>
    """, unsafe_allow_html=True)

    products = [
        {"badge": "Best Seller", "name": "Winter Puffer Vest", "price": "$29"},
        {"badge": "New", "name": "Soft Hoodie", "price": "$24"},
        {"badge": "Limited", "name": "Harness Jacket", "price": "$33"},
    ]

    cols = st.columns(3)
    for i, p in enumerate(products):
        with cols[i]:
            st.markdown(f"""
            <div class="product-card">
                <span class="product-badge">{p["badge"]}</span>
                <div style="height: 160px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 4rem;">👕</span>
                </div>
            </div>
            <p style="font-weight: 700; margin-top: 16px; font-size: 1.1rem;">{p["name"]}</p>
            <p style="font-weight: 800; color: #5bb5e0; font-size: 1.2rem;">{p["price"]}</p>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer">
        <p style="font-size: 1.1rem; font-weight: 600;">© 2026 PetFit</p>
        <p style="margin-top: 8px;">Privacy Policy · Terms of Service · Contact</p>
    </div>
    """, unsafe_allow_html=True)

# ============== SERVICE PAGE ==============
def render_service_page():
    render_header()

    # Title Bar
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
                padding: 20px; border-radius: 16px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
            <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #5bb5e0 0%, #3a9fd1 100%);
                        border-radius: 12px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                <span style="font-size: 1.3rem;">🐕</span>
            </div>
            <div>
                <h2 style="font-weight: 700; font-size: 1.1rem; margin: 0;">PetFit Virtual Fitting</h2>
                <p style="color: #666; font-size: 0.85rem; margin: 0;">Try clothes on your pet with AI</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Pet info display if exists
    if st.session_state.pet_info:
        pet = st.session_state.pet_info
        col_info, col_reset = st.columns([4, 1])
        with col_info:
            st.markdown(f"""
            <div style="background: #f0fdf4; padding: 10px 16px; border-radius: 10px; display: flex; align-items: center; gap: 8px; border: 1px solid #bbf7d0; flex-wrap: wrap;">
                <span style="font-size: 1rem;">🐕</span>
                <span style="font-weight: 600; font-size: 0.9rem;">{pet['name']}</span>
                <span style="color: #666; font-size: 0.85rem;">| {pet['chest']}cm | {pet['weight']}kg</span>
            </div>
            """, unsafe_allow_html=True)
        with col_reset:
            if st.button("Reset", key="reset"):
                st.session_state.pet_info = None
                st.session_state.pet_image = None
                st.session_state.current_step = 1
                st.session_state.show_fitting = False
                st.rerun()

    # Step Indicator
    render_step_indicator(st.session_state.current_step)

    st.markdown("<br>", unsafe_allow_html=True)

    # ===== STEP 1: Upload Photo =====
    if st.session_state.current_step == 1:
        st.markdown("""
        <div class="premium-card">
            <h2 style="font-weight: 700; margin-bottom: 8px;">📸 Step 1: Upload Your Pet's Photo</h2>
            <p style="color: #666; margin-bottom: 28px;">Upload a clear photo of your pet. Front-facing photos work best for accurate fitting.</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Pet Information")
            pet_name = st.text_input("Pet Name", placeholder="e.g. Buddy", key="pet_name")

            col_a, col_b = st.columns(2)
            with col_a:
                weight = st.text_input("Weight (kg)", placeholder="e.g. 4.2", key="pet_weight")
            with col_b:
                chest = st.text_input("Chest (cm)", placeholder="e.g. 40", key="pet_chest")

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Next: Choose Clothes →", key="next_step1", type="primary", use_container_width=True):
                if pet_name and weight and chest:
                    st.session_state.pet_info = {'name': pet_name, 'weight': weight, 'chest': chest}
                    st.session_state.current_step = 2
                    st.rerun()
                else:
                    st.error("Please fill in all fields")

        with col2:
            st.markdown("#### Upload Photo")
            uploaded_file = st.file_uploader("Choose a photo", type=['png', 'jpg', 'jpeg'], key="pet_upload")

            if uploaded_file:
                image = Image.open(uploaded_file)
                st.session_state.pet_image = image
                st.image(image, use_container_width=True)
            elif st.session_state.pet_image:
                st.image(st.session_state.pet_image, use_container_width=True)
            else:
                st.markdown("""
                <div style="background: #f8fafc; border: 2px dashed #d0d7de; border-radius: 16px;
                            padding: 60px 40px; text-align: center;">
                    <p style="font-size: 3rem; margin-bottom: 16px;">📷</p>
                    <p style="color: #666;">Drag & drop or click to upload</p>
                    <p style="color: #999; font-size: 0.85rem;">PNG, JPG up to 10MB</p>
                </div>
                """, unsafe_allow_html=True)

    # ===== STEP 2: Choose Clothes =====
    elif st.session_state.current_step == 2:
        st.markdown("""
        <div class="premium-card">
            <h2 style="font-weight: 700; margin-bottom: 8px;">🛍️ Step 2: Choose Clothing</h2>
            <p style="color: #666; margin-bottom: 8px;">Select a product to see how it looks on your pet</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Products
        products = [
            {"id": 1, "brand": "WarmPaws", "name": "Winter Puffer Vest", "price": 29, "color": (91, 140, 180), "emoji": "🧥"},
            {"id": 2, "brand": "CityWalk", "name": "Soft Hoodie", "price": 24, "color": (91, 140, 180), "emoji": "👕"},
            {"id": 3, "brand": "PupGear", "name": "Harness Jacket", "price": 33, "color": (91, 140, 180), "emoji": "🦺"},
        ]

        cols = st.columns(3)
        for i, p in enumerate(products):
            with cols[i]:
                st.markdown(f"""
                <div class="product-card">
                    <span class="product-badge">{p['brand']}</span>
                    <div style="height: 150px; display: flex; align-items: center; justify-content: center;">
                        <span style="font-size: 4rem;">{p['emoji']}</span>
                    </div>
                </div>
                <p style="font-weight: 700; margin-top: 12px;">{p['name']}</p>
                <p style="font-weight: 700; color: #5bb5e0; font-size: 1.2rem;">${p['price']}</p>
                """, unsafe_allow_html=True)

                if st.button(f"Try This On →", key=f"select_{p['id']}", use_container_width=True, type="primary"):
                    st.session_state.selected_product = p
                    st.session_state.current_step = 3
                    st.session_state.show_fitting = True
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("← Back to Upload", key="back_to_step1"):
            st.session_state.current_step = 1
            st.rerun()

    # ===== STEP 3: See Results =====
    elif st.session_state.current_step == 3:
        product = st.session_state.selected_product

        st.markdown(f"""
        <div class="premium-card">
            <h2 style="font-weight: 700; margin-bottom: 8px;">✨ Step 3: AI Fitting Result</h2>
            <p style="color: #666;">Here's how <strong>{product['name']}</strong> looks on your pet!</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if not st.session_state.pet_image:
            st.warning("⚠️ Please upload your pet's photo first!")
            if st.button("← Back to Upload", key="back_upload"):
                st.session_state.current_step = 1
                st.rerun()
        else:
            # 4 Fitting Results
            result_cols = st.columns(4)
            views = [
                ("Original Photo", None),
                ("AI Fitting — Front", "front"),
                ("AI Fitting — Side", "side"),
                ("AI Fitting — Back", "back")
            ]

            for i, (label, view) in enumerate(views):
                with result_cols[i]:
                    st.markdown("<div class='fitting-card'>", unsafe_allow_html=True)
                    if view is None:
                        st.image(st.session_state.pet_image, use_container_width=True)
                    else:
                        fitted = simulate_fitting(st.session_state.pet_image, product['color'], view)
                        if fitted:
                            st.image(fitted, use_container_width=True)
                    st.markdown(f"<p class='fitting-label'>{label}</p></div>", unsafe_allow_html=True)

            # Size Recommendation
            if st.session_state.pet_info:
                size, reason = recommend_size(st.session_state.pet_info['chest'])
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
                            padding: 30px 20px; border-radius: 16px; margin-top: 24px; text-align: center;
                            border: 1px solid #bbf7d0;">
                    <p style="font-size: 0.9rem; color: #166534; margin-bottom: 12px; font-weight: 600;">📏 Recommended Size for {st.session_state.pet_info['name']}</p>
                    <span class="size-badge">{size}</span>
                    <p style="color: #15803d; margin-top: 12px; font-size: 0.9rem;">{reason}</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                if st.button("🛒 Add to Cart", key="add_cart", type="primary", use_container_width=True):
                    st.session_state.cart.append(product)
                    st.success("🎉 Added to cart!")
                    st.balloons()

            st.markdown("<br>", unsafe_allow_html=True)

            col_x, col_y = st.columns(2)
            with col_x:
                if st.button("← Try Different Clothes", key="try_different"):
                    st.session_state.current_step = 2
                    st.rerun()
            with col_y:
                if st.button("Start Over", key="start_over"):
                    st.session_state.current_step = 1
                    st.session_state.pet_info = None
                    st.session_state.pet_image = None
                    st.session_state.selected_product = None
                    st.rerun()

    # Demo Info
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-weight: 700; margin-bottom: 20px;'>ℹ️ About This Demo</h3>", unsafe_allow_html=True)

    demo_cols = st.columns(3)
    demos = [
        {"icon": "💰", "title": "Free to Use", "desc": "No cost, runs entirely in your browser"},
        {"icon": "🧠", "title": "Smart Sizing", "desc": "AI recommends the perfect size based on measurements"},
        {"icon": "🚀", "title": "Instant Results", "desc": "See fitting results in seconds, no waiting"}
    ]

    for i, d in enumerate(demos):
        with demo_cols[i]:
            st.markdown(f"""
            <div class="info-card">
                <p style="font-size: 2rem; margin-bottom: 8px;">{d["icon"]}</p>
                <p class="info-card-title">{d["title"]}</p>
                <p class="info-card-desc">{d["desc"]}</p>
            </div>
            """, unsafe_allow_html=True)

# ============== LOGIN PAGE ==============
def render_login_page():
    render_header()

    st.markdown("""
    <div class="hero-section" style="text-align: center;">
        <h1 style="font-size: 2.2rem; font-weight: 800; color: white; margin-bottom: 12px;">Welcome to PetFit</h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 1rem;">Virtual fitting for your furry friend</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("""
        <div class="premium-card">
            <h2 style="text-align: center; font-weight: 700; margin-bottom: 8px;">Sign In</h2>
            <p style="text-align: center; color: #666; margin-bottom: 32px;">Welcome back!</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Continue with Google", key="google_login", use_container_width=True):
            st.session_state.logged_in = True
            navigate_to('service')

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Continue with Apple", key="apple_login", use_container_width=True):
            st.session_state.logged_in = True
            navigate_to('service')

        st.markdown("<p style='text-align: center; color: #888; margin: 24px 0;'>— or —</p>", unsafe_allow_html=True)

        email = st.text_input("Email", placeholder="you@example.com", key="email")
        password = st.text_input("Password", type="password", placeholder="••••••••", key="password")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Sign In", key="signin", type="primary", use_container_width=True):
            st.session_state.logged_in = True
            navigate_to('service')

    st.markdown("""
    <div class="footer">
        <p>Privacy Policy · Terms of Service · Contact</p>
    </div>
    """, unsafe_allow_html=True)

# Page routing
if st.session_state.page == 'main':
    render_main_page()
elif st.session_state.page == 'login':
    render_login_page()
elif st.session_state.page == 'service':
    render_service_page()
