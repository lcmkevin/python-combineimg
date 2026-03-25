# Zoom Features - Image Combiner v3

## New Functionality

### Zoom Controls

Both the **Selected Image Preview** and **Output Preview** tabs now include interactive zoom controls:

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

## How to Use

### Example Workflow:

1. **Add images** using "📁 Add Images" button
2. **Select an image** from the list to preview
3. **Adjust zoom** using:
   - Buttons for preset zoom levels (Fit, 100%, Zoom In/Out)
   - Ctrl+Scroll wheel for fine control
4. **View output** in "Output Preview" tab
5. **Adjust output zoom** independently using same controls
6. **Export** final combined image with "✨ COMBINE IMAGES ✨"

### Zoom Modes:

- **Fit Mode** (Default):
  - Image scales to fit preview area completely
  - Maintains aspect ratio
  - Label shows "Fit"

- **100% Mode**:
  - Shows image at true resolution
  - May require scrolling for large images
  - Label shows "100%"

- **Custom Zoom**:
  - Any zoom level from 10% to 400%
  - Freely scroll to see different parts
  - Label shows current percentage (e.g., "150%")

## Technical Details

- Uses high-quality LANCZOS resampling for zoom scaling
- Zoom calculations preserve aspect ratio automatically
- Per-image zoom tracking prevents accidentally losing zoom adjustments
- Works with both selected image preview and combined output
- Smooth zoom increments of 10% for predictable control
