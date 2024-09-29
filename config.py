from dataclasses import dataclass


# todo move this into a file
@dataclass
class Config:
    frame_length: int = 512
    buffer_size_msec: int = 100
    sentences_path: str = 'recenice.csv'
    output_dir: str = 'output'
    repeat_sentences: bool = True
    repeat_sentences_count: int = 5
    shuffle_sentences: bool = True



