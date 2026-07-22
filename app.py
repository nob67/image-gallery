import gradio as gr
import os
from pathlib import Path
from PIL import Image
import json
from datetime import datetime

# Configuration
UPLOAD_DIR = "images/uploads"
GALLERY_DIR = "images/gallery"
METADATA_FILE = "images/metadata.json"

# Create directories if they don't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(GALLERY_DIR, exist_ok=True)

def load_metadata():
    """Load metadata from JSON file"""
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_metadata(metadata):
    """Save metadata to JSON file"""
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=2)

def get_gallery_images():
    """Get all images from gallery directory"""
    images = []
    if not os.path.exists(GALLERY_DIR):
        return images
    
    for file in sorted(os.listdir(GALLERY_DIR)):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            filepath = os.path.join(GALLERY_DIR, file)
            images.append(filepath)
    return images

def upload_image(file):
    """Handle image upload"""
    if file is None:
        return "No file uploaded", get_gallery_images()
    
    try:
        # Get filename
        if hasattr(file, 'name'):
            filename = os.path.basename(file.name)
            file_path = file.name
        else:
            filename = os.path.basename(str(file))
            file_path = str(file)
        
        save_path = os.path.join(GALLERY_DIR, filename)
        
        # Use PIL to verify it's a valid image
        img = Image.open(file_path)
        img.save(save_path)
        
        # Update metadata
        metadata = load_metadata()
        metadata[filename] = {
            "uploaded": datetime.now().isoformat(),
            "size": f"{img.width}x{img.height}",
            "format": img.format
        }
        save_metadata(metadata)
        
        return f"✅ Image '{filename}' uploaded successfully!", get_gallery_images()
    except Exception as e:
        return f"❌ Error uploading image: {str(e)}", get_gallery_images()

def delete_image(gallery_state):
    """Delete image from gallery - requires Gradio 6.20+ select callback"""
    if not gallery_state:
        return "No image selected", get_gallery_images()
    
    try:
        # Handle different gallery return formats
        image_path = gallery_state
        if isinstance(gallery_state, dict):
            image_path = gallery_state.get('name') or gallery_state.get('image')
        
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
            
            # Update metadata
            filename = os.path.basename(image_path)
            metadata = load_metadata()
            if filename in metadata:
                del metadata[filename]
            save_metadata(metadata)
            
            return f"✅ Image deleted!", get_gallery_images()
        else:
            return "❌ Image not found", get_gallery_images()
    except Exception as e:
        return f"❌ Error: {str(e)}", get_gallery_images()

def search_images(query):
    """Search images by filename"""
    all_images = get_gallery_images()
    if not query:
        return all_images
    
    query = query.lower()
    return [img for img in all_images if query in os.path.basename(img).lower()]

# Create Gradio interface
with gr.Blocks(title="Image Gallery", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🖼️ Image Gallery")
    gr.Markdown("A simple image gallery built with Gradio. Upload, organize, and view your images.")
    
    with gr.Tabs():
        # Gallery Tab
        with gr.Tab("📸 Gallery"):
            gallery_output = gr.Gallery(
                label="Images",
                value=get_gallery_images(),
                columns=4,
                rows=3,
                object_fit="scale-down",
                height="auto"
            )
            
            with gr.Row():
                search_input = gr.Textbox(
                    label="Search",
                    placeholder="Search images by filename..."
                )
                search_btn = gr.Button("🔍 Search")
            
            with gr.Row():
                refresh_btn = gr.Button("🔄 Refresh Gallery")
            
            search_btn.click(
                search_images,
                inputs=search_input,
                outputs=gallery_output
            )
            
            refresh_btn.click(
                lambda: get_gallery_images(),
                outputs=gallery_output
            )
        
        # Upload Tab
        with gr.Tab("⬆️ Upload"):
            gr.Markdown("### Upload New Images")
            
            with gr.Row():
                file_input = gr.File(
                    label="Select Image",
                    file_count="single",
                    file_types=["image"]
                )
                upload_btn = gr.Button("Upload")
            
            upload_status = gr.Textbox(label="Status", interactive=False)
            
            uploaded_gallery = gr.Gallery(
                label="Recent Uploads",
                columns=4,
                rows=2,
                object_fit="scale-down"
            )
            
            upload_btn.click(
                upload_image,
                inputs=file_input,
                outputs=[upload_status, uploaded_gallery]
            )
        
        # Manage Tab
        with gr.Tab("⚙️ Manage"):
            gr.Markdown("### Manage Images")
            
            manage_gallery = gr.Gallery(
                value=get_gallery_images(),
                label="Gallery Images",
                columns=4,
                rows=3,
                object_fit="scale-down",
                interactive=True,
                show_label=True
            )
            
            with gr.Row():
                refresh_manage_btn = gr.Button("🔄 Refresh")
            
            action_status = gr.Textbox(label="Status", interactive=False)
            
            refresh_manage_btn.click(
                lambda: get_gallery_images(),
                outputs=manage_gallery
            )
        
        # Info Tab
        with gr.Tab("ℹ️ Info"):
            gr.Markdown("""
            ## About This Gallery
            
            **Features:**
            - 📤 Upload images (PNG, JPG, GIF, WebP)
            - 🔍 Search and filter by filename
            - 🗂️ Organize and manage images
            - 📊 View image metadata (size, format)
            - 🐳 Run anywhere with Docker
            
            **Supported Formats:**
            - PNG
            - JPEG/JPG
            - GIF
            - WebP
            
            **Storage:**
            - Gallery: `images/gallery/`
            - Metadata: `images/metadata.json`
            
            **Version Info:**
            - Python: 3.13+
            - Gradio: 6.20.0+
            - Pillow: 10.2.0+
            """)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
