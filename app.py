import os
from urllib.parse import quote

import streamlit as st
st.markdown("""
<style>
.main { background-color: #FFF8E7; }
h1, h2, h3 { color: #1A1A1A; font-family: Georgia, serif; }
.stButton>button { background-color: #C9A227; color: white; }
</style>
""", unsafe_allow_html=True)
SHOP_NAME = "Delight Cosmetic and Beauty Shop"
WHATSAPP = "2349113579070"

st.set_page_config(page_title=SHOP_NAME, page_icon="💄")


def show_image(path, fallback_text, **kwargs):
    """Show an image if the file exists, otherwise show fallback text."""
    if os.path.exists(path):
        st.image(path, **kwargs)
    else:
        st.write(fallback_text)


# --- LOGO ---
show_image("logo.png", SHOP_NAME, width=200)

st.title(SHOP_NAME)
st.markdown("📱 WhatsApp: 09113579070 | 📍 No 6, Balqis Jumoke Street, Fate, Ilorin")

# --- BANNER ---
show_image(
    "banner.jpg",
    "Welcome to Delight - Our Signature Perfume Collection",
    use_container_width=True,
)

perfumes = [
    ("Oud Royal", 15000, "oud_royal.jpg"),
    ("Floral Blush", 12000, "floral_blush.jpg"),
    ("Clean Fresh", 10000, "clean_fresh.jpg"),
    ("Vanilla Dream", 8000, "vanilla_dream.jpg"),
    ("Mask Classic", 18000, "musk_classic.jpg"),
    ("Strawberry Sweet", 7500, "strawberry_sweet.jpg"),
    ("Leather Bold", 20000, "leather_bold.jpg"),
    ("Jasmine Gold", 16500, "jasmine_gold.jpg"),
    ("Royal Rose", 25000, "royal_rose.jpg"),
]

st.markdown("### Our Signature Perfume Collection")

for name, price, img in perfumes:
    show_image(img, f"Picture coming soon: {name}", use_container_width=True)

    st.write(f"**{name}** - ₦{price:,}")

    message = f"Hello Delight, I want to order {name} for ₦{price:,}"
    st.link_button(
        f"Order {name} on WhatsApp",
        f"https://wa.me/{WHATSAPP}?text={quote(message)}",
    )
    st.markdown("---")

st.markdown("Thank you for shopping with Delight!")
