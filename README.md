# Design Idea

A user request to create a one page picture by combining different picture(s) or pdf(s) together. 

# Image Combiner v3 - Complete Feature Guide

A powerful GUI application for combining multiple images horizontally or vertically with advanced preview and zoom capabilities.

## 🚀 Core Features

### Image Combination
- **Horizontal/Vertical Layout**: Combine images side-by-side or stacked
- **Order Management**: Reorder images with up/down buttons
- **Batch Processing**: Add multiple images at once
- **Format Support**: JPEG, PNG, PDF (via first-page import) and other common formats

### Advanced Preview System
- **Dual Preview Tabs**:
  - **Selected Image Preview**: Individual image inspection
  - **Output Preview**: Combined result visualization
- **Real-time Updates**: Previews update instantly when images change
- **Full Screen Mode**: Dedicated fullscreen preview window

## 🔍 Zoom & Navigation Features

### Interactive Zoom Controls

Both preview tabs include comprehensive zoom functionality:

#### Preset Buttons:
- **🔍- Zoom Out**: Decreases zoom by 10% (minimum 10%)
- **Fit**: Automatically sizes image to fit within preview area (smart fit)
- **100%**: Displays image at true 100% size (no scaling)
- **Zoom In 🔍+**: Increases zoom by 10% (maximum 400%)

#### Zoom Level Display:
- Live zoom percentage/status shown in display field next to buttons
- Shows "Fit" when in fit-to-window mode

### Keyboard/Mouse Controls:
- **Ctrl + Mouse Wheel**: Zoom in/out smoothly
  - Scroll up with Ctrl = Zoom in
  - Scroll down with Ctrl = Zoom out
- **Shift + Mouse Wheel**: Horizontal scrolling (existing feature)
- **Normal Mouse Wheel**: Vertical scrolling (existing feature)

### Persistent Zoom State:
- Each selected image remembers its last zoom level
- Switching between images preserves individual zoom settings
- Output preview has its own independent zoom level
- Zoom state resets when clearing all images

## 📊 Information Panels

### Size Information Box (Lower Left)
Displays aggregate statistics about all loaded images:
- **📊 Total Original Size**: Combined file size of all images
- **🎨 Total Pixels**: Sum of pixel counts across all images
- **💾 Estimated Output Size**: Predicted JPEG file size (15:1 compression)

### File Information Box (Lower Left)
Shows detailed information for the currently selected image:
- **📷 Filename**: Image name and path
- **📏 Original Dimensions**: True image resolution
- **📐 Displayed Dimensions**: Current scaled size (if different)
- **💾 File Size**: Disk space used
- **🖱️ Controls**: Available interaction methods
- **💡 Tips**: Usage hints

## 🎛️ User Interface Layout

### Left Panel (Control & Information)
```
┌─ Controls ──────────────────────┐
│ Direction: ○ Horizontal ● Vertical │
│ [📁 Add Images] [🗑 Remove] [🗑 Clear] │
├─ Image List ────────────────────┤
│ image1.jpg (1920x1080)          │
│ image2.jpg (1280x720)           │
│ [↑ Move Up] [↓ Move Down]       │
├─ Size Information ──────────────┤
│ 📊 Total Original Size: 5.2 MB  │
│ 🎨 Total Pixels: 3,932,160      │
│ 💾 Estimated Output Size: ~1.5 MB│
├─ File Information ──────────────┤
│ 📷 image1.jpg                   │
│ 📏 Original: 1920 x 1080 pixels │
│ 📐 Displayed: 800 x 450 pixels  │
│ 💾 File Size: 2.1 MB            │
│ 🖱️ Use buttons or Ctrl+Scroll   │
│ 💡 Hold Shift + Scroll          │
└─────────────────────────────────┘
```

### Right Panel (Preview & Controls)
```
┌─ Selected Image Preview ──────┬─ Output Preview ──────────┐
│ [🔍 Full Screen] [🔍-] [Fit] [100%] [🔍+] [Fit] │
│                              │                           │
│        [Image Preview]       │    [Combined Preview]    │
│                              │                           │
├─ Preview Information ────────┴───────────────────────────┤
│ 📐 Layout: 3 images horizontally                        │
│ 📏 Output Dimensions: 4000 x 1080 pixels               │
│ 🖱️ Use scrollbars to view full image                   │
│ 💡 Hold Shift + Scroll for horizontal scrolling        │
│ 🔍 Zoom: Fit | Use buttons or Ctrl+Scroll to zoom      │
├──────────────────────────────────────────────────────────┤
│                    [✨ COMBINE IMAGES ✨]                 │
└──────────────────────────────────────────────────────────┘
```

## 📋 How to Use

### Basic Workflow:

1. **Launch Application**:
   ```bash
   python combineimgv3.py --gui
   ```

2. **Add Images**:
   - Click "📁 Add Images" button
   - Select multiple image files
   - Images appear in the list with dimensions

3. **Configure Layout**:
   - Choose "Horizontal" or "Vertical" direction
   - Reorder images using ↑↓ buttons if needed
   - Imported PDF pages appear as separate items (PDF page 1, page 2, ...)

4. **Preview Images**:
   - Click any image in the list to preview individually
   - Use zoom controls to inspect details
   - Switch to "Output Preview" tab to see combined result

5. **Adjust Zoom**:
   - Use preset buttons (Fit, 100%, Zoom In/Out)
   - Or Ctrl+Mouse Wheel for smooth zooming
   - Each image remembers its zoom level

6. **Combine & Save**:
   - Click "✨ COMBINE IMAGES ✨" button
   - Choose save location and format
   - Combined image is saved

### Advanced Features:

- **Full Screen Preview**: Click "🔍 Full Screen Preview" for distraction-free viewing
- **Real-time Updates**: All previews update instantly when you change settings
- **Persistent Zoom**: Your zoom preferences are remembered per image
- **Size Estimation**: Get accurate file size predictions before saving

## 🎨 Zoom Modes Explained

### Fit Mode (Default):
- Image scales to fit preview area completely
- Maintains aspect ratio automatically
- Perfect for overview and comparison
- Label shows "Fit"

### 100% Mode:
- Shows image at true resolution (1:1 pixels)
- May require scrolling for large images
- Ideal for pixel-perfect inspection
- Label shows "100%"

### Custom Zoom:
- Any zoom level from 10% to 400%
- Freely scroll to examine specific areas
- Label shows current percentage (e.g., "150%")
- Useful for detailed work

## 🔧 Technical Specifications

### Image Processing:
- **Library**: PIL (Pillow) for robust image handling
- **Resampling**: High-quality LANCZOS algorithm for zoom operations
- **Format Support**: JPEG, PNG, and other PIL-supported formats
- **Memory Management**: Efficient image caching and cleanup

### Zoom System:
- **Range**: 10% to 400% zoom levels
- **Increments**: 10% steps for predictable control
- **Persistence**: Per-image zoom state tracking
- **Aspect Ratio**: Always preserved during scaling

### UI Framework:
- **GUI Library**: Tkinter with ttk styling
- **Layout**: Responsive paned windows
- **Navigation**: Tabbed interface for organized workflow
- **Status Updates**: Real-time feedback and progress indication

## 🐛 Troubleshooting

### Common Issues:

- **Images not loading**: Check file format compatibility
- **Preview not updating**: Try clearing and re-adding images
- **Zoom not working**: Ensure image is selected first
- **Memory issues**: Clear images periodically for large batches

### Performance Tips:

- **Large images**: Use "Fit" mode for faster preview updates
- **Many images**: Clear unused images to free memory
- **High zoom levels**: May be slower with very large images

## 📝 CLI Mode

The script also supports command-line operation:

```bash
# Combine all images in current directory horizontally
python combineimgv3.py

# Combine vertically
python combineimgv3.py --vertical

# Specify output file
python combineimgv3.py --output combined_result.jpg

# Different format
python combineimgv3.py --format PNG
```

## 🎯 Feature Highlights

- ✅ **Smart Auto-Fit**: Images automatically scale to fit preview areas
- ✅ **Persistent Zoom**: Each image remembers your preferred zoom level
- ✅ **Dual Preview**: Individual and combined result previews
- ✅ **Full Screen Mode**: Distraction-free image inspection
- ✅ **Real-time Updates**: Instant feedback on all changes
- ✅ **Size Estimation**: Accurate output file size prediction
- ✅ **Flexible Layout**: Horizontal or vertical image arrangement
- ✅ **Order Management**: Easy reordering of image sequence
- ✅ **Format Support**: Multiple input/output formats
- ✅ **User-Friendly**: Intuitive GUI with helpful information panels

---

**Ready to combine your images?** Launch the GUI and start creating stunning image compositions! 🎨✨
