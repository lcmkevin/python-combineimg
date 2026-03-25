from PIL import Image, ImageTk, ImageOps
import glob
import sys
import os
import argparse
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class FullScreenPreview:
    """Full screen preview window"""
    def __init__(self, parent, image_path=None, pil_image=None):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Full Screen Preview")
        self.window.attributes('-fullscreen', True)
        
        # Store the image
        self.pil_image = pil_image
        self.image_path = image_path
        self.photo_image = None
        
        # Setup UI
        self.setup_ui()
        
        # Load and display image
        if pil_image:
            self.display_image(pil_image)
        elif image_path:
            self.load_and_display_image()
        
        # Bind escape key to close
        self.window.bind('<Escape>', self.close)
        self.window.bind('<F11>', self.toggle_fullscreen)
    
    def setup_ui(self):
        """Setup full screen UI"""
        # Create frame for controls
        control_frame = ttk.Frame(self.window)
        control_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        
        # Close button
        close_btn = ttk.Button(control_frame, text="✖ Close (Esc)", command=self.close)
        close_btn.pack(side=tk.RIGHT, padx=5)
        
        # Info label
        self.info_label = ttk.Label(control_frame, text="", font=("TkDefaultFont", 10))
        self.info_label.pack(side=tk.LEFT, padx=10)
        
        # Create canvas for image with scrollbars
        canvas_frame = ttk.Frame(self.window)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(canvas_frame, highlightthickness=0, bg='black')
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.canvas.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        
        # Create frame inside canvas for the image
        self.image_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.image_frame, anchor="nw")
        
        self.image_label = ttk.Label(self.image_frame)
        self.image_label.pack(padx=10, pady=10)
        
        # Bind mouse wheel
        self.bind_mouse_wheel()
        
        # Bind frame configure
        self.image_frame.bind("<Configure>", self.on_frame_configure)
        
        # Bind window resize
        self.window.bind('<Configure>', self.on_window_resize)
    
    def bind_mouse_wheel(self):
        """Bind mouse wheel scrolling"""
        def on_mousewheel(event):
            if event.state & 0x1:  # Shift key for horizontal scroll
                self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
            else:
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    def on_frame_configure(self, event):
        """Update scroll region"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        canvas_width = self.canvas.winfo_width()
        if canvas_width > 1:
            self.canvas.itemconfig(self.canvas_window, width=canvas_width)
    
    def on_window_resize(self, event):
        """Handle window resize"""
        if self.photo_image:
            canvas_width = self.canvas.winfo_width()
            if canvas_width > 1:
                self.canvas.itemconfig(self.canvas_window, width=canvas_width)
    
    def load_and_display_image(self):
        """Load and display image from file"""
        try:
            img = Image.open(self.image_path)
            self.display_image(img)
            
            # Update info
            file_size = os.path.getsize(self.image_path)
            if file_size < 1024 * 1024:
                size_str = f"{file_size / 1024:.1f} KB"
            else:
                size_str = f"{file_size / (1024 * 1024):.1f} MB"
            
            info = f"📷 {os.path.basename(self.image_path)} | "
            info += f"Dimensions: {img.size[0]} x {img.size[1]} pixels | "
            info += f"Size: {size_str}"
            self.info_label.configure(text=info)
            
        except Exception as e:
            self.image_label.configure(text=f"Error loading image:\n{str(e)}")
    
    def display_image(self, pil_image):
        """Display PIL image"""
        self.pil_image = pil_image

        # Ensure full image fits on screen in fullscreen window
        self.window.update_idletasks()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        display_img = pil_image
        if pil_image.width > screen_width or pil_image.height > screen_height:
            display_img = ImageOps.contain(pil_image, (screen_width, screen_height))

        photo = ImageTk.PhotoImage(display_img)
        self.photo_image = photo
        self.image_label.configure(image=photo, text="")
        self.image_label.image = photo

        if display_img.size != pil_image.size:
            self.info_label.configure(text=f"Showing scaled image: {display_img.size[0]}x{display_img.size[1]} (original {pil_image.size[0]}x{pil_image.size[1]})")
        
        # Update scroll region
        self.image_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        # Set canvas window width
        canvas_width = self.canvas.winfo_width()
        if canvas_width > 1:
            self.canvas.itemconfig(self.canvas_window, width=canvas_width)
    
    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode"""
        is_fullscreen = self.window.attributes('-fullscreen')
        self.window.attributes('-fullscreen', not is_fullscreen)
    
    def close(self, event=None):
        """Close the preview window"""
        self.window.destroy()

class ImageCombinerGUI:
    def __init__(self, root):
        """Initialize the main application"""
        self.root = root
        self.root.title("Image Combiner")
        self.root.geometry("1400x800")
        
        # Data storage
        self.images = []
        self.image_sizes = {}
        self.preview_images = []
        self.current_preview_image = None
        self.current_output_preview = None
        
        # UI Variables
        self.direction = tk.StringVar(value="horizontal")
        
        # Zoom state tracking - stores zoom % per image path
        self.selected_zoom = tk.DoubleVar(value=100.0)
        self.output_zoom = tk.DoubleVar(value=100.0)
        self.zoom_levels = {}  # Store zoom level per image path
        
        # Setup UI components
        self.setup_ui()
        
        # Initialize empty state
        self.update_size_info()
        self.file_info_label.configure(text="Select an image to see details")
    
    # ==================== UI SETUP FUNCTIONS ====================
    
    def setup_ui(self):
        """Main UI setup orchestrator"""
        # Create main paned window
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Image list
        self.setup_left_panel()
        
        # Right panel - Preview
        self.setup_right_panel()
        
        # Status bar
        self.setup_status_bar()
    
    def setup_left_panel(self):
        """Setup left panel with image list and controls"""
        left_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(left_frame, weight=1)
        
        # Control section
        self.setup_control_section(left_frame)
        
        # Image list section
        self.setup_image_list_section(left_frame)
        
        # Size info section
        self.setup_size_info_section(left_frame)
        
        # File info section
        self.setup_file_info_section(left_frame)
    
    def setup_control_section(self, parent):
        """Setup control buttons and direction selection"""
        control_frame = ttk.LabelFrame(parent, text="Controls", padding="10")
        control_frame.pack(fill=tk.X, pady=(0, 10), padx=5)
        
        # Direction selection
        direction_frame = ttk.Frame(control_frame)
        direction_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(direction_frame, text="Direction:").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(direction_frame, text="Horizontal", 
                       variable=self.direction, value="horizontal",
                       command=self.on_direction_change).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(direction_frame, text="Vertical", 
                       variable=self.direction, value="vertical",
                       command=self.on_direction_change).pack(side=tk.LEFT, padx=5)
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="📁 Add Images", 
                  command=self.on_add_images).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="🗑 Remove Selected", 
                  command=self.on_remove_selected).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="🗑 Clear All", 
                  command=self.on_clear_all).pack(side=tk.LEFT, padx=2)
    
    def setup_image_list_section(self, parent):
        """Setup image listbox with ordering controls"""
        list_frame = ttk.LabelFrame(parent, text="Image List", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)
        
        # Listbox with scrollbar
        listbox_container = ttk.Frame(list_frame)
        listbox_container.pack(fill=tk.BOTH, expand=True)
        
        self.listbox = tk.Listbox(listbox_container, selectmode=tk.SINGLE, height=12)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind('<<ListboxSelect>>', self.on_image_select)
        
        list_scrollbar = ttk.Scrollbar(listbox_container, orient=tk.VERTICAL, command=self.listbox.yview)
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=list_scrollbar.set)
        
        # Order control buttons
        order_frame = ttk.Frame(list_frame)
        order_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(order_frame, text="↑ Move Up", command=self.on_move_up).pack(side=tk.LEFT, padx=2)
        ttk.Button(order_frame, text="↓ Move Down", command=self.on_move_down).pack(side=tk.LEFT, padx=2)
    
    def setup_size_info_section(self, parent):
        """Setup size information display"""
        size_frame = ttk.LabelFrame(parent, text="Size Information", padding="10")
        size_frame.pack(fill=tk.X, pady=5, padx=5)
        
        self.size_info_label = ttk.Label(size_frame, text="", justify=tk.LEFT)
        self.size_info_label.pack(anchor=tk.W)
    
    def setup_file_info_section(self, parent):
        """Setup file information display"""
        file_frame = ttk.LabelFrame(parent, text="File Information", padding="10")
        file_frame.pack(fill=tk.X, pady=5, padx=5)
        
        self.file_info_label = ttk.Label(file_frame, text="", justify=tk.LEFT)
        self.file_info_label.pack(anchor=tk.W)
    
    def setup_right_panel(self):
        """Setup right panel with preview tabs"""
        right_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(right_frame, weight=2)
        
        # Create Notebook for tabs
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Selected Image Preview
        self.setup_selected_preview_tab()
        
        # Tab 2: Output Preview
        self.setup_output_preview_tab()
        
        # Combine button at bottom of right panel
        self.setup_combine_button(right_frame)
    
    def setup_selected_preview_tab(self):
        """Setup selected image preview tab"""
        selected_tab = ttk.Frame(self.notebook)
        self.notebook.add(selected_tab, text="Selected Image Preview")
        
        # Create a frame that will expand
        main_frame = ttk.Frame(selected_tab)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create LabelFrame for preview
        preview_frame = ttk.LabelFrame(main_frame, text="Image Preview", padding="5")
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas with scrollbars
        self.selected_canvas = tk.Canvas(preview_frame, highlightthickness=0, bg='gray20')
        v_scrollbar = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=self.selected_canvas.yview)
        h_scrollbar = ttk.Scrollbar(preview_frame, orient=tk.HORIZONTAL, command=self.selected_canvas.xview)
        
        self.selected_canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout with proper weights
        self.selected_canvas.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        preview_frame.grid_rowconfigure(0, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)
        
        # Create frame inside canvas for the image
        self.selected_image_frame = ttk.Frame(self.selected_canvas)
        self.selected_canvas_window = self.selected_canvas.create_window((0, 0), window=self.selected_image_frame, anchor="nw")
        
        # Button frame for full screen
        button_frame = ttk.Frame(self.selected_image_frame)
        button_frame.pack(pady=5)
        
        self.selected_fullscreen_btn = ttk.Button(button_frame, text="🔍 Full Screen Preview", 
                                                   command=self.show_selected_fullscreen,
                                                   state=tk.DISABLED)
        self.selected_fullscreen_btn.pack(side=tk.LEFT, padx=2)
        
        # Zoom control buttons
        ttk.Button(button_frame, text="🔍- Zoom Out", 
                  command=self.on_selected_zoom_out).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Fit", 
                  command=self.on_selected_set_zoom_fit).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="100%", 
                  command=self.on_selected_set_zoom_100).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Zoom In 🔍+", 
                  command=self.on_selected_zoom_in).pack(side=tk.LEFT, padx=2)
        
        # Zoom level label
        self.selected_zoom_label = ttk.Label(button_frame, text="100%", width=5)
        self.selected_zoom_label.pack(side=tk.LEFT, padx=5)
        
        self.selected_preview_label = ttk.Label(self.selected_image_frame, text="Select an image from the list")
        self.selected_preview_label.pack(padx=10, pady=10)
        
        # Update scroll region when frame changes
        self.selected_image_frame.bind("<Configure>", self.on_selected_frame_configure)
        
        # Bind mouse wheel for scrolling with shift for horizontal
        self.bind_mouse_wheel(self.selected_canvas)
    
    def setup_output_preview_tab(self):
        """Setup output preview tab"""
        output_tab = ttk.Frame(self.notebook)
        self.notebook.add(output_tab, text="Output Preview")
        
        # Create a frame that will expand
        main_frame = ttk.Frame(output_tab)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create LabelFrame for preview
        preview_frame = ttk.LabelFrame(main_frame, text="Combined Output Preview", padding="5")
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas with scrollbars
        self.output_canvas = tk.Canvas(preview_frame, highlightthickness=0, bg='gray20')
        v_scrollbar = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=self.output_canvas.yview)
        h_scrollbar = ttk.Scrollbar(preview_frame, orient=tk.HORIZONTAL, command=self.output_canvas.xview)
        
        self.output_canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout with proper weights
        self.output_canvas.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        preview_frame.grid_rowconfigure(0, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)
        
        # Create frame inside canvas for the image
        self.output_image_frame = ttk.Frame(self.output_canvas)
        self.output_canvas_window = self.output_canvas.create_window((0, 0), window=self.output_image_frame, anchor="nw")
        
        # Button frame for full screen
        button_frame = ttk.Frame(self.output_image_frame)
        button_frame.pack(pady=5)
        
        self.output_fullscreen_btn = ttk.Button(button_frame, text="🔍 Full Screen Preview", 
                                                 command=self.show_output_fullscreen,
                                                 state=tk.DISABLED)
        self.output_fullscreen_btn.pack(side=tk.LEFT, padx=2)
        
        # Zoom control buttons
        ttk.Button(button_frame, text="🔍- Zoom Out", 
                  command=self.on_output_zoom_out).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Fit", 
                  command=self.on_output_set_zoom_fit).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="100%", 
                  command=self.on_output_set_zoom_100).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Zoom In 🔍+", 
                  command=self.on_output_zoom_in).pack(side=tk.LEFT, padx=2)
        
        # Zoom level label
        self.output_zoom_label = ttk.Label(button_frame, text="100%", width=5)
        self.output_zoom_label.pack(side=tk.LEFT, padx=5)
        
        self.output_preview_label = ttk.Label(self.output_image_frame, text="Add images to see preview")
        self.output_preview_label.pack(padx=10, pady=10)
        
        # Output preview info
        self.preview_info_frame = ttk.LabelFrame(output_tab, text="Preview Information", padding="5")
        self.preview_info_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        self.preview_info_label = ttk.Label(self.preview_info_frame, text="", justify=tk.LEFT)
        self.preview_info_label.pack(anchor=tk.W)
        
        # Update scroll region when frame changes
        self.output_image_frame.bind("<Configure>", self.on_output_frame_configure)
        
        # Bind mouse wheel for scrolling with shift for horizontal
        self.bind_mouse_wheel(self.output_canvas)
    
    def bind_mouse_wheel(self, canvas):
        """Bind mouse wheel scrolling with shift for horizontal scroll and Ctrl for zoom"""
        def on_mousewheel(event):
            if event.state & 0x4:  # Ctrl key pressed for zoom
                if canvas == self.selected_canvas:
                    if event.delta > 0:
                        self.on_selected_zoom_in()
                    else:
                        self.on_selected_zoom_out()
                elif canvas == self.output_canvas:
                    if event.delta > 0:
                        self.on_output_zoom_in()
                    else:
                        self.on_output_zoom_out()
            elif event.state & 0x1:  # Shift key pressed for horizontal scroll
                canvas.xview_scroll(int(-1*(event.delta/120)), "units")
            else:  # Normal vertical scroll
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    def on_selected_frame_configure(self, event):
        """Update scroll region for selected preview canvas"""
        self.selected_canvas.configure(scrollregion=self.selected_canvas.bbox("all"))
        canvas_width = self.selected_canvas.winfo_width()
        if canvas_width > 1:
            self.selected_canvas.itemconfig(self.selected_canvas_window, width=canvas_width)
    
    def on_output_frame_configure(self, event):
        """Update scroll region for output preview canvas"""
        self.output_canvas.configure(scrollregion=self.output_canvas.bbox("all"))
        canvas_width = self.output_canvas.winfo_width()
        if canvas_width > 1:
            self.output_canvas.itemconfig(self.output_canvas_window, width=canvas_width)
    
    def setup_combine_button(self, parent):
        """Setup combine button at bottom"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=10)
        
        combine_button = ttk.Button(button_frame, text="✨ COMBINE IMAGES ✨", 
                                    command=self.on_combine_images,
                                    style="Accent.TButton")
        combine_button.pack(pady=5)
        
        # Configure style
        style = ttk.Style()
        style.configure("Accent.TButton", font=('TkDefaultFont', 11, 'bold'))
    
    def setup_status_bar(self):
        """Setup status bar at bottom"""
        self.status_label = ttk.Label(self.root, text="Ready - Click 'Add Images' to get started", 
                                      relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)
    
    # ==================== FULL SCREEN FUNCTIONS ====================
    
    def show_selected_fullscreen(self):
        """Show selected image in full screen"""
        if self.current_preview_image and hasattr(self, 'current_preview_path'):
            FullScreenPreview(self.root, image_path=self.current_preview_path)
    
    def show_output_fullscreen(self):
        """Show output preview in full screen"""
        if self.current_output_preview and hasattr(self, 'current_output_image'):
            FullScreenPreview(self.root, pil_image=self.current_output_image)
    
    # ==================== IMAGE MANAGEMENT FUNCTIONS ====================
    
    def add_image_to_list(self, image_path):
        """Add image to listbox with dimensions"""
        try:
            img = Image.open(image_path)
            self.listbox.insert(tk.END, f"{os.path.basename(image_path)} ({img.size[0]}x{img.size[1]})")
            self.image_sizes[image_path] = img.size
            return True
        except Exception as e:
            self.listbox.insert(tk.END, f"{os.path.basename(image_path)} (Error loading)")
            return False
    
    def refresh_listbox(self):
        """Refresh the listbox display"""
        self.listbox.delete(0, tk.END)
        for img_path in self.images:
            self.add_image_to_list(img_path)
    
    def get_image_dimensions(self, image_path):
        """Get dimensions of an image"""
        if image_path in self.image_sizes:
            return self.image_sizes[image_path]
        else:
            img = Image.open(image_path)
            return img.size
    
    def calculate_total_size_info(self):
        """Calculate total original size, total pixels, and estimated output size"""
        if not self.images:
            return None, None, None
        
        total_original_size = 0
        total_pixels = 0
        
        for img_path in self.images:
            width, height = self.get_image_dimensions(img_path)
            file_size = os.path.getsize(img_path)
            total_original_size += file_size
            total_pixels += width * height
        
        # Format original size
        if total_original_size < 1024 * 1024:
            original_size_str = f"{total_original_size / 1024:.1f} KB"
        else:
            original_size_str = f"{total_original_size / (1024 * 1024):.1f} MB"
        
        # Estimate output size (JPEG compression ~15:1)
        estimated_bytes = total_pixels * 3
        estimated_mb = estimated_bytes / (1024 * 1024)
        compressed_mb = estimated_mb / 15
        
        if compressed_mb < 1:
            output_size_str = f"~{compressed_mb * 1024:.1f} KB"
        else:
            output_size_str = f"~{compressed_mb:.1f} MB"
        
        return original_size_str, f"{total_pixels:,}", output_size_str
    
    # ==================== PREVIEW FUNCTIONS ====================
    
    def fit_image_to_canvas(self, pil_image, canvas, margin=24):
        """Scale image to fit inside canvas while keeping aspect ratio."""
        canvas.update_idletasks()
        max_width = canvas.winfo_width() - margin
        max_height = canvas.winfo_height() - margin

        if max_width <= 0 or max_height <= 0:
            max_width = self.root.winfo_width() - margin
            max_height = self.root.winfo_height() - margin

        max_width = max(1, max_width)
        max_height = max(1, max_height)

        if pil_image.width > max_width or pil_image.height > max_height:
            return ImageOps.contain(pil_image, (max_width, max_height))
        return pil_image

    def apply_zoom_to_image(self, pil_image, zoom_percent):
        """Apply zoom percentage to image with aspect ratio preservation."""
        if zoom_percent <= 0 or zoom_percent == 100:
            return pil_image
        
        new_width = int(pil_image.width * zoom_percent / 100)
        new_height = int(pil_image.height * zoom_percent / 100)
        
        # Ensure minimum size
        new_width = max(1, new_width)
        new_height = max(1, new_height)
        
        return pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def apply_zoom_based_on_mode(self, pil_image, canvas, zoom_mode):
        """Apply zoom based on preset mode: 'fit', '100%', or 'actual'."""
        if zoom_mode == 'fit':
            return self.fit_image_to_canvas(pil_image, canvas)
        elif zoom_mode == '100%':
            return pil_image
        elif zoom_mode == 'actual':
            # Fit to canvas if larger than canvas
            return self.fit_image_to_canvas(pil_image, canvas)
        return pil_image

    def show_selected_preview(self, image_path):
        """Show preview of selected image with zoom level support"""
        try:
            img = Image.open(image_path)
            
            # Check zoom level for this image
            zoom_level = self.zoom_levels.get(image_path, 100.0)
            self.selected_zoom.set(zoom_level)
            
            # Apply zoom if not 100%
            if zoom_level != 100:
                display_img = self.apply_zoom_to_image(img, zoom_level)
                self.selected_zoom_label.configure(text=f"{int(zoom_level)}%")
            else:
                display_img = self.fit_image_to_canvas(img, self.selected_canvas)
                self.selected_zoom_label.configure(text="Fit")
            
            photo = ImageTk.PhotoImage(display_img)
            
            self.current_preview_image = photo
            self.current_preview_path = image_path
            self.preview_images.append(photo)
            
            # Get file size
            file_size = os.path.getsize(image_path)
            if file_size < 1024 * 1024:
                size_str = f"{file_size / 1024:.1f} KB"
            else:
                size_str = f"{file_size / (1024 * 1024):.1f} MB"
            
            displayed_w, displayed_h = display_img.size
            info_text = f"📷 {os.path.basename(image_path)}\n"
            info_text += f"📏 Original: {img.size[0]} x {img.size[1]} pixels\n"
            if (displayed_w, displayed_h) != img.size:
                info_text += f"📐 Displayed: {displayed_w} x {displayed_h} pixels\n"
            info_text += f"💾 File Size: {size_str}\n"
            info_text += f"🖱️ Use buttons or Ctrl+Scroll to zoom\n"
            info_text += f"💡 Hold Shift + Scroll for horizontal scrolling"
            
            # Update file info in bottom panel instead of preview
            self.file_info_label.configure(text=info_text)
            
            self.selected_preview_label.configure(image=photo, text="", compound=tk.TOP)
            self.selected_preview_label.image = photo
            
            # Enable full screen button
            self.selected_fullscreen_btn.configure(state=tk.NORMAL)
            
            # Force update to calculate proper size
            self.selected_image_frame.update_idletasks()
            
            # Update scroll region after the frame size is known
            self.selected_canvas.configure(scrollregion=self.selected_canvas.bbox("all"))
            
            # Also update canvas window width
            canvas_width = self.selected_canvas.winfo_width()
            if canvas_width > 1:
                self.selected_canvas.itemconfig(self.selected_canvas_window, width=canvas_width)
            
            self.update_status(f"Previewing: {os.path.basename(image_path)} ({img.size[0]}x{img.size[1]})")
            
        except Exception as e:
            self.selected_preview_label.configure(text=f"Error loading image:\n{str(e)}", image="")
            self.file_info_label.configure(text="Error loading image details")
            self.update_status("Error loading preview")
    
    def show_selected_preview_fit(self, image_path):
        """Show selected preview in fit-to-window mode (100% zoom)"""
        self.selected_zoom.set(100.0)
        self.selected_zoom_label.configure(text="Fit")
        if image_path in self.zoom_levels:
            del self.zoom_levels[image_path]
        self.show_selected_preview(image_path)
    
    def generate_output_preview(self):
        """Generate the output preview image"""
        if not self.images:
            return None, None
        
        imgs = [Image.open(f) for f in self.images]
        direction = self.direction.get()
        
        if direction == 'horizontal':
            total_width = sum(i.width for i in imgs)
            max_height = max(i.height for i in imgs)
            
            preview_img = Image.new('RGB', (total_width, max_height), 'gray')
            x = 0
            for img in imgs:
                preview_img.paste(img, (x, 0))
                x += img.width
            
            info = f"📐 Layout: {len(imgs)} images horizontally\n"
            info += f"📏 Output Dimensions: {total_width} x {max_height} pixels\n"
            info += f"🖱️ Use scrollbars to view full image\n"
            info += f"💡 Hold Shift + Scroll for horizontal scrolling"
            
        else:  # vertical
            max_width = max(i.width for i in imgs)
            total_height = sum(i.height for i in imgs)
            
            preview_img = Image.new('RGB', (max_width, total_height), 'gray')
            y = 0
            for img in imgs:
                preview_img.paste(img, (0, y))
                y += img.height
            
            info = f"📐 Layout: {len(imgs)} images vertically\n"
            info += f"📏 Output Dimensions: {max_width} x {total_height} pixels\n"
            info += f"🖱️ Use scrollbars to view full image\n"
            info += f"💡 Hold Shift + Scroll for horizontal scrolling"
        
        return preview_img, info
    
    def update_output_preview(self):
        """Update the output preview display with zoom support"""
        if not self.images:
            self.output_preview_label.configure(text="Add images to see preview", image="")
            self.preview_info_label.configure(text="")
            self.output_fullscreen_btn.configure(state=tk.DISABLED)
            return
        
        try:
            self.update_status("Generating preview...")
            self.root.update()
            
            preview_img, info = self.generate_output_preview()
            
            if preview_img:
                self.current_output_image = preview_img
                
                # Apply zoom level
                zoom_level = self.output_zoom.get()
                if zoom_level != 100:
                    display_img = self.apply_zoom_to_image(preview_img, zoom_level)
                    self.output_zoom_label.configure(text=f"{int(zoom_level)}%")
                else:
                    display_img = self.fit_image_to_canvas(preview_img, self.output_canvas)
                    self.output_zoom_label.configure(text="Fit")
                
                photo = ImageTk.PhotoImage(display_img)
                self.current_output_preview = photo
                self.preview_images.append(photo)
                
                self.output_preview_label.configure(image=photo, text="", compound=tk.TOP)
                self.output_preview_label.image = photo
                
                # Add info about scaling
                if display_img.size != preview_img.size:
                    info += f"\n📐 Display: {display_img.size[0]} x {display_img.size[1]} pixels (original {preview_img.size[0]} x {preview_img.size[1]})"
                info += f"\n🔍 Zoom: {int(zoom_level)}% | Use buttons or Ctrl+Scroll to zoom"
                self.preview_info_label.configure(text=info)
                
                # Enable full screen button
                self.output_fullscreen_btn.configure(state=tk.NORMAL)
                
                # Force update to calculate proper size
                self.output_image_frame.update_idletasks()
                
                # Update scroll region after the frame size is known
                self.output_canvas.configure(scrollregion=self.output_canvas.bbox("all"))
                
                # Also update canvas window width
                canvas_width = self.output_canvas.winfo_width()
                if canvas_width > 1:
                    self.output_canvas.itemconfig(self.output_canvas_window, width=canvas_width)
                
                self.update_status(f"Preview updated - Output size: {preview_img.size[0]}x{preview_img.size[1]} pixels")
            
        except Exception as e:
            self.output_preview_label.configure(text=f"Error generating preview:\n{str(e)}", image="")
            self.update_status("Error generating preview")
    
    def update_size_info(self):
        """Update the size information display"""
        if not self.images:
            self.size_info_label.configure(text="No images loaded")
            return
        
        try:
            original_size, total_pixels, output_size = self.calculate_total_size_info()
            
            info = f"📊 Total Original Size: {original_size}\n"
            info += f"🎨 Total Pixels: {total_pixels}\n"
            info += f"💾 Estimated Output Size: {output_size} (JPEG)"
            
            self.size_info_label.configure(text=info)
            
        except Exception as e:
            self.size_info_label.configure(text=f"Error calculating sizes: {str(e)}")
    
    # ==================== COMBINE FUNCTION ====================
    
    def combine_images(self):
        """Combine images and save the result"""
        if not self.images:
            return None
        
        imgs = [Image.open(f) for f in self.images]
        direction = self.direction.get()
        
        if direction == 'horizontal':
            total_width = sum(i.width for i in imgs)
            max_height = max(i.height for i in imgs)
            new_img = Image.new('RGB', (total_width, max_height))
            x = 0
            for img in imgs:
                new_img.paste(img, (x, 0))
                x += img.width
        else:
            max_width = max(i.width for i in imgs)
            total_height = sum(i.height for i in imgs)
            new_img = Image.new('RGB', (max_width, total_height))
            y = 0
            for img in imgs:
                new_img.paste(img, (0, y))
                y += img.height
        
        return new_img
    
    def save_combined_image(self, image):
        """Save the combined image"""
        output_file = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[
                ("JPEG files", "*.jpg"),
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ]
        )
        
        if output_file:
            try:
                if output_file.lower().endswith('.jpg') or output_file.lower().endswith('.jpeg'):
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    image.save(output_file, 'JPEG', quality=95)
                elif output_file.lower().endswith('.png'):
                    image.save(output_file, 'PNG')
                else:
                    image = image.convert('RGB')
                    image.save(output_file, 'JPEG')
                
                return True, output_file
            except Exception as e:
                return False, str(e)
        
        return None, None
    
    # ==================== EVENT HANDLERS ====================
    
    def on_add_images(self):
        """Handle add images button click"""
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.JPG *.JPEG *.PNG")]
        )
        
        added = 0
        for f in files:
            if f not in self.images:
                self.images.append(f)
                if self.add_image_to_list(f):
                    added += 1
        
        if added > 0:
            self.update_status(f"Added {added} images. Total: {len(self.images)}")
            self.update_size_info()
            self.update_output_preview()
    
    def on_remove_selected(self):
        """Handle remove selected button click"""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            self.images.pop(index)
            self.listbox.delete(index)
            self.update_status(f"Removed image. Total: {len(self.images)}")
            self.update_size_info()
            
            if not self.images:
                self.clear_previews()
            else:
                self.update_output_preview()
        else:
            messagebox.showinfo("No Selection", "Please select an image to remove")
    
    def on_clear_all(self):
        """Handle clear all button click"""
        if self.images and messagebox.askyesno("Confirm", "Clear all images?"):
            self.images = []
            self.listbox.delete(0, tk.END)
            self.update_status("Cleared all images")
            self.update_size_info()
            self.clear_previews()
    
    def on_move_up(self):
        """Handle move up button click"""
        selection = self.listbox.curselection()
        if selection and selection[0] > 0:
            index = selection[0]
            self.images[index], self.images[index-1] = self.images[index-1], self.images[index]
            self.refresh_listbox()
            self.listbox.selection_set(index-1)
            self.update_status("Moved image up")
            self.update_size_info()
            self.update_output_preview()
            self.on_image_select(None)
    
    def on_move_down(self):
        """Handle move down button click"""
        selection = self.listbox.curselection()
        if selection and selection[0] < len(self.images) - 1:
            index = selection[0]
            self.images[index], self.images[index+1] = self.images[index+1], self.images[index]
            self.refresh_listbox()
            self.listbox.selection_set(index+1)
            self.update_status("Moved image down")
            self.update_size_info()
            self.update_output_preview()
            self.on_image_select(None)
    
    def on_image_select(self, event):
        """Handle image selection from listbox"""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            image_path = self.images[index]
            self.show_selected_preview(image_path)
    
    def on_direction_change(self):
        """Handle direction change"""
        self.update_output_preview()
    
    # ==================== ZOOM HANDLERS ====================
    
    def on_selected_zoom_in(self):
        """Zoom in on selected image"""
        current_zoom = self.selected_zoom.get()
        new_zoom = min(400, current_zoom + 10)
        self.selected_zoom.set(new_zoom)
        self.selected_zoom_label.configure(text=f"{int(new_zoom)}%")
        if hasattr(self, 'current_preview_path'):
            self.zoom_levels[self.current_preview_path] = new_zoom
            self.show_selected_preview(self.current_preview_path)
    
    def on_selected_zoom_out(self):
        """Zoom out on selected image"""
        current_zoom = self.selected_zoom.get()
        new_zoom = max(10, current_zoom - 10)
        self.selected_zoom.set(new_zoom)
        self.selected_zoom_label.configure(text=f"{int(new_zoom)}%")
        if hasattr(self, 'current_preview_path'):
            self.zoom_levels[self.current_preview_path] = new_zoom
            self.show_selected_preview(self.current_preview_path)
    
    def on_selected_set_zoom_fit(self):
        """Set selected image to fit mode"""
        self.selected_zoom.set(100.0)
        self.selected_zoom_label.configure(text="Fit")
        if hasattr(self, 'current_preview_path'):
            self.zoom_levels[self.current_preview_path] = 100.0
            self.show_selected_preview_fit(self.current_preview_path)
    
    def on_selected_set_zoom_100(self):
        """Set selected image to 100% zoom"""
        self.selected_zoom.set(100.0)
        self.selected_zoom_label.configure(text="100%")
        if hasattr(self, 'current_preview_path'):
            self.zoom_levels[self.current_preview_path] = 100.0
            self.show_selected_preview(self.current_preview_path)
    
    def on_output_zoom_in(self):
        """Zoom in on output preview"""
        current_zoom = self.output_zoom.get()
        new_zoom = min(400, current_zoom + 10)
        self.output_zoom.set(new_zoom)
        self.output_zoom_label.configure(text=f"{int(new_zoom)}%")
        if hasattr(self, 'current_output_image'):
            self.update_output_preview()
    
    def on_output_zoom_out(self):
        """Zoom out on output preview"""
        current_zoom = self.output_zoom.get()
        new_zoom = max(10, current_zoom - 10)
        self.output_zoom.set(new_zoom)
        self.output_zoom_label.configure(text=f"{int(new_zoom)}%")
        if hasattr(self, 'current_output_image'):
            self.update_output_preview()
    
    def on_output_set_zoom_fit(self):
        """Set output preview to fit mode"""
        self.output_zoom.set(100.0)
        self.output_zoom_label.configure(text="Fit")
        self.update_output_preview()
    
    def on_output_set_zoom_100(self):
        """Set output preview to 100% zoom"""
        self.output_zoom.set(100.0)
        self.output_zoom_label.configure(text="100%")
        self.update_output_preview()
    
    def on_combine_images(self):
        """Handle combine button click"""
        if not self.images:
            messagebox.showwarning("No Images", "Please add images first!")
            return
        
        try:
            self.update_status("Processing images...")
            self.root.update()
            
            combined_image = self.combine_images()
            
            if combined_image:
                result, output = self.save_combined_image(combined_image)
                
                if result is True:
                    self.update_status(f"Successfully combined {len(self.images)} images!")
                    messagebox.showinfo("Success", f"Combined image saved as:\n{output}")
                elif result is False:
                    messagebox.showerror("Error", f"Error saving image:\n{output}")
                else:
                    self.update_status("Save cancelled")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error processing images:\n{str(e)}")
            self.update_status("Error occurred")
    
    # ==================== UTILITY FUNCTIONS ====================
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)
        self.root.update()
    
    def clear_previews(self):
        """Clear all preview displays"""
        self.selected_preview_label.configure(text="Select an image from the list", image="")
        self.output_preview_label.configure(text="Add images to see preview", image="")
        self.preview_info_label.configure(text="")
        self.size_info_label.configure(text="No images loaded")
        self.file_info_label.configure(text="Select an image to see details")
        self.selected_fullscreen_btn.configure(state=tk.DISABLED)
        self.output_fullscreen_btn.configure(state=tk.DISABLED)
        # Reset zoom
        self.selected_zoom.set(100.0)
        self.output_zoom.set(100.0)
        self.selected_zoom_label.configure(text="Fit")
        self.output_zoom_label.configure(text="Fit")
        self.zoom_levels.clear()

# ==================== MAIN APPLICATION FUNCTIONS ====================

def gui_mode():
    """Launch GUI version"""
    root = tk.Tk()
    app = ImageCombinerGUI(root)
    root.mainloop()

def cli_mode():
    """Original CLI version"""
    parser = argparse.ArgumentParser(description='Combine images horizontally or vertically')
    parser.add_argument('-v', '--vertical', action='store_true', 
                       help='Combine vertically (default is horizontal)')
    parser.add_argument('-o', '--output', type=str, default=None,
                       help='Output filename (default: combined_[direction].jpg)')
    parser.add_argument('--format', type=str, default='JPEG',
                       help='Output format (JPEG, PNG, etc.)')
    parser.add_argument('-g', '--gui', action='store_true',
                       help='Launch GUI mode')
    args = parser.parse_args()
    
    # Launch GUI if requested
    if args.gui:
        gui_mode()
        return 0
    
    # Otherwise run CLI version
    direction = 'vertical' if args.vertical else 'horizontal'
    
    patterns = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']
    images = []
    for pattern in patterns:
        images.extend([f for f in glob.glob(f'./{pattern}') 
                      if 'combined' not in f.lower()])
    
    images = sorted(list(set(images)))
    
    if not images:
        print("No images found!")
        return 1
    
    try:
        imgs = [Image.open(f) for f in images]
        
        if direction == 'horizontal':
            total_width = sum(i.width for i in imgs)
            max_height = max(i.height for i in imgs)
            new_img = Image.new('RGB', (total_width, max_height))
            x = 0
            for img in imgs:
                new_img.paste(img, (x, 0))
                x += img.width
        else:
            max_width = max(i.width for i in imgs)
            total_height = sum(i.height for i in imgs)
            new_img = Image.new('RGB', (max_width, total_height))
            y = 0
            for img in imgs:
                new_img.paste(img, (0, y))
                y += img.height
        
        if args.output:
            output_file = args.output
        else:
            output_file = f'combined_{direction}.{args.format.lower()}'
        
        if args.format.upper() == 'JPEG' and new_img.mode != 'RGB':
            new_img = new_img.convert('RGB')
        
        new_img.save(output_file, format=args.format.upper())
        print(f"Successfully combined {len(images)} images {direction}ly!")
        print(f"Output saved as: {output_file}")
        
    except Exception as e:
        print(f"Error processing images: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(cli_mode())