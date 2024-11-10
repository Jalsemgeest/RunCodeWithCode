import sys
from pytube import YouTube
from pytube.innertube import _default_clients

_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]
YouTube(sys.argv[1]).streams.first().download("C:/Users/cptli/Desktop")