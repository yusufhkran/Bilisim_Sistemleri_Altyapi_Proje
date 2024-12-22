#!/bin/bash
import json  # JSON formatında veri işlemek için
from datetime import datetime  # Olay zamanını almak için
from watchdog.observers import Observer  # Dosya sistemi değişikliklerini izlemek için
from watchdog.events import FileSystemEventHandler  # Olay işleyicisi sınıfı

# İzlenecek sabit dizin ve log dosyası
WATCHED_DIRECTORY = "/home/yusufhkran/bsm/test"  # İzlenecek dizinin yolu
LOG_FILE = "/home/yusufhkran/bsm/logs/changes_logs.json"  # Olayların kaydedileceği dosya

# Olayları işlemek için bir sınıf tanımlanır
class FileEventHandler(FileSystemEventHandler):
    def log_event(self, event_type, file_path):
        # Olay bilgilerini JSON formatında kaydet
        log_entry = {
            "timestamp": datetime.now().isoformat(),  # Olayın gerçekleştiği zaman
            "event_type": event_type,  # Olay türü (created, deleted, modified, moved)
            "file_path": file_path  # Etkilenen dosyanın yolu
        }
        # JSON verisini log dosyasına ekle
        with open(LOG_FILE, "a") as log_file:
            log_file.write(json.dumps(log_entry) + "\n")  # Her olayı yeni satır olarak ekle

    # Yeni bir dosya oluşturulduğunda tetiklenir
    def on_created(self, event):
        if not event.is_directory:  # Sadece dosyalar için işlem yap
            self.log_event("created", event.src_path)  # Olay türü "created" olarak loglanır

    # Bir dosya silindiğinde tetiklenir
    def on_deleted(self, event):
        if not event.is_directory:  # Sadece dosyalar için işlem yap
            self.log_event("deleted", event.src_path)  # Olay türü "deleted" olarak loglanır

    # Mevcut bir dosya değiştirildiğinde tetiklenir
    def on_modified(self, event):
        if not event.is_directory:  # Sadece dosyalar için işlem yap
            self.log_event("modified", event.src_path)  # Olay türü "modified" olarak loglanır

    # Bir dosya taşındığında tetiklenir
    def on_moved(self, event):
        if not event.is_directory:  # Sadece dosyalar için işlem yap
            self.log_event("moved", {"from": event.src_path, "to": event.dest_path})  # Kaynak ve hedef yolu logla

# Servis başlatma işlevi
def start_watching():
    observer = Observer()  # Bir gözlemci (observer) oluştur
    event_handler = FileEventHandler()  # Olayları işlemek için bir işleyici oluştur
    observer.schedule(event_handler, WATCHED_DIRECTORY, recursive=False)  # İşleyiciyi belirtilen dizine ata
    observer.start()  # İzlemeye başla
    print(f"Watching directory: {WATCHED_DIRECTORY}")  # İzlenen dizini terminale yazdır

    try:
        observer.join()  # İzlemeyi devam ettir (kesintisiz çalışmayı sağlar)
    except KeyboardInterrupt:
        observer.stop()  # Kullanıcı `Ctrl+C` yaparsa izlemeyi durdur
        print("Stopped watching.")  # İzleme durduruldu mesajı yazdır

# Ana çalışma bloğu
if __name__ == "__main__":
    import os  # Dosya ve dizin işlemleri için
    if not os.path.exists(WATCHED_DIRECTORY):  # İzlenecek dizin mevcut mu kontrol et
        print(f"The directory {WATCHED_DIRECTORY} does not exist. Please create it.")  # Hata mesajı yazdır
    else:
        start_watching()  # Servisi başlat
