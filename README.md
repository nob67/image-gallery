# 🖼️ Image Gallery

A simple, Docker-based image gallery built with Gradio. No PHP, no Nginx, no complex configuration required.

## Features

- ✅ **Upload Images** - Drag and drop or select from your computer
- 🔍 **Search & Filter** - Find images by filename
- 🗂️ **Manage Images** - Delete, organize, and browse your collection
- 📊 **Image Metadata** - View image dimensions, format, and upload date
- 🐳 **Docker Ready** - One command to run anywhere
- 🎨 **Beautiful UI** - Built with Gradio for a modern interface

## Supported Image Formats

- PNG
- JPEG/JPG
- GIF
- WebP

## Quick Start

### Prerequisites

- Docker & Docker Compose installed ([Get Docker](https://www.docker.com/products/docker-desktop))
- That's it! ✨

### Run the Gallery

```bash
docker-compose up
```

The gallery will be available at: **http://localhost:7860**

### First Time Setup

1. Open http://localhost:7860 in your browser
2. Go to the **⬆️ Upload** tab
3. Upload your first image
4. Images are saved to `images/gallery/`

## Directory Structure

```
image-gallery/
├── app.py                 # Main Gradio application
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Docker Compose configuration
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── images/
    ├── uploads/           # Temporarily uploaded images
    ├── gallery/           # Main gallery images
    └── metadata.json      # Image metadata (auto-generated)
```

## Usage

### 📸 Gallery Tab
- View all images in a grid
- Search by filename
- Refresh to see new images

### ⬆️ Upload Tab
- Upload new images from your computer
- Supported formats: PNG, JPG, GIF, WebP
- Images are stored and indexed automatically

### ⚙️ Manage Tab
- Select and delete images
- View all gallery images
- Organize your collection

## Advanced Usage

### Stop the Gallery

```bash
docker-compose down
```

### View Logs

```bash
docker-compose logs -f
```

### Access Images Directly

Your images are stored in the `images/gallery/` directory on your computer. You can:
- Add images directly to this folder
- Back them up
- Share them

### Change Port

Edit `docker-compose.yml` and change the port mapping:

```yaml
ports:
  - "8080:7860"  # Access at http://localhost:8080
```

### Increase Upload Limit

The default upload limit is 5GB per file. To change it, edit `docker-compose.yml`:

```yaml
environment:
  - GRADIO_MAX_FILE_SIZE=10gb
```

## Deployment

### Render.com (Free)

1. Push to GitHub
2. Connect to Render.com
3. Select "Docker" as the environment
4. Deploy automatically

### Other Cloud Platforms

- AWS (ECS)
- Google Cloud (Cloud Run)
- Azure (Container Instances)
- DigitalOcean (App Platform)
- Heroku (with buildpack)

All support Docker out of the box!

## Performance Tips

- Store images on a fast disk (SSD recommended)
- Limit gallery size to 10,000+ images for best performance
- Use image optimization tools to reduce file sizes
- Enable browser caching for faster loading

## Troubleshooting

### Port 7860 Already In Use

Change the port in `docker-compose.yml`:

```yaml
ports:
  - "7861:7860"  # Use port 7861 instead
```

### Images Not Appearing

1. Refresh the page (F5)
2. Click the 🔄 Refresh button in the Gallery tab
3. Ensure images are in `images/gallery/` directory

### Container Won't Start

Check the logs:

```bash
docker-compose logs gallery
```

### Upload Fails

- Check file size (default 5GB limit)
- Verify file format is supported
- Ensure disk has free space

## Development

### Local Development (No Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

Then open http://localhost:7860

### Modify the Gallery

Edit `app.py` and restart:

```bash
docker-compose restart
```

## License

MIT License - See LICENSE file

## Support

For issues or feature requests, please open an issue on GitHub.

---

**Built with ❤️ using Gradio and Docker**