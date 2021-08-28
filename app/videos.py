import youtube_dl
from moviepy.editor import VideoFileClip


class VideoFromYoutubeURL:  # Use 'H6R9gbClEg' for search
    """

    __init__ argumnts:
    ----short_link - link like 'https://www.youtube.com/watch?v=2WemzwuAQF4'
                     or only video id ('2WemzwuAQF4')

    """

    def __init__(self, video_id):
        self.video_id = get_id(video_id)
        self.stream_url = None
        self.video = None
        self.start_downloading_webm()
        self.last_asked_time = 0

    # @in_new_thread
    def start_downloading_webm(self, attempts=10):
        self.video = None

        self.stream_url = get_best_stream_link(self.video_id)["url"]
        print("1/2", self.stream_url)
        self.video = VideoFileClip(self.stream_url)
        self.video.get_frame(0)
        print("1")

    def get_sound_and_frame(self, t):
        if not self.get_is_downloaded():
            return [], []
        return self._get_sound(t), self._get_frame(t)

    def _get_frame(self, t, waiting_time=100):
        return self.video.get_frame(t)

    def _get_sound(self, t):
        if t >= self.last_asked_time:
            return []
        self.video.audio.subclip(self.last_asked_time, t).to_soundarray()
        self.last_asked_time = t

    def get_is_downloaded(self):
        return bool(self.video)

    def wait_until_downloaded(self):
        while not self.get_is_downloaded():
            pass


def get_id(url):
    if not url.startswith("http"):
        return url

    from urllib.parse import urlparse, parse_qs
    """
    tooked from
    https://stackoverflow.com/questions/45579306/get-youtube-video-url-or-youtube-video-id-from-a-string-using-regex
    look it for more info
    """
    u_pars = urlparse(url)
    quer_v = parse_qs(u_pars.query).get('v')
    if quer_v:
        return quer_v[0]
    pth = u_pars.path.split('/')
    if pth:
        return pth[-1]


def get_best_stream_link(url):
    with youtube_dl.YoutubeDL({}) as ydl:
        meta = ydl.extract_info(url, download=False)
        formats = meta.get('formats', [meta])
        available_formats = [f for f in formats if f["acodec"] != "none"]
        for f in available_formats:
            print(f["acodec"])
        return max(available_formats, key=lambda elem: elem["quality"])
 
