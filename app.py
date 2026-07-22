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
    for file in sorted(os.listdir(GALLERY_DIR)):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            filepath = os.path.join(GALLERY_DIR, file)
            images.append(filepath)
    return images

def upload_image(file):
    """Handle image upload"""
    if file is None:
        return "No file uploaded", get_gallery_images()
    
    # Save uploaded file
    filename = os.path.basename(file.name)
    save_path = os.path.join(UPLOAD_DIR, filename)
    
    # Use PIL to verify it's a valid image
    try:
        img = Image.open(file.name)
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

def move_to_gallery(image_path):
    """Move image from uploads to gallery"""
    if not image_path:
        return "No image selected", get_gallery_images()
    
    try:
        filename = os.path.basename(image_path)
        gallery_path = os.path.join(GALLERY_DIR, filename)
        
        # Copy to gallery
        img = Image.open(image_path)
        img.save(gallery_path)
        
        return f"✅ Image moved to gallery!", get_gallery_images()
    except Exception as e:
        return f"❌ Error: {str(e)}", get_gallery_images()

def delete_image(image_path):
    """Delete image from gallery"""
    if not image_path:
        return "No image selected", get_gallery_images()
    
    try:
        os.remove(image_path)
        
        # Update metadata
        filename = os.path.basename(image_path)
        metadata = load_metadata()
        if filename in metadata:
            del metadata[filename]
        save_metadata(metadata)
        
        return f"✅ Image deleted!", get_gallery_images()
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
            
            search_btn.click(
                search_images,
                inputs=search_input,
                outputs=gallery_output
            )
            
            refresh_btn = gr.Button("🔄 Refresh Gallery")
            refresh_btn.click(
                lambda: get_gallery_images(),
                outputs=gallery_output
            )
        
        # Upload Tab
        with gr.Tab("⬆️ Upload"):
            gr.Markdown("### Upload New Images")
            
            with gr.Row():
                file_input = gr.File(label="Select Image", file_types=["image"])
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
                object_fit="scale-down"
            )
            
            selected_image = gr.Textbox(
                label="Selected Image Path",
                interactive=False
            )
            
            with gr.Row():
                delete_btn = gr.Button("🗑️ Delete Selected", variant="stop")
                refresh_manage_btn = gr.Button("🔄 Refresh")
            
            action_status = gr.Textbox(label="Status", interactive=False)
            
            manage_gallery.select(
                lambda x: x if isinstance(x, str) else "",
                inputs=manage_gallery,
                outputs=selected_image
            )
            
            delete_btn.click(
                delete_image,
                inputs=selected_image,
                outputs=[action_status, manage_gallery]
            )
            
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
            - 🐳 Run in Docker - no configuration needed
            
            **Supported Formats:**
            - PNG
            - JPEG/JPG
            - GIF
            - WebP
            
            **Storage:**
            - Uploads: `images/uploads/`
            - Gallery: `images/gallery/`
            - Metadata: `images/metadata.json`
            """)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
