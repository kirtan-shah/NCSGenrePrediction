#!/opt/homebrew/bin/python3.9
import matplotlib
import librosa
matplotlib.use('Agg') # no display
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from tempfile import mktemp
import os
import tqdm
import warnings
import multiprocessing
import tracemalloc
import gc
import math
import sys

dirpath = "../NCSDownload/songs"
files = [os.path.join(dirpath, f) for f in os.listdir(dirpath)]

def export_to_specgram(file):
    # tracemalloc.start()
    # audio_len = librosa.get_duration(filename=file)
    # duration = 30
    # start = (audio_len - duration) / 2

    y_whole, sr = librosa.load(file, mono=True) # offset=start, duration=duration)
    intervals = librosa.effects.split(y_whole, top_db=20)
    chunk_size = 8 * sr
    istart = intervals[0][0]
    iend = intervals[-1][1]
    y = y_whole[istart:iend]
    # for i in range(0, len(y_sec), chunk_size):
    #     b = i
    #     e = i + chunk_size
    #     if e > len(y_sec):
    #         b = len(y_sec) - chunk_size
    #         e = len(y_sec)
    #     y = y_sec[b:e]

    # spec = np.abs(librosa.stft(y, hop_length=512))
    # spec = librosa.amplitude_to_db(spec, ref=np.max)
    # librosa.display.specshow(spec, sr=sr, ax=ax, cmap='gray')
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
    # mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=16)
    # librosa.display.specshow(mfccs, sr=sr, ax=ax, cmap='gray')

    w, h = S.shape[1], S.shape[0]
    fig = plt.figure(figsize=(w, h))
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    plt.axis("off")
    ax.set_ylabel(None)
    ax.set_xlabel(None)

    librosa.display.specshow(librosa.power_to_db(S, ref=np.max), sr=sr, ax=ax, cmap='gray')

    # save plot to file
    song_only = os.path.splitext(os.path.basename(file))[0]
    if not os.path.isdir("specgrams"): # + song_only):
        os.makedirs("specgrams") # + song_only)
    fig.savefig('specgrams/' + song_only + '.png', dpi=1)
    fig.clear()
    plt.close(fig)

    del y, sr # mfccs, spec
    gc.collect()

    # snap1 = tracemalloc.take_snapshot()
    # top_stats = snap1.statistics('lineno')
    # print("[ Top 4 ]")
    # for stat in top_stats[:4]:
    #     print(stat)


def process_file(file):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            export_to_specgram(file)
        except Exception as e:
            print("Failed to process " + file, e, file=sys.stderr)

if __name__ == '__main__':
    if not os.path.isdir("specgrams"):
        os.makedirs("specgrams")
    pool = multiprocessing.Pool(processes=8)
    r = list(tqdm.tqdm(pool.imap(process_file, files), total=len(files)))
    # pool.map(process_file, files)


