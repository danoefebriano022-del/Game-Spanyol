import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random

duration = 5  # durasi rekaman dalam detik
sample_rate = 44100

recognizer = sr.Recognizer()

words_by_level = {
  "mudah": ["kucing", "anjing", "apel", "susu", "matahari"],
  "sedang": ["pisang", "sekolah", "teman", "jendela", "kuning"],
  "sulit": ["teknologi", "universitas", "informasi", "pengucapan", "imajinasi"]
}

print("Selamat datang di Game Bahasa Spanyol!")
print("Kamu akan diminta untuk merekam kata-kata random dalam bahasa Indonesia yang harus kamu terjemahkan ke dalam bahasa Spanyol. Semaking tinggi levelnya, semakin sulit kata-katanya.")
print("Kamu memiliki 3 nyawa dalam game ini, kalau kamu menjawab salah ❤️ ❤️ ❤️ , nyawa kamu berkurang 1. ➖")
print("Kamu bisa keluar dari game ini dengan mengetik 'exit'. ➜]")
print("Ayo mulai bermain! 🎉")

point = 0
health = 3

while True:
    print("\nPilih level kesulitan: (mudah🟢/sedang🟡/sulit🔴)")
    level = input(">>>")
    if level =='exit':
        print("⭐️ Point akhir kamu adalah:", point)
        print("🙏 Terima kasih telah bermain! Sampai jumpa lagi!")
        break
    word = random.choice(words_by_level.get(level, words_by_level["mudah"]))
    print(f"Ucapankan kata berikut dalam bahasa Spanyol: {word}")
    
    print("\nSilakan berbicara sekarang... 🎧")
    recording = sd.rec(
        int(duration * sample_rate),  # jumlah contoh rekaman
        samplerate=sample_rate,       # sample rate
        channels=1,                   # 1 berarti rekaman tunggal
        dtype="int16")              # tipe data untuk contoh rekaman
    sd.wait()  # menunggu rekaman selesai

    wav.write("output.wav", sample_rate, recording)
    print("Rekaman selesai, memulai pengenalan suara... 🔊")

    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="es-ES").lower().strip()
        print("Kamu mengatakan:", text)
        translator = Translator()
        translated = translator.translate(word, src="id", dest="es").text.lower().strip()
        print(f"Terjemahan ke Bahasa Spanyol:", translated)
        
        if translated == text:
            print("Selamat! Jawaban kamu benar! ✅")
            point = point + 1
            print(f"Skor kamu saat ini: {point}")
        else:
            health -= 1
            print(f"Maaf, jawaban kamu salah. ❌ Coba lagi! Nyawa kamu: {health}")
            if health == 0:
                print("Game Over! 😢")
                print("⭐️ Point akhir kamu adalah:", point)
                print("🙏 Terima kasih telah bermain! Sampai jumpa lagi!")
                break
    except sr.UnknownValueError:
        print("Suara tidak dapat dikenali")
    except sr.RequestError as e:
        print(f"Service error: {e}")
    