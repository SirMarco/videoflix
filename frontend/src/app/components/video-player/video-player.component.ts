import { AfterViewInit, Component, ElementRef, Input, OnDestroy, ViewChild } from '@angular/core';
import videojs from 'video.js';
import Player from 'video.js/dist/types/player';
import 'videojs-contrib-quality-levels';
import 'videojs-http-source-selector';
import 'videojs-hls-quality-selector';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { environment } from '../../../environments/environment';
import { Video } from '../../interfaces/video.interface';

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

    if (this.player.hlsQualitySelector) {
      this.player.hlsQualitySelector();
    }

    this.http.get<Video>(environment.baseUrl + `/progress/${this.videoId}`).subscribe(response => {
      this.savedTime = parseFloat(response.progress) || 0;
      if (this.savedTime > 0) {
        this.showResumeButton = true;
        this.player.currentTime(this.savedTime);
        console.log(environment.baseUrl);

      }
    });

    this.player.on('play', () => {
      this.startSaveProgressInterval();
    });


    this.player.on('pause', () => {
      this.stopSaveProgressInterval();
      console.log(this.savedTime);
    });

    this.player.on('ended', () => {
      this.markAsSeen();
      this.stopSaveProgressInterval();
    });
  }

  markAsSeen() {
    this.http.post(environment.baseUrl + '/progress/', {
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
    this.http.post(environment.baseUrl + '/progress/', {
      video_slug: this.videoId,
      progress: currentTime
    }).subscribe(response => {
      console.log('Fortschritt gespeichert:', response);
    });
  }

  resumeVideo() {
    this.player.currentTime(this.savedTime);
    this.showResumeButton = false;
    this.player.play();
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
