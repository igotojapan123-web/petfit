"""
PetFit - AI-powered Virtual Pet Clothing Fitting Service
"""

import streamlit as st
from PIL import Image, ImageDraw, ImageFilter
import io

# 페이지 설정
st.set_page_config(
    page_title="PetFit",
    page_icon="🐕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일 (Figma 디자인 그대로)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    * { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #ffffff; }
    #MainMenu, footer, header { visibility: hidden; }

    /* 버튼 기본 스타일 */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        padding: 12px 24px;
        transition: all 0.2s;
    }

    /* 상품 카드 */
    .product-card {
        background: linear-gradient(180deg, #d4ecf7 0%, #b8dff5 100%);
        border-radius: 12px;
        padding: 16px;
        height: 260px;
        cursor: pointer;
        transition: transform 0.2s;
        border: 1px solid #cce5f0;
    }
    .product-card:hover { transform: translateY(-4px); }

    .product-badge {
        display: inline-block;
        background: white;
        padding: 4px 12px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    /* 리뷰 카드 */
    .review-card {
        background: #1a1a1a;
        border-radius: 12px;
        padding: 16px;
        color: white;
    }

    /* 데모 카드 */
    .demo-card {
        background: #fef3c7;
        padding: 20px;
        border-radius: 12px;
    }
    .demo-card-title {
        font-weight: 700;
        color: #92400e;
        margin-bottom: 8px;
    }
    .demo-card-desc {
        color: #78716c;
        font-size: 0.85rem;
    }

    /* 피팅 결과 카드 */
    .fitting-card {
        background: #f8fafc;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .fitting-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 16px;
        font-weight: 500;
    }

    /* 소셜 버튼 */
    .social-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        padding: 14px 24px;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        background: white;
        cursor: pointer;
        width: 100%;
        margin-bottom: 12px;
        font-weight: 500;
    }
    .social-btn:hover {
        background: #f8fafc;
    }

    /* 입력 필드 라벨 */
    .input-label {
        font-size: 0.85rem;
        font-weight: 500;
        color: #1a1a1a;
        margin-bottom: 6px;
        display: block;
    }

    /* 푸터 */
    .footer {
        text-align: center;
        padding: 40px 20px;
        color: #666;
        border-top: 1px solid #f0f0f0;
        margin-top: 60px;
    }
    .footer-links {
        display: flex;
        justify-content: center;
        gap: 40px;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
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
if 'service_tab' not in st.session_state:
    st.session_state.service_tab = 'register'
if 'show_fitting' not in st.session_state:
    st.session_state.show_fitting = False
if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None

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

# AI 피팅 시뮬레이션
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

# 헤더
def render_header():
    col1, col2, col3 = st.columns([1, 4, 1])

    with col1:
        if st.button("**PetFit**", key="logo", use_container_width=True):
            navigate_to('main')

    with col2:
        nav_cols = st.columns(5)
        with nav_cols[0]:
            st.markdown("<p style='text-align:center; color:#666;'>How it Work</p>", unsafe_allow_html=True)
        with nav_cols[1]:
            st.markdown("<p style='text-align:center; color:#666;'>Why Choose Us</p>", unsafe_allow_html=True)
        with nav_cols[2]:
            st.markdown("<p style='text-align:center; color:#666;'>Testimonial</p>", unsafe_allow_html=True)
        with nav_cols[3]:
            if st.button("Service", key="service_nav_header", use_container_width=True):
                st.session_state.logged_in = True
                navigate_to('service')

    with col3:
        if st.button("Log In", key="login_nav", type="primary"):
            navigate_to('login')

    st.markdown("<hr style='margin:0; border:none; border-top:1px solid #eee;'>", unsafe_allow_html=True)

# ============== 메인 페이지 ==============
def render_main_page():
    render_header()

    # 히어로 섹션
    st.markdown("""
    <div style="background: linear-gradient(135deg, #b8dff5 0%, #a8d4f0 100%); padding: 80px 60px; margin: -1rem -1rem 0 -1rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto;">
            <div style="max-width: 450px;">
                <h1 style="font-size: 2.8rem; font-weight: 700; color: white; line-height: 1.2; margin-bottom: 20px;">
                    Dress Your Pup with Style!
                </h1>
                <p style="color: rgba(255,255,255,0.9); font-size: 1.05rem; line-height: 1.6; margin-bottom: 28px;">
                    Discover the latest in dog fashion with our AI-powered virtual fitting service.
                </p>
            </div>
            <div style="width: 320px; height: 280px; background: white; border-radius: 12px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 버튼
    col1, col2, col3 = st.columns([1.2, 1.2, 4])
    with col1:
        if st.button("Shop Now", key="shop_now", use_container_width=True):
            navigate_to('register')
    with col2:
        if st.button("Get Started", key="get_started", type="primary", use_container_width=True):
            navigate_to('register')

    # 태그
    st.markdown("""
    <div style="display: flex; gap: 10px; margin: 20px 0 50px 0;">
        <span style="background: #5bb5e0; color: white; padding: 8px 22px; border-radius: 20px; font-size: 0.9rem; font-weight: 500;">Trendy</span>
        <span style="background: #5bb5e0; color: white; padding: 8px 22px; border-radius: 20px; font-size: 0.9rem; font-weight: 500;">Classic</span>
        <span style="background: #5bb5e0; color: white; padding: 8px 22px; border-radius: 20px; font-size: 0.9rem; font-weight: 500;">Seasonal</span>
    </div>
    """, unsafe_allow_html=True)

    # New Arrivals
    st.markdown("""
    <h2 style="text-align: center; font-size: 2rem; font-weight: 700; margin-bottom: 8px;">New Arrivals</h2>
    <p style="text-align: center; color: #666; margin-bottom: 24px;">Browse the latest styles for your furry friend.</p>
    """, unsafe_allow_html=True)

    col_center = st.columns([2, 1, 2])
    with col_center[1]:
        if st.button("View All", key="view_all", type="primary", use_container_width=True):
            navigate_to('register')

    st.markdown("<br>", unsafe_allow_html=True)

    # 상품 카드
    products = [
        {"badge": "New", "desc": "Cute red sweater", "name": "Cozy Dog Red Sweater", "sizes": "S, M, L"},
        {"badge": "Best Seller", "desc": "Stylish raincoat", "name": "Trendy Dog Raincoat", "sizes": "M, L, XL"},
        {"badge": "Limited Edition", "desc": "Comfortable denim jacket", "name": "Denim Dog Jacket", "sizes": "S, M"},
    ]

    cols = st.columns(3)
    for i, p in enumerate(products):
        with cols[i]:
            st.markdown(f"""
            <div class="product-card">
                <span class="product-badge">{p['badge']}</span>
                <div style="height: 180px; display: flex; align-items: center; justify-content: center; color: #888;">
                    {p['desc']}
                </div>
            </div>
            <p style="font-weight: 700; margin-top: 12px;">{p['name']}</p>
            <p style="color: #666; font-size: 0.9rem;">Sizes: {p['sizes']}</p>
            """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # What Our Customers Say
    st.markdown("""
    <div style="background: #f8fafc; padding: 50px 40px; margin: 0 -1rem;">
        <div style="display: flex; gap: 60px; max-width: 1100px; margin: 0 auto;">
            <div style="flex: 1;">
                <h2 style="font-size: 2rem; font-weight: 700; margin-bottom: 12px;">What Our Customers Say</h2>
                <p style="color: #666;">Hear from happy dog parents who love our products!</p>
            </div>
            <div style="flex: 1.5; display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                <div class="review-card">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                        <div style="width: 32px; height: 32px; background: #5bb5e0; border-radius: 50%;"></div>
                        <span style="font-weight: 600;">Alice</span>
                        <span style="color: #fbbf24;">★★★★★</span>
                    </div>
                    <p style="color: #ccc; font-size: 0.85rem;">The red sweater fits perfect...</p>
                </div>
                <div class="review-card">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                        <div style="width: 32px; height: 32px; background: #5bb5e0; border-radius: 50%;"></div>
                        <span style="font-weight: 600;">Bob</span>
                        <span style="color: #fbbf24;">★★★★★</span>
                    </div>
                    <p style="color: #ccc; font-size: 0.85rem;">Excellent quality and a perf...</p>
                </div>
                <div class="review-card" style="grid-column: span 2;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                        <div style="width: 32px; height: 32px; background: #5bb5e0; border-radius: 50%;"></div>
                        <span style="font-weight: 600;">Charlie</span>
                        <span style="color: #fbbf24;">★★★★★</span>
                    </div>
                    <p style="color: #ccc; font-size: 0.85rem;">The raincoat is not only styli...</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Why Choose PetFit
    st.markdown("""
    <h2 style="text-align: center; font-size: 2rem; font-weight: 700; margin-bottom: 8px;">Why Choose PetFit?</h2>
    <p style="text-align: center; color: #666; margin-bottom: 28px;">Our AI technology ensures the perfect fit for your furry friend.</p>
    """, unsafe_allow_html=True)

    col_center = st.columns([2, 1, 2])
    with col_center[1]:
        st.button("Learn More", key="learn_more", type="primary", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    feature_cols = st.columns(2)
    with feature_cols[0]:
        st.markdown("""
        <div style="background: white; border: 1px solid #e0e0e0; border-radius: 12px; padding: 24px; display: flex; gap: 16px;">
            <div style="width: 60px; height: 60px; background: #f0f0f0; border-radius: 8px;"></div>
            <div>
                <p style="font-weight: 700; margin-bottom: 4px;">Virtual Fitting</p>
                <p style="color: #666; font-size: 0.85rem;">Use your dog's measurements to find the perfect fit without the hassle.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with feature_cols[1]:
        st.markdown("""
        <div style="background: white; border: 1px solid #e0e0e0; border-radius: 12px; padding: 24px; display: flex; gap: 16px;">
            <div style="width: 60px; height: 60px; background: #f0f0f0; border-radius: 8px;"></div>
            <div>
                <p style="font-weight: 700; margin-bottom: 4px;">Stylish Collection</p>
                <p style="color: #666; font-size: 0.85rem;">We offer a wide variety of trendy and fashionable dog clothing.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Follow Us on Social Media
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: #f8fafc; padding: 50px 40px; margin: 0 -1rem;">
        <h2 style="text-align: center; font-size: 2rem; font-weight: 700; margin-bottom: 8px;">Follow Us on Social Media</h2>
        <p style="text-align: center; color: #666; margin-bottom: 32px;">Join our community and share your pet's style!</p>
        <div style="max-width: 500px; margin: 0 auto;">
            <div style="background: white; border-radius: 12px; padding: 16px; margin-bottom: 16px; border: 1px solid #eee;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                    <div style="width: 32px; height: 32px; background: #5bb5e0; border-radius: 50%;"></div>
                    <span style="font-weight: 600;">PetLover99</span>
                    <span style="margin-left: auto;">•••</span>
                </div>
                <div style="background: #b8dff5; height: 200px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #666;">
                    Dog wearing stylish clothes
                </div>
                <p style="margin-top: 12px; font-size: 0.9rem;">Loving the new outfits from PetFit! #DogFashion</p>
                <p style="color: #5bb5e0; font-size: 0.85rem;">#Stylish #HappyDog</p>
            </div>
            <div style="background: white; border-radius: 12px; padding: 16px; border: 1px solid #eee;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                    <div style="width: 32px; height: 32px; background: #5bb5e0; border-radius: 50%;"></div>
                    <span style="font-weight: 600;">PawPrints</span>
                    <span style="margin-left: auto;">•••</span>
                </div>
                <div style="background: #b8dff5; height: 200px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #666;">
                    Cute puppy modeling a coat
                </div>
                <p style="margin-top: 12px; font-size: 0.9rem;">This coat is perfect for rainy day walks! #PetFit</p>
                <p style="color: #5bb5e0; font-size: 0.85rem;">#RainyDay #ReadyToWalk</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 푸터
    st.markdown("""
    <div class="footer">
        <p>© 2026 PetFit</p>
        <div class="footer-links">
            <span>Privacy Policy</span>
            <span>Terms of Service</span>
            <span>Contact Us</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============== 회원가입 페이지 ==============
def render_register_page():
    render_header()

    # 파란 배너
    st.markdown("""
    <div style="background: linear-gradient(135deg, #b8dff5 0%, #a8d4f0 100%); padding: 70px 40px; text-align: center; margin: -1rem -1rem 0 -1rem;">
        <h1 style="font-size: 2.2rem; font-weight: 700; color: white; margin-bottom: 8px;">Start Dressing Your Pet Today</h1>
        <p style="color: rgba(255,255,255,0.9);">Millions of fitcheck for your pet</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    # 회원가입 폼
    col1, col2, col3 = st.columns([1, 1.5, 1])

    with col2:
        st.markdown("""
        <h2 style="text-align: center; font-size: 1.6rem; font-weight: 700; margin-bottom: 8px;">Let's get in</h2>
        <p style="text-align: center; color: #666; margin-bottom: 32px;">We Are Happy To Help With Your Learning Journey, Lets Dive in By Registering.</p>
        """, unsafe_allow_html=True)

        if st.button("Continue with Google", key="google_reg", use_container_width=True):
            st.session_state.logged_in = True
            navigate_to('service')

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Continue with Apple", key="apple_reg", use_container_width=True):
            st.session_state.logged_in = True
            navigate_to('service')

        st.markdown("<p style='text-align: center; color: #888; margin: 24px 0;'>( Or )</p>", unsafe_allow_html=True)

        if st.button("Sign In With your Account", key="signin_account", use_container_width=True):
            navigate_to('login')

        st.markdown("""
        <p style="text-align: center; color: #666; margin-top: 24px;">
            Don't have an Account? <span style="text-decoration: underline; font-weight: 600; cursor: pointer;">SIGN UP</span>
        </p>
        """, unsafe_allow_html=True)

    # 푸터
    st.markdown("""
    <div class="footer">
        <div class="footer-links">
            <span>Privacy Policy</span>
            <span>Terms of Service</span>
            <span>Contact Us</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============== 로그인 페이지 ==============
def render_login_page():
    render_header()

    # 파란 배너
    st.markdown("""
    <div style="background: linear-gradient(135deg, #b8dff5 0%, #a8d4f0 100%); padding: 70px 40px; text-align: center; margin: -1rem -1rem 0 -1rem;">
        <h1 style="font-size: 2.2rem; font-weight: 700; color: white; margin-bottom: 8px;">Start Dressing Your Pet Today</h1>
        <p style="color: rgba(255,255,255,0.9);">Millions of fitcheck for your pet</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])

    with col2:
        st.markdown("""
        <h2 style="text-align: center; font-size: 1.6rem; font-weight: 700; margin-bottom: 8px;">Hello Again!</h2>
        <p style="text-align: center; color: #666; margin-bottom: 32px;">Welcome Back You've Been Missed!</p>
        """, unsafe_allow_html=True)

        st.markdown("<span class='input-label'>Email Address</span>", unsafe_allow_html=True)
        email = st.text_input("email", placeholder="fastcampusai@gmail.com", key="login_email", label_visibility="collapsed")

        st.markdown("<span class='input-label'>Password</span>", unsafe_allow_html=True)
        password = st.text_input("password", type="password", placeholder="••••••••", key="login_password", label_visibility="collapsed")

        st.markdown("<p style='text-align: right; color: #5bb5e0; font-size: 0.9rem; cursor: pointer;'>Recovery Password</p>", unsafe_allow_html=True)

        if st.button("Sign In", key="signin_btn", type="primary", use_container_width=True):
            st.session_state.logged_in = True
            navigate_to('service')

        st.markdown("<p style='text-align: center; color: #888; margin: 24px 0;'>( Or Continue With )</p>", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Google", key="google_login", use_container_width=True):
                st.session_state.logged_in = True
                navigate_to('service')
        with col_b:
            if st.button("Apple", key="apple_login", use_container_width=True):
                st.session_state.logged_in = True
                navigate_to('service')

        st.markdown("""
        <p style="text-align: center; color: #666; margin-top: 24px;">
            Don't have an Account? <span style="text-decoration: underline; font-weight: 600;">SIGN UP</span>
        </p>
        """, unsafe_allow_html=True)

    # 푸터
    st.markdown("""
    <div class="footer">
        <div class="footer-links">
            <span>Privacy Policy</span>
            <span>Terms of Service</span>
            <span>Contact Us</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============== 서비스 페이지 ==============
def render_service_page():
    render_header()

    # Top info bar
    st.markdown("""
    <div style="background: #f8fafc; padding: 20px 28px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #b8dff5 0%, #5bb5e0 100%); border-radius: 50%;"></div>
            <div>
                <p style="font-weight: 700; font-size: 1.1rem; margin: 0;">PetFit Demo</p>
                <p style="color: #888; font-size: 0.85rem; margin: 0;">Free demo · Runs in browser</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Pet info + Reset button
    if st.session_state.pet_info:
        pet = st.session_state.pet_info
        col_info, col_reset = st.columns([4, 1])
        with col_info:
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">
                <span style="width: 8px; height: 8px; background: #5bb5e0; border-radius: 50%; display: inline-block;"></span>
                <span style="font-weight: 600;">{pet['name']}</span>
                <span style="color: #888;">Chest {pet['chest']}cm · Weight {pet['weight']}kg</span>
            </div>
            """, unsafe_allow_html=True)
        with col_reset:
            if st.button("Reset", key="reset"):
                st.session_state.pet_info = None
                st.session_state.pet_image = None
                st.rerun()

    # Tabs
    tab_cols = st.columns([1, 1, 5, 1])
    with tab_cols[0]:
        if st.button("Register", key="tab_register", type="primary" if st.session_state.service_tab == 'register' else "secondary", use_container_width=True):
            st.session_state.service_tab = 'register'
            st.session_state.show_fitting = False
            st.rerun()
    with tab_cols[1]:
        if st.button("Shop", key="tab_shopping", type="primary" if st.session_state.service_tab == 'shopping' else "secondary", use_container_width=True):
            st.session_state.service_tab = 'shopping'
            st.rerun()
    with tab_cols[3]:
        st.markdown(f"<div style='background: white; border: 1px solid #1a1a1a; padding: 8px 16px; border-radius: 8px; font-weight: 600; text-align: center;'>Cart {len(st.session_state.cart)}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ===== Register Tab =====
    if st.session_state.service_tab == 'register':
        st.markdown("""
        <div style="background: #f8fafc; padding: 28px 32px; border-radius: 16px;">
            <h2 style="font-weight: 700; margin-bottom: 8px;">Register Your Pet</h2>
            <p style="color: #666; margin-bottom: 28px;">Enter your pet's photo and measurements. When you click a product, auto size recommendation and fitting demo will work.</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            pet_name = st.text_input("Pet Name", placeholder="Buddy", key="pet_name", value=st.session_state.pet_info['name'] if st.session_state.pet_info else "")
            weight = st.text_input("Weight (kg)", placeholder="4.2", key="pet_weight", value=st.session_state.pet_info['weight'] if st.session_state.pet_info else "")
            chest = st.text_input("Chest (cm)", placeholder="40", key="pet_chest", value=st.session_state.pet_info['chest'] if st.session_state.pet_info else "")

            if st.button("Save & Start Shopping", key="save_pet", type="primary"):
                if pet_name and weight and chest:
                    st.session_state.pet_info = {'name': pet_name, 'weight': weight, 'chest': chest}
                    st.session_state.service_tab = 'shopping'
                    st.rerun()
                else:
                    st.error("Please fill in all fields!")

        with col2:
            st.markdown("**Upload Pet Photo**")
            uploaded_file = st.file_uploader("Choose file", type=['png', 'jpg', 'jpeg'], key="pet_upload")

            if uploaded_file:
                image = Image.open(uploaded_file)
                st.session_state.pet_image = image
                st.image(image, use_container_width=True)
            elif st.session_state.pet_image:
                st.image(st.session_state.pet_image, use_container_width=True)

        # Demo points
        st.markdown("""
        <div style="background: #fef3c7; padding: 20px 24px; border-radius: 12px; margin-top: 24px;">
            <p style="font-weight: 700; color: #92400e; margin-bottom: 12px;">Demo Features</p>
            <ul style="margin: 0; padding-left: 20px; color: #78716c;">
                <li>Recommendations are rule-based (explainable)</li>
                <li>Fitting works with canvas overlay (no server/cost)</li>
                <li>Can be upgraded to AI warping/generation models</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # ===== Shop Tab =====
    elif st.session_state.service_tab == 'shopping':
        st.markdown("""
        <div style="background: #f8fafc; padding: 28px 32px; border-radius: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h2 style="font-weight: 700; margin-bottom: 8px;">Shop</h2>
                    <p style="color: #666;">Click a product to see auto size recommendation and virtual fitting demo.</p>
                </div>
                <span style="font-weight: 600;">Cart {len(st.session_state.cart)} items</span>
            </div>
        </div>
        """.format(len=len), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Products
        products = [
            {"id": 1, "brand": "WarmPaws", "name": "Winter Puffer Vest", "price": 29, "sizes": "S/M/L/XL", "color": (91, 140, 180)},
            {"id": 2, "brand": "CityWalk", "name": "Soft Hoodie", "price": 24, "sizes": "S/M/L/XL", "color": (91, 140, 180)},
            {"id": 3, "brand": "PupGear", "name": "Harness Jacket", "price": 33, "sizes": "S/M/L/XL", "color": (91, 140, 180)},
        ]

        cols = st.columns(3)
        for i, p in enumerate(products):
            with cols[i]:
                st.markdown(f"""
                <div class="product-card">
                    <span class="product-badge">{p['brand']}</span>
                    <div style="height: 180px;"></div>
                </div>
                <p style="font-weight: 700; margin-top: 12px;">{p['name']}</p>
                <p style="font-weight: 700;">${p['price']}</p>
                <p style="color: #666; font-size: 0.85rem;">Sizes: {p['sizes']}</p>
                """, unsafe_allow_html=True)

                if st.button(f"🎨 Try Fitting", key=f"fit_{p['id']}", use_container_width=True):
                    st.session_state.selected_product = p
                    st.session_state.show_fitting = True
                    st.rerun()

        # AI Fitting Results
        if st.session_state.show_fitting and st.session_state.selected_product:
            product = st.session_state.selected_product

            st.markdown("<hr style='margin: 40px 0;'>", unsafe_allow_html=True)
            st.markdown(f"""
            <h3 style="font-weight: 700; margin-bottom: 24px;">🎨 AI Virtual Fitting — {product['name']}</h3>
            """, unsafe_allow_html=True)

            if not st.session_state.pet_image:
                st.warning("⚠️ Please upload your pet's photo in the 'Register' tab first!")
            else:
                # 4 images (Original + Front + Side + Back)
                result_cols = st.columns(4)

                with result_cols[0]:
                    st.markdown("<div class='fitting-card'>", unsafe_allow_html=True)
                    st.image(st.session_state.pet_image, use_container_width=True)
                    st.markdown("<p class='fitting-label'>Original Photo</p></div>", unsafe_allow_html=True)

                with result_cols[1]:
                    st.markdown("<div class='fitting-card'>", unsafe_allow_html=True)
                    front = simulate_fitting(st.session_state.pet_image, product['color'], "front")
                    if front:
                        st.image(front, use_container_width=True)
                    st.markdown("<p class='fitting-label'>AI Fitting — Front</p></div>", unsafe_allow_html=True)

                with result_cols[2]:
                    st.markdown("<div class='fitting-card'>", unsafe_allow_html=True)
                    side = simulate_fitting(st.session_state.pet_image, product['color'], "side")
                    if side:
                        st.image(side, use_container_width=True)
                    st.markdown("<p class='fitting-label'>AI Fitting — Side</p></div>", unsafe_allow_html=True)

                with result_cols[3]:
                    st.markdown("<div class='fitting-card'>", unsafe_allow_html=True)
                    back = simulate_fitting(st.session_state.pet_image, product['color'], "back")
                    if back:
                        st.image(back, use_container_width=True)
                    st.markdown("<p class='fitting-label'>AI Fitting — Back</p></div>", unsafe_allow_html=True)

                # Size recommendation
                if st.session_state.pet_info:
                    size, reason = recommend_size(st.session_state.pet_info['chest'])
                    st.markdown(f"""
                    <div style="background: #f0fdf4; padding: 28px; border-radius: 12px; margin-top: 32px; text-align: center; border: 1px solid #bbf7d0;">
                        <h4 style="color: #166534; margin-bottom: 8px;">📏 Recommended Size</h4>
                        <p style="font-size: 3rem; font-weight: 800; color: #10b981; margin: 20px 0;">{size}</p>
                        <p style="color: #15803d;">{reason}</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                col_a, col_b, col_c = st.columns([1, 2, 1])
                with col_b:
                    if st.button("🛒 Add to Cart", key="add_cart", type="primary", use_container_width=True):
                        st.session_state.cart.append(product)
                        st.success("🎉 Added to cart!")
                        st.balloons()

    # Demo Features
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-weight: 700; margin-bottom: 16px;'>Demo Features</h3>", unsafe_allow_html=True)

    demo_cols = st.columns(3)
    with demo_cols[0]:
        st.markdown("""
        <div class="demo-card">
            <p class="demo-card-title">Free to Run</p>
            <p class="demo-card-desc">Runs in browser without server. Image compositing is done locally.</p>
        </div>
        """, unsafe_allow_html=True)
    with demo_cols[1]:
        st.markdown("""
        <div class="demo-card">
            <p class="demo-card-title">Explainable AI</p>
            <p class="demo-card-desc">Size recommendation based on chest measurement with clear reasoning.</p>
        </div>
        """, unsafe_allow_html=True)
    with demo_cols[2]:
        st.markdown("""
        <div class="demo-card">
            <p class="demo-card-title">Scalable</p>
            <p class="demo-card-desc">Can be upgraded to warping/segmentation/generation models for better quality.</p>
        </div>
        """, unsafe_allow_html=True)

# 페이지 라우팅
if st.session_state.page == 'main':
    render_main_page()
elif st.session_state.page == 'register':
    render_register_page()
elif st.session_state.page == 'login':
    render_login_page()
elif st.session_state.page == 'service':
    render_service_page()
