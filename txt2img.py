#import replicate
import streamlit as st
import requests
import zipfile
import io
from utils import icon
from streamlit_image_select import image_select

# UI configurations
st.set_page_config(page_title="Text to Image Generator by Swayam Swapnila",
                   page_icon=":bridge_at_night:",
                   layout="wide")
icon.show_icon(":foggy:")
st.markdown("# :rainbow[Text-to-Image generator AI]")

# API Tokens and endpoints from `.streamlit/secrets.toml` file
REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]
REPLICATE_MODEL_ENDPOINTSTABILITY = st.secrets["REPLICATE_MODEL_ENDPOINTSTABILITY"]

# Resources text, link, and logo
replicate_text = "Stability AI SDXL Model on Replicate"
replicate_link = "https://replicate.com/stability-ai/sdxl"
replicate_logo = "https://storage.googleapis.com/llama2_release/Screen%20Shot%202023-07-21%20at%2012.34.05%20PM.png"

# Placeholders for images and gallery
generated_images_placeholder = st.empty()
gallery_placeholder = st.empty()

def configure_sidebar():
    with st.sidebar.form(key='sidebar_form'):
        prompt = st.text_input("Enter your prompt")
        negative_prompt = st.text_input("Enter negative prompt", "")
        width = st.slider("Width", min_value=256, max_value=1024, value=512, step=16)
        height = st.slider("Height", min_value=256, max_value=1024, value=512, step=16)
        num_outputs = st.slider("Number of outputs", min_value=1, max_value=5, value=1)
        scheduler = st.selectbox("Scheduler", ["default", "pndm", "ddim", "ddpm"])
        num_inference_steps = st.slider("Inference steps", min_value=1, max_value=100, value=50)
        guidance_scale = st.slider("Guidance scale", min_value=1.0, max_value=20.0, value=7.5)
        prompt_strength = st.slider("Prompt strength", min_value=0.1, max_value=1.0, value=0.8)
        refine = st.selectbox("Refine", ["default", "img2img", "inpaint"])
        high_noise_frac = st.slider("High noise fraction", min_value=0.0, max_value=1.0, value=0.1)
        submitted = st.form_submit_button("Submit")
    return submitted, width, height, num_outputs, scheduler, num_inference_steps, guidance_scale, prompt_strength, refine, high_noise_frac, prompt, negative_prompt

def main_page(submitted, width, height, num_outputs, scheduler, num_inference_steps, guidance_scale, prompt_strength, refine, high_noise_frac, prompt, negative_prompt):
    if submitted:
        with st.spinner('👩🏾‍🍳 Whipping up your words into art...'):
            st.write("⚙️ Model initiated")
            st.write("🙆‍♀️ Stand up and stretch in the meantime")
            try:
                with generated_images_placeholder.container():
                    all_images = []
                    output = replicate.run(
                        REPLICATE_MODEL_ENDPOINTSTABILITY,
                        input={
                            "prompt": prompt,
                            "width": width,
                            "height": height,
                            "num_outputs": num_outputs,
                            "scheduler": scheduler,
                            "num_inference_steps": num_inference_steps,
                            "guidance_scale": guidance_scale,
                            "prompt_strength": prompt_strength,
                            "refine": refine,
                            "high_noise_frac": high_noise_frac
                        }
                    )
                    if output:
                        st.success('Your image has been generated!', icon='😍')
                        st.session_state.generated_image = output
                        for image in st.session_state.generated_image:
                            with st.container():
                                st.image(image, caption="Generated Image 🎈", use_column_width=True)
                                all_images.append(image)
                                response = requests.get(image)
                        st.session_state.all_images = all_images
                        zip_io = io.BytesIO()
                        with zipfile.ZipFile(zip_io, 'w') as zipf:
                            for i, image in enumerate(st.session_state.all_images):
                                response = requests.get(image)
                                if response.status_code == 200:
                                    image_data = response.content
                                    zipf.writestr(f"output_file_{i+1}.png", image_data)
                                else:
                                    st.error(f"Failed to fetch image {i+1} from {image}. Error code: {response.status_code}", icon="🚨")
                        st.download_button(":red[**Download All Images**]", data=zip_io.getvalue(), file_name="output_files.zip", mime="application/zip", use_container_width=True)
            except Exception as e:
                st.error(f'Encountered an error: {e}', icon="🚨")
    else:
        pass
    with gallery_placeholder.container():
        img = image_select(
            label="Like what you see? Right-click and save! It's not stealing if we're sharing! 😉",
            images=[
                "gallery/farmer_sunset.png", "gallery/astro_on_unicorn.png",
                "gallery/friends.png", "gallery/wizard.png", "gallery/puppy.png",
                "gallery/cheetah.png", "gallery/viking.png",
            ],
            captions=["A farmer tilling a farm with a tractor during sunset, cinematic, dramatic",
                      "An astronaut riding a rainbow unicorn, cinematic, dramatic",
                      "A group of friends laughing and dancing at a music festival, joyful atmosphere, 35mm film photography",
                      "A wizard casting a spell, intense magical energy glowing from his hands, extremely detailed fantasy illustration",
                      "A cute puppy playing in a field of flowers, shallow depth of field, Canon photography",
                      "A cheetah mother nurses her cubs in the tall grass of the Serengeti. The early morning sun beams down through the grass. National Geographic photography by Frans Lanting",
                      "A close-up portrait of a bearded viking warrior in a horned helmet. He stares intensely into the distance while holding a battle axe. Dramatic mood lighting, digital oil painting",
                      ],
            use_container_width=True
        )

def main():
    submitted, width, height, num_outputs, scheduler, num_inference_steps, guidance_scale, prompt_strength, refine, high_noise_frac, prompt, negative_prompt = configure_sidebar()
    main_page(submitted, width, height, num_outputs, scheduler, num_inference_steps, guidance_scale, prompt_strength, refine, high_noise_frac, prompt, negative_prompt)
    st.markdown("[Follow me on Twitter](https://x.com/SwapnilaSwayam)")

if __name__ == "__main__":
    main()
