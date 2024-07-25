import os
from PIL import Image
from moviepy.editor import ImageSequenceClip
import numpy as np

def cut_images_in_half_vertical(input_folder, output_folder, standard_size):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    images = []
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img_path = os.path.join(input_folder, filename)
            img = Image.open(img_path).resize(standard_size)
            width, height = img.size
            left_half = img.crop((0, 0, width // 2, height))
            right_half = img.crop((width // 2, 0, width, height))

            left_path = os.path.join(output_folder, f"left_{filename}")
            right_path = os.path.join(output_folder, f"right_{filename}")

            left_half.save(left_path)
            right_half.save(right_path)

            images.append((left_path, right_path))

    return images

def create_pause_challenge_video(images, fixed_left_image, output_video, standard_size):
    left_image = Image.open(fixed_left_image).resize(standard_size)
    width, height = left_image.size
    frames = []

    for _, right_path in images:
        right_image = Image.open(right_path).resize(standard_size)
        combined = Image.new("RGB", (width * 2, height))
        combined.paste(left_image, (0, 0))
        combined.paste(right_image, (width, 0))
        frames.append(np.array(combined))

    frame_rate = 2  
    clip = ImageSequenceClip(
        [frame for frame in frames for _ in range(frame_rate)], fps=frame_rate)
    clip.write_videofile(output_video, codec="libx264")

def main():
    input_folder = "images"
    output_folder = "output/cut_images"
    output_video = "output/video.mp4"
    #Eixo x é metade do valor final pois as 2 metades serão somadas, fazendo assim com que o video seja 1080x1920
    standard_size = (540, 1920)
    images = cut_images_in_half_vertical(input_folder, output_folder, standard_size)

    fixed_left_image = images[0][0]

    create_pause_challenge_video(images, fixed_left_image, output_video, standard_size)


if __name__ == "__main__":
    main()
