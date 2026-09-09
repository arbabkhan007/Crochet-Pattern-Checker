
from pathlib import Path
from typing import Optional
import webbrowser
import tempfile
import base64

class BrowserPDFViewer:
    """View PDFs in browser"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def view_pdf(self, pdf_path: str) -> str:
        """Open PDF in browser"""
        pdf_file = Path(pdf_path)
        
        if not pdf_file.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        # Read PDF and convert to base64
        with open(pdf_file, 'rb') as f:
            pdf_data = base64.b64encode(f.read()).decode()
        
        # Create HTML viewer
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>PDF Viewer - {pdf_file.name}</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            font-family: Arial, sans-serif;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }}
        .pdf-container {{
            width: 100%;
            height: 80vh;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        .controls {{
            margin: 20px 0;
        }}
        button {{
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            margin-right: 10px;
        }}
        button:hover {{
            background: #0056b3;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📄 {pdf_file.name}</h1>
        <div class="controls">
            <button onclick="window.print()">🖨️ Print</button>
            <button onclick="downloadPDF()">⬇️ Download</button>
            <button onclick="window.close()">❌ Close</button>
        </div>
        <div class="pdf-container">
            <iframe 
                src="data:application/pdf;base64,{pdf_data}" 
                width="100%" 
                height="100%"
                style="border: none;">
            </iframe>
        </div>
    </div>
    <script>
        function downloadPDF() {{
            const link = document.createElement('a');
            link.href = 'data:application/pdf;base64,{pdf_data}';
            link.download = '{pdf_file.name}';
            link.click();
        }}
    </script>
</body>
</html>
"""
        
        # Save HTML file
        html_path = Path(self.temp_dir) / f"{pdf_file.stem}_viewer.html"
        with open(html_path, 'w') as f:
            f.write(html_content)
        
        # Open in browser
        webbrowser.open(f'file://{html_path.absolute()}')
        
        return str(html_path)

class BrowserImageViewer:
    """View images in browser with controls"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def view_image(self, image_path: str, title: str = "Image Viewer") -> str:
        """Open image in browser with controls"""
        image_file = Path(image_path)
        
        if not image_file.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Read image and convert to base64
        with open(image_file, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode()
        
        # Determine MIME type
        mime_type = f"image/{image_file.suffix[1:]}"
        
        # Create HTML viewer
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            font-family: Arial, sans-serif;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #28a745;
            padding-bottom: 10px;
        }}
        .image-container {{
            text-align: center;
            margin: 20px 0;
        }}
        img {{
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
            transition: transform 0.3s ease;
        }}
        .controls {{
            margin: 20px 0;
            text-align: center;
        }}
        button {{
            background: #28a745;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            margin: 0 5px;
            font-size: 16px;
        }}
        button:hover {{
            background: #218838;
        }}
        .zoom-info {{
            margin: 10px 0;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🖼️ {title}</h1>
        <div class="controls">
            <button onclick="zoomIn()">🔍+ Zoom In</button>
            <button onclick="zoomOut()">🔍- Zoom Out</button>
            <button onclick="resetZoom()">↺ Reset</button>
            <button onclick="rotateImage()">🔄 Rotate</button>
            <button onclick="downloadImage()">⬇️ Download</button>
        </div>
        <div class="zoom-info">Zoom: <span id="zoomLevel">100%</span></div>
        <div class="image-container">
            <img id="mainImage" src="data:{mime_type};base64,{image_data}" alt="{title}">
        </div>
    </div>
    <script>
        let zoomLevel = 1;
        let rotation = 0;
        const image = document.getElementById('mainImage');
        const zoomDisplay = document.getElementById('zoomLevel');
        
        function updateTransform() {{
            image.style.transform = `scale(${{zoomLevel}}) rotate(${{rotation}}deg)`;
            zoomDisplay.textContent = Math.round(zoomLevel * 100) + '%';
        }}
        
        function zoomIn() {{
            zoomLevel = Math.min(zoomLevel + 0.25, 5);
            updateTransform();
        }}
        
        function zoomOut() {{
            zoomLevel = Math.max(zoomLevel - 0.25, 0.25);
            updateTransform();
        }}
        
        function resetZoom() {{
            zoomLevel = 1;
            rotation = 0;
            updateTransform();
        }}
        
        function rotateImage() {{
            rotation = (rotation + 90) % 360;
            updateTransform();
        }}
        
        function downloadImage() {{
            const link = document.createElement('a');
            link.href = 'data:{mime_type};base64,{image_data}';
            link.download = '{image_file.name}';
            link.click();
        }}
    </script>
</body>
</html>
"""
        
        # Save HTML file
        html_path = Path(self.temp_dir) / f"{image_file.stem}_viewer.html"
        with open(html_path, 'w') as f:
            f.write(html_content)
        
        # Open in browser
        webbrowser.open(f'file://{html_path.absolute()}')
        
        return str(html_path)

def view_pdf_in_browser(pdf_path: str) -> str:
    """Convenience function to view PDF in browser"""
    viewer = BrowserPDFViewer()
    return viewer.view_pdf(pdf_path)

def view_image_in_browser(image_path: str, title: str = "Image Viewer") -> str:
    """Convenience function to view image in browser"""
    viewer = BrowserImageViewer()
    return viewer.view_image(image_path, title)
