import random
import time

import streamlit as st

# --- DELIGHT STYLE: Black + Pink + Gold ---
st.set_page_config(page_title="Delight Play & Win", page_icon="🎮")
st.markdown(
    """
<style>
.stApp { background-color: #000000; color: white; }
.stApp label, .stApp p, .stApp span { color: white; }
h1 { color: #FF69B4 !important; text-align: center; }
h3 { color: #FFD700 !important; text-align: center; }
.stButton>button, .stFormSubmitButton>button {
    background-color: #FF69B4; color: white; font-weight: bold;
    border-radius: 20px; width: 100%; border: none;
}
.scrambled {
    font-size: 32px; letter-spacing: 8px; text-align: center;
    background: #1a1a1a; border: 2px solid #FFD700; padding: 15px;
    border-radius: 15px; color: #FFD700; margin-bottom: 10px;
}
</style>
""",
    unsafe_allow_html=True,
)

# --- WORD POOL (100 words) ---
ALL_WORDS = list(dict.fromkeys([  # dict.fromkeys removes any accidental duplicates
    "LIP", "SOAP", "NAIL", "CREAM", "POWDER", "BLUSH", "GLOSS", "LOTION", "TONER", "SERUM",
    "LIPSTICK", "PERFUME", "MAKEUP", "BRUSHES", "MASCARA", "PRIMER", "CLEANSER", "SHAMPOO", "SPONGE", "MIRROR",
    "FOUNDATION", "CONCEALER", "EYESHADOW", "HIGHLIGHTER", "CONTOURING", "MOISTURIZER", "EXFOLIATOR", "MANICURE", "PEDICURE", "EYELINER",
    "WIG", "HAIR OIL", "EDGE CONTROL", "HAIR SPRAY", "WEAVE", "BRAID", "TWEEZER", "LASHES", "BROW PENCIL", "BODY SCRUB",
    "FACE MASK", "BODY LOTION", "SUNSCREEN", "ROSE WATER", "ALOE VERA", "VITAMIN C", "COLLAGEN", "FACIAL", "PORE", "ACNE CREAM",
    "LIP GLOSS", "LIP LINER", "LIP BALM", "BLUSHER", "COMPACT", "PALETTE", "KABUKI", "BEAUTY BAG", "SETTING SPRAY", "BRONZER",
    "POLISH", "CUTICLE", "NAIL FILE", "HAND CREAM", "FOOT SCRUB", "GEL NAILS", "ACRYLIC", "NAIL ART", "TOP COAT", "BASE COAT",
    "BODY MIST", "BODY SPRAY", "DEODORANT", "BATH SOAP", "SHOWER GEL", "BODY BUTTER", "COCONUT OIL", "SHEA BUTTER", "OLIVE OIL", "ARGAN OIL",
    "HAIR DRYER", "STRAIGHTENER", "CURLING IRON", "HAIR BAND", "CLIP", "COMB", "SCISSORS", "TOWEL", "APRON", "CHAIR",
    "KAJAL", "HENNA", "LIP TINT", "TINT", "GLOW", "SHIMMER", "MATTE", "VELVET", "SILK", "BEAUTY",
]))

TOTAL_WORDS = 30
WIN_SCORE = 15


def normalize(text):
    """Uppercase and remove spaces so 'HAIR OIL' and 'HAIROIL' both match."""
    return "".join(text.upper().split())


def scramble(word):
    letters = list(normalize(word))
    original = "".join(letters)
    # Try a few times to get an arrangement different from the original
    for _ in range(10):
        random.shuffle(letters)
        if "".join(letters) != original:
            break
    return " ".join(letters)


def word_hint(word):
    parts = word.split()
    if len(parts) > 1:
        return f"{len(parts)} words ({' + '.join(str(len(p)) for p in parts)} letters)"
    return f"{len(word)} letters"


def start_game():
    st.session_state.game_words = random.sample(ALL_WORDS, TOTAL_WORDS)
    st.session_state.current = 0
    st.session_state.score = 0
    st.session_state.scrambled = scramble(st.session_state.game_words[0])
    st.session_state.start_time = time.time()
    st.session_state.end_time = None
    st.session_state.feedback = None
    st.session_state.balloons_shown = False


def advance():
    st.session_state.current += 1
    if st.session_state.current < TOTAL_WORDS:
        st.session_state.scrambled = scramble(
            st.session_state.game_words[st.session_state.current]
        )
    else:
        st.session_state.end_time = time.time()


# --- START SCREEN ---
st.markdown("<h1>💄 Delight Cosmetic and Beauty Shop</h1>", unsafe_allow_html=True)
st.markdown("<h3>🎮 Play & Win - Where Elegance Meets Fragrance ✨</h3>", unsafe_allow_html=True)
st.write(
    f"Unscramble {TOTAL_WORDS} words and get at least {WIN_SCORE} right. "
    "Win **10% OFF** on Strawberry Sweet, Jasmine Gold & all perfumes!"
)
st.write("📍 No 6, Balqis Jumoke Street, Fate, Ilorin | 📱 WhatsApp: 09113579070")

# Start a game on first visit (30 random words from the pool)
if "game_words" not in st.session_state:
    start_game()

st.button("🔄 Play New Game - Get New 30 Words", on_click=start_game)

words = st.session_state.game_words
idx = st.session_state.current

if idx < TOTAL_WORDS:
    word = words[idx]

    # Show feedback from the previous action
    fb = st.session_state.feedback
    if fb:
        kind, msg = fb
        if kind == "success":
            st.success(msg)
        elif kind == "error":
            st.error(msg)
        else:
            st.info(msg)

    st.write(f"**Word {idx + 1} of {TOTAL_WORDS} | Score: {st.session_state.score}**")
    st.progress(idx / TOTAL_WORDS)
    st.markdown(
        f'<div class="scrambled">{st.session_state.scrambled}</div>',
        unsafe_allow_html=True,
    )
    st.write(f"Hint: It's a cosmetic / beauty item - {word_hint(word)}.")

    with st.form(key=f"form_{idx}", clear_on_submit=True):
        answer = st.text_input("Type the correct word:")
        col1, col2 = st.columns(2)
        check = col1.form_submit_button("✅ Check")
        skip = col2.form_submit_button("⏭️ Skip")

    if check:
        if normalize(answer) == normalize(word):
            st.session_state.score += 1
            st.session_state.feedback = ("success", "Correct! 🎉")
            advance()
        else:
            st.session_state.feedback = ("error", "Not yet, try again! You can do it 💪")
        st.rerun()
    elif skip:
        st.session_state.feedback = ("info", f"Skipped. The answer was: {word}")
        advance()
        st.rerun()

else:
    # --- GAME FINISHED ---
    score = st.session_state.score
    won = score >= WIN_SCORE

    if won and not st.session_state.balloons_shown:
        st.balloons()
        st.session_state.balloons_shown = True

    st.markdown(
        f"<h1>{'🎉 YOU WIN! 🎉' if won else '🎮 GAME OVER'}</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(f"<h3>Your Score: {score} / {TOTAL_WORDS}</h3>", unsafe_allow_html=True)

    if st.session_state.end_time:
        secs = int(st.session_state.end_time - st.session_state.start_time)
        st.write(f"⏱️ Time taken: {secs // 60}m {secs % 60}s")

    if won:
        st.success("Congratulations! You are a Delight Beauty Queen!")
        st.markdown(
            """
### 🎁 Your Prize Code: **DELIGHT10**
Use it for **10% OFF** on Strawberry Sweet (₦7,500 → ₦6,750) and all perfumes!
"""
        )
        st.link_button(
            "📱 Claim Prize on WhatsApp - 09113579070",
            "https://wa.me/2349113579070?text=Hello%20Delight!%20I%20won%20DELIGHT10%20in%20the%20Word%20Game.%20I%20want%20to%20order.",
        )
    else:
        st.warning(
            f"Good try! You need {WIN_SCORE} correct to win. Play again for new {TOTAL_WORDS} words!"
        )

    st.button("Play Again - New 30 Words", on_click=start_game, key="play_again")
