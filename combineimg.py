from PIL import Image
import glob
import sys
import os
import argparse

def main():
    # Better argument handling with argparse
    parser = argparse.ArgumentParser(description='Combine images horizontally or vertically')
    parser.add_argument('-v', '--vertical', action='store_true', 
                       help='Combine vertically (default is horizontal)')
    parser.add_argument('-o', '--output', type=str, default=None,
                       help='Output filename (default: combined_[direction].jpg)')
    parser.add_argument('--format', type=str, default='JPEG',
                       help='Output format (JPEG, PNG, etc.)')
    args = parser.parse_args()
    
    direction = 'vertical' if args.vertical else 'horizontal'
    
    # More comprehensive image pattern matching
    patterns = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']
    images = []
    for pattern in patterns:
        images.extend([f for f in glob.glob(f'./{pattern}') 
                      if 'combined' not in f.lower()])
    
    # Remove duplicates and sort for consistent ordering
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
        
        # Handle output filename
        if args.output:
            output_file = args.output
        else:
            output_file = f'combined_{direction}.{args.format.lower()}'
        
        # Save with appropriate format
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
    sys.exit(main())