import os
import re
import shutil

# Paths
posts_dir = r"D:\Trabalho\obsidian_vaults\vault\posts"
attachments_dir = r"D:\Trabalho\obsidian_vaults\vault\Attachments"
hugo_posts_dir = r"D:\Trabalho\MyBlogStufs\matosdatascience\content\posts"  # New directpry for Hugo
static_images_dir = r"D:\Trabalho\MyBlogStufs\matosdatascience\static\images"

# Create if not exists
for dir_path in [hugo_posts_dir, static_images_dir]:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

# Process every mardown file
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        # Read original file from Obsidian
        source_path = os.path.join(posts_dir, filename)
        with open(source_path, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Find and process images
        images = re.findall(r'\[\[([^]]*\.png)\]\]', content)
        
        # Make hugo on each one
        hugo_content = content
        for image in images:
            # Replace links only for Hugo's one
            markdown_image = f"![Image Description](/images/{image.replace(' ', '%20')})"
            hugo_content = hugo_content.replace(f"[[{image}]]", markdown_image)
            
            # Copy image for static on Hugo
            image_source = os.path.join(attachments_dir, image)
            if os.path.exists(image_source):
                shutil.copy(image_source, static_images_dir)
        
        # Save in the hupo dir
        hugo_path = os.path.join(hugo_posts_dir, filename)
        with open(hugo_path, "w", encoding="utf-8") as file:
            file.write(hugo_content)

print("Files processed end copy!")