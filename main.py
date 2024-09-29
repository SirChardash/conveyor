import random

import helper
from config import Config

config = Config()

sentences = helper.load_sentences(config.sentences_path)
recorders = helper.create_recorders(helper.choose_devices(), config.frame_length, config.buffer_size_msec)
helper.create_working_dirs(config.output_dir, recorders)

repeat_count = config.repeat_sentences_count if config.repeat_sentences else 1

for i in range(0, repeat_count):
    # shuffle sentences between each cycle if needed
    if config.shuffle_sentences:
        random.shuffle(sentences)
    # iterate through all sentences
    for sentence in sentences:
        print(sentence.console_format)
        # record current sentence in an audio stream for each recorder
        audios = dict(map(lambda x: (x, []), recorders))
        try:
            for recorder in recorders:
                recorder.start()
            while True:
                frames = dict(map(lambda x: (x, x.read()), recorders))
                for recorder in recorders:
                    audios[recorder].extend(frames[recorder])
        except KeyboardInterrupt:
            # save current recording and move over to next sentence
            for recorder in recorders:
                recorder.stop()
            for recorder in recorders:
                helper.save_recording(audios[recorder], config.output_dir, recorder.selected_device, i + 1,
                                      sentence.file_name_format, config.frame_length)
