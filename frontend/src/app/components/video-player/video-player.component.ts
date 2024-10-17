import { AfterViewInit, Component, ElementRef, Input, OnDestroy, ViewChild } from '@angular/core';
import videojs from 'video.js';
import Player from 'video.js/dist/types/player';
import 'videojs-contrib-quality-levels';
import 'videojs-http-source-selector';
import 'videojs-hls-quality-selector';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

interface CustomPlayer extends Player {
  hlsQualitySelector: (options?: any) => void;
}

@Component({
  selector: 'app-video-player',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './video-player.component.html',
  styleUrl: './video-player.component.scss'
})
export class VideoPlayerComponent implements AfterViewInit, OnDestroy {
  @ViewChild('targetVideo', { static: true }) target!: ElementRef;
  @Input() videoSrc!: string;
  @Input() videoId!: string;
  @Input() thumbnail!: string;
  player!: CustomPlayer;
  saveInterval: any;
  showResumeButton = false;
  savedTime = 0;

  constructor(private http: HttpClient) { }

  ngAfterViewInit() {
    if (!this.videoSrc || !this.videoId) return;

    // Initialisiere den Player
    this.player = videojs(this.target.nativeElement, {
      fluid: true,
      autoplay: false,
      controls: true,
      poster: this.thumbnail,
      sources: [{
        src: this.videoSrc,
        type: 'application/x-mpegURL'
      }]
    }) as CustomPlayer;

    // Verwende das hlsQualitySelector Plugin, wenn es verfügbar ist
    if (this.player.hlsQualitySelector) {
      this.player.hlsQualitySelector();
    }

    // Hole den gespeicherten Fortschritt
    this.http.get<any>(`/api/v1/get-progress/${this.videoId}`).subscribe(response => {
      this.savedTime = parseFloat(response.progress) || 0;
      if (this.savedTime > 0) {
        this.showResumeButton = true;  // Zeige den Resume-Button
        this.player.currentTime(this.savedTime);  // Setze die Video-Zeit auf die gespeicherte Position
      }
    });

    // Starte das Speichern des Fortschritts bei 'play'
    this.player.on('play', () => {
      this.startSaveProgressInterval();
    });

    // Stoppe das Speichern bei 'pause'
    this.player.on('pause', () => {
      this.stopSaveProgressInterval();
    });

    // Markiere das Video als gesehen bei 'ended'
    this.player.on('ended', () => {
      this.markAsSeen();
      this.stopSaveProgressInterval();
    });
  }

  markAsSeen() {
    // Setze den Status "vollständig gesehen" im Backend
    this.http.post('/api/v1/save-progress/', {
      video_slug: this.videoId,
      progress: this.player.duration(),
      seen: true
    }).subscribe(response => {
      console.log('Video vollständig gesehen:', response);
    });
  }

  startSaveProgressInterval() {
    if (this.saveInterval) return;

    this.saveInterval = setInterval(() => {
      const currentTime = this.player.currentTime();
      if (typeof currentTime === 'number') {
        this.saveProgress(currentTime);
      }
    }, 5000);
  }

  stopSaveProgressInterval() {
    if (this.saveInterval) {
      clearInterval(this.saveInterval);
      this.saveInterval = null;
    }
  }

  saveProgress(currentTime: number) {
    this.http.post('/api/v1/save-progress/', {
      video_slug: this.videoId,
      progress: currentTime
    }).subscribe(response => {
      console.log('Fortschritt gespeichert:', response);
    });
  }

  resumeVideo() {
    this.player.currentTime(this.savedTime);  // Setze die Video-Zeit auf die gespeicherte Position
    this.showResumeButton = false;  // Verberge den Button
    this.player.play();  // Starte das Video
  }

  ngOnDestroy() {
    if (this.player) {
      this.player.dispose();
    }
    if (this.saveInterval) {
      clearInterval(this.saveInterval);
    }
  }
}
