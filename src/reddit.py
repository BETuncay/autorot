## Reddit API
#
import json
import praw


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

# rework
def get_reddit_story():
    with open('reddit_secrets.json') as f:
            data = json.load(f)

    # Initialize Reddit client
    reddit = praw.Reddit(
        client_id=data["id"],
        client_secret=data["secret"],
        username=data["username"],
        password=data["password"],
        user_agent=data["agent"],
    )

    # Choose a subreddit
    subreddit = reddit.subreddit("wallstreetbets")  # change this to any subreddit

    text = []
    # Fetch top 5 posts from the subreddit
    for post in subreddit.hot(limit=5):
        print(f"\nPost: {post.title}\n{'='*50}")

        # Load top-level comments
        post.comments.replace_more(limit=0)  # avoids "load more comments"
        for i, comment in enumerate(post.comments[:3]):  # limit to top 3 comments
            print(f"{comment.body}\n")
            text.append(comment.body)
    return text