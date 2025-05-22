import numpy as np
import matplotlib.pyplot as plt


import os
import glob

import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError, Error

import torch
from TTS.api import TTS

from moviepy import ImageSequenceClip
from moviepy import VideoClip
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


RANDOM_TEXT = """ I've held this in long enough. The shame, guilt, lies. Pretending to be cool and knowing what the fuck I'm talking about. I've been holding this in for years. I've cried and cried and cried. I'm fed up with my bitch behavior. It's time to fucking take things into my own hands and change. I'm not stopping, I'm going to gain this all back the slow, and right way. Here's my story.

In 2019 I learned about the stock market. Like a responsible retail investor, I created baskets and diversified my equity investments.

In 2020, I learned about options.

My first gamble was a meme stock I found on WSB that rhymes with Ped Pad Peyon. That was the start of my entire $1M loss and life downfall.

It felt so good to see those big spikes in gains.

But it also felt like the end of the world when it all went to $0.

For some reason, I always came back. I tasted the forbidden fruit, and was addicted.

Fast forward two years, I needed a source for more trading capital - I sold my house and car, maxed out credit cards, borrowed from the bank, and lenders. I lied to family/friends to get money, and worked odd jobs that were shameful.

My wife who I'd been with for 12 years left me, we didn't sign a prenup so there was that whole process...then she took custody of the kids.

Sure, I lost $1,030,220.81. But the worst part of it all, is I lost loved ones, every friend in my life, and every single asset I owned. I cried like a fucking bitch for days on end, slept on benches, backyards, and under bridges.

I managed to save up some money, and am now living on my own, in a one-bedroom apartment.

I know it I can do this. I know I can make it all back. I've heard stories and seen people do it. I understand all the technical analysis, indicators, price action, gamma exposure, OI, risk-free interest, blah blah fucking blah. I know it all. What made me lose it all wasn't my understanding of the markets, it was my ego, my greed, and lack of discipline. My psyche.

I've spent the last 2 yrs dedicating myself to mastering every technical aspect of the market. I've met 10 figure retail investors, hedgefund managers, and everyone in between. Really dedicated myself to learning the markets. Most importantly, I've made good progress mastering my emotions. I've even gone on months without masturbating. I needed to model a stimulus that was just as rewarding as gambling.

I'm here to show that I can gradually get out of this hell-hole.

I've managed to trade back up to $25k, and in the last week I made $14k (options + futures). I will get back to $1M. I'm just here to prove to the world and myself that this isn't over.

Is it the most hedged / low risk decision? Fuck no. The degen surely lives on inside me. But I've tamed it. I guess if you're looking for entertainment, or a person to root for, you can find me on X. Username is lost1million. I'll try to give periodic updates here as well.

This is pretty much it for me. Here we go.

P.S. Please don't report me to the suicide prevention. While I appreciate the sympathy, the messages I get are quite annoying. I will be fine. I am fine. """


# L-system generation
def apply_rules(ch):
    rules = {
        "F": "FF+[+F-F-F]-[-F+F+F]"
    }
    return rules.get(ch, ch)

def generate_l_system(iterations, axiom):
    current = axiom
    for _ in range(iterations):
        current = "".join(apply_rules(c) for c in current)
    return current

# Drawing and frame capture
def draw_l_system(instructions, angle=25, step=5):
    stack = []
    x, y = 0, 0
    heading = 90
    positions = [(x, y)]

    frames = []
    for idx, cmd in enumerate(instructions):
        if cmd == 'F':
            rad = np.deg2rad(heading)
            x += step * np.cos(rad)
            y += step * np.sin(rad)
            positions.append((x, y))
        elif cmd == '+':
            heading -= angle
        elif cmd == '-':
            heading += angle
        elif cmd == '[':
            stack.append((x, y, heading))
        elif cmd == ']':
            x, y, heading = stack.pop()
            positions.append((x, y))  # move without drawing

        # Capture frame every N steps
        if idx % 10 == 0:
            fig, ax = plt.subplots(figsize=(6, 8))
            ax.plot(*zip(*positions), color='green')
            ax.axis('off')
            plt.tight_layout()
            frame_path = f'frames/frame_{idx:04d}.png'
            fig.savefig(frame_path)
            plt.close()
            frames.append(frame_path)

    return frames

# Export as video
def export_video(frame_paths, output="l_system.mp4", fps=30):
    clip = ImageSequenceClip(frame_paths, fps=fps)
    clip.write_videofile(output, codec='libx264', bitrate='4000k')


def load__images(root: str) -> list[str]:
    return glob.glob(os.path.join(root, "*.png"))


# Scopes for full upload access

def upload_video(video_file, title, description, category_id="22", privacy_status="public"):
    SCOPES = ["https://www.googleapis.com/auth/youtube"]

    # Authenticate and get credentials
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_secrets.json", SCOPES)
    
    credentials = flow.run_local_server(host='localhost',
        port=8080, 
        authorization_prompt_message='Please visit this URL: {url}', 
        success_message='The auth flow is complete; you may close this window.',
        open_browser=True)
    
    # Build the API client
    with googleapiclient.discovery.build("youtube", "v3", credentials=credentials) as youtube:
        request_body = {
            "snippet": {
                "title": title,
                "description": description,
                "categoryId": category_id
            },
            "status": {
                "privacyStatus": privacy_status
            }
        }

        # Attach the video file
        media_file = MediaFileUpload(video_file, resumable=True)

        # Upload
        request = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media_file
        )
        
        try:
            response = request.execute()
        except HttpError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))

        print(f"✅ Upload successful! Video URL: https://youtu.be/{response['id']}")




# Parameters
width, height = 800, 800
duration = 30  # seconds
fps = 30
frames = duration * fps
c = complex(-0.8, 0.156)  # Julia set constant

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


# Run
def main():
    #os.makedirs("frames", exist_ok=True)
    #axiom = "F"
    #instructions = generate_l_system(5, axiom)
    #frame_paths = draw_l_system(instructions)
    #frame_paths = load__images("frames")

    #export_video(frame_paths)

    # Clean up
    #for f in frame_paths:
    #    os.remove(f)
    #os.rmdir("frames")

    
    title = "awesome-vid"
    description = "lars my dearly beloved"
    video_file = "julia_zoom.mp4"
    privacy_status = "unlisted"  # or "public" or "private"


    # Generate video
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

    upload_video(
        video_file=video_file,
        title=title,
        description=description,
        privacy_status=privacy_status
    )

    device = "cuda" if torch.cuda.is_available() else "cpu"

    # List available 🐸TTS models
    print(TTS().list_models())

    # Init TTS
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    # Init TTS with the target model name
    #tts = TTS(model_name="tts_models/de/thorsten/tacotron2-DDC", progress_bar=True).to(device)

    # Run TTS
    tts.tts_to_file(text="Ich bin eine Testnachricht.", file_path="output.wav")

    # Example voice cloning with YourTTS in English, French and Portuguese
    tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False).to(device)
    tts.tts_to_file("This is voice cloning.", speaker_wav="my/cloning/audio.wav", language="en", file_path="output.wav")
    tts.tts_to_file("C'est le clonage de la voix.", speaker_wav="my/cloning/audio.wav", language="fr-fr", file_path="output.wav")
    tts.tts_to_file("Isso é clonagem de voz.", speaker_wav="my/cloning/audio.wav", language="pt-br", file_path="output.wav")


if __name__ == "__main__":
    main()
