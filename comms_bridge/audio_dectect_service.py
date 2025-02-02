import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import librosa
import csv


class AudioDectect:
    yamnet_model = hub.load('https://tfhub.dev/google/yamnet/1')


    def preprocess_audio(self,file_path):
        waveform, sample_rate = librosa.load(file_path, sr=16000)  # Resample to 16 kHz
        return tf.convert_to_tensor(waveform, dtype=tf.float32)

    def load_class_map(self,file_path):
        class_names = []
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                class_names.append(row['display_name'])
        return class_names

    def identify_sound(self,audio_file, class_map_file):
        class_names = self.load_class_map(class_map_file)
        waveform = self.preprocess_audio(audio_file)
        scores, embeddings, spectrogram = self.yamnet_model(waveform)
        mean_scores = scores.numpy().mean(axis=0)
        top_class_index = np.argmax(mean_scores)
        predicted_class = class_names[top_class_index]
        return predicted_class




