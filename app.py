import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="Meme Generator", page_icon="🤣", layout="centered")

st.markdown(
    "<h1 style='text-align: center; color: #FF4B4B;'>🖼️ Meme Generator 😂</h1>",
    unsafe_allow_html=True
)

st.markdown("<p style='text-align: center;'>Upload or capture an image, customize text, and create your meme!</p>", unsafe_allow_html=True)

# ---- FONT FILES ----
font_files = {
    "Impact": "impact.ttf",
    "Arial": "arial.ttf",
    "Comic Sans": "comic.ttf"
}

# ---- Image Input ----
st.markdown("### 📸 Choose an Image Source")
input_option = st.radio("Select image input method:", ["Upload from Device", "Capture from Camera"])

if input_option == "Upload from Device":
    selected_image = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
else:
    selected_image = st.camera_input("Capture an Image")

# ---- Sidebar Controls ----
st.sidebar.header("🎨 Meme Text Settings")

# Top Text
st.sidebar.subheader("🔼 Top Text")
top_text = st.sidebar.text_input("Top Text", "TOP TEXT").upper()
top_font_size = st.sidebar.slider("Top Font Size", 20, 100, 40)
top_font_color = st.sidebar.color_picker("Top Text Color", "#FFFFFF")
top_font_choice = st.sidebar.selectbox("Top Font", list(font_files.keys()))
top_x_offset = st.sidebar.slider("Top Text X", -300, 300, 0)
top_y_offset = st.sidebar.slider("Top Text Y", 0, 300, 10)

# Bottom Text
st.sidebar.subheader("🔽 Bottom Text")
bottom_text = st.sidebar.text_input("Bottom Text", "BOTTOM TEXT").upper()
bottom_font_size = st.sidebar.slider("Bottom Font Size", 20, 100, 40)
bottom_font_color = st.sidebar.color_picker("Bottom Text Color", "#FFFFFF")
bottom_font_choice = st.sidebar.selectbox("Bottom Font", list(font_files.keys()), index=1)
bottom_x_offset = st.sidebar.slider("Bottom Text X", -300, 300, 0)
bottom_y_offset = st.sidebar.slider("Bottom Text Y", 0, 300, 10)

# ---- Draw Text Helper ----
def draw_text(draw, text, x_offset, y, font, font_color, image_width):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (image_width - text_width) / 2 + x_offset
    outline_range = 2

    for dx in range(-outline_range, outline_range + 1):
        for dy in range(-outline_range, outline_range + 1):
            draw.text((x + dx, y + dy), text, font=font, fill="black")

    draw.text((x, y), text, font=font, fill=font_color)

# ---- Generate Meme ----
def generate_meme(image_data):
    image = Image.open(image_data).convert("RGB")
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size

    # Responsive font sizes
    top_scaled_size = int(top_font_size * (image_width / 600))
    bottom_scaled_size = int(bottom_font_size * (image_width / 600))

    # Load fonts safely
    try:
        top_font = ImageFont.truetype(font_files[top_font_choice], top_scaled_size)
    except:
        top_font = ImageFont.truetype("arial.ttf", top_scaled_size)

    try:
        bottom_font = ImageFont.truetype(font_files[bottom_font_choice], bottom_scaled_size)
    except:
        bottom_font = ImageFont.truetype("arial.ttf", bottom_scaled_size)

    # Responsive offset scaling
    tx = int(top_x_offset * (image_width / 600))
    ty = int(top_y_offset * (image_height / 600))
    bx = int(bottom_x_offset * (image_width / 600))
    by = int(bottom_y_offset * (image_height / 600))

    draw_text(draw, top_text, tx, ty, top_font, top_font_color, image_width)
    draw_text(draw, bottom_text, bx, image_height - bottom_scaled_size - by, bottom_font, bottom_font_color, image_width)

    return image

# ---- Display Result ----
if selected_image:
    meme_image = generate_meme(selected_image)
    st.image(meme_image, caption="Your Meme", use_container_width=True)

    buf = io.BytesIO()
    meme_image.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button("📥 Download Meme", byte_im, file_name="custom_meme.png", mime="image/png")
else:
    st.info("Please upload or capture an image to start.")

st.markdown("<hr>", unsafe_allow_html=True)
