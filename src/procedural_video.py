## create procedural videos
# rewrite this
#
import numpy as np
import matplotlib.pyplot as plt
from moviepy import ImageSequenceClip
from moviepy import VideoClip
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


# Parameters
width, height = 800, 800
duration = 30  # seconds
fps = 30
frames = duration * fps
c = complex(-0.8, 0.156)  # Julia set constant


# Export as video
def export_video(frame_paths, output="l_system.mp4", fps=30):
    clip = ImageSequenceClip(frame_paths, fps=fps)
    clip.write_videofile(output, codec='libx264', bitrate='4000k')


# Julia Set function
def julia_set(xmin, xmax, ymin, ymax, width, height, c, max_iter=256):
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    img = np.zeros(Z.shape, dtype=int)

    for i in range(max_iter):
        Z = Z**2 + c
        mask = (np.abs(Z) < 10)
        img += mask

    return img


# Generate video
def make_video():
    fig, ax = plt.subplots(figsize=(8, 8), dpi=100)
    canvas = FigureCanvas(fig)
    plt.axis('off')
    def make_frame(t):
        zoom = 1.5 * (0.98 ** (t * fps))
        xmin, xmax = -zoom, zoom
        ymin, ymax = -zoom, zoom

        ax.clear()
        ax.axis('off')
        img = julia_set(xmin, xmax, ymin, ymax, width, height, c)
        ax.imshow(img, cmap='hot', extent=[xmin, xmax, ymin, ymax])

        canvas.draw()
        buf = canvas.buffer_rgba()
        image = np.asarray(buf)
        return image[:, :, :3]  # Drop alpha channel for RGB
    
    animation = VideoClip(make_frame, duration=duration)
    animation.write_videofile("julia_zoom.mp4", fps=fps)