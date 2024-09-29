import csv
import os
import struct
import wave
from dataclasses import dataclass

from pvrecorder import PvRecorder


@dataclass
class Sentence:
    console_format: str
    file_name_format: str


def load_sentences(path):
    with open(path, newline='') as csvfile:
        lines = csv.reader(csvfile, delimiter=',', quotechar='"')
        return list(map(lambda x: Sentence(x[0], x[1]), lines))


def choose_devices():
    index = 0
    for index, device in enumerate(PvRecorder.get_audio_devices()):
        print(f"[{index + 1}] {device}")

    selection = (input('Select inputs (enter for all): '))

    if not selection:
        selection = ''.join(list(map(lambda x: str(x), range(1, index + 2))))

    return list(map(lambda x: int(x) - 1, [*selection]))


def create_recorders(device_indices, frame_length, buffer_size_ms):
    return list(map(lambda x: PvRecorder(device_index=x, frame_length=frame_length, buffer_size_msec=buffer_size_ms),
                    device_indices))


def save_recording(audio, output_dir, device_dir, repetition_index, file_name, frame_length):
    path = '{0}/{1}/{2}_{3}.wav'.format(output_dir, device_dir, file_name, repetition_index)
    with wave.open(path, 'w') as output:
        output.setparams((1, 2, 16000, frame_length, "NONE", "NONE"))
        output.writeframes(struct.pack("h" * len(audio), *audio))


def create_working_dirs(root_output_path, recorders):
    if not os.path.isdir(root_output_path):
        os.mkdir(root_output_path)

    for recorder in recorders:
        path = '{0}/{1}'.format(root_output_path, recorder.selected_device)
        if not os.path.isdir(path):
            os.mkdir(path)