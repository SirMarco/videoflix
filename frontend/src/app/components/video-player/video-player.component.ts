import { AfterViewInit, Component, ElementRef, Input, OnDestroy, ViewChild, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { environment } from '../../../environments/environment';
import { Video } from '../../interfaces/video.interface';

import 'vidstack/player/styles/base.css';
import 'vidstack/player/styles/plyr/theme.css';

import 'vidstack/player';
import 'vidstack/player/layouts/plyr';
import 'vidstack/player/ui';

@Component({
  selector: 'app-video-player',
  standalone: true,
  imports: [CommonModule],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  templateUrl: './video-player.component.html',
  styleUrl: './video-player.component.scss'
})
export class VideoPlayerComponent implements AfterViewInit, OnDestroy {
  @ViewChild('targetVideo', { static: true }) target!: ElementRef;
  @Input() videoSrc!: string;
  @Input() videoId!: string;
  @Input() thumbnail!: string;
  @Input() title!: string;
  @Input() poster!: string;
  public events: string[] = [];
  player!: any;
  saveInterval: any;
  showResumeButton = false;
  savedTime = 0;

  constructor(private http: HttpClient) { }

  ngAfterViewInit() {
    if (!this.videoSrc || !this.videoId) return;
    this.http.get<Video>(environment.baseUrl + `/progress/${this.videoId}`).subscribe(response => {
      this.savedTime = parseFloat(response.progress) || 0;
      this.player = this.target.nativeElement;
      if (this.savedTime > 0) {
        this.showResumeButton = true;
      }
      if (this.savedTime > 0) {
        this.player.currentTime = this.savedTime;
      }
    });
  }

  eventFired(eventName: string) {
    if (eventName == 'play') {
      this.startSaveProgressInterval()
      this.showResumeButton = false
    } if (eventName == 'pause') {
      this.stopSaveProgressInterval()
    }
    console.log(`Event triggered: ${eventName}`);
  }

  saveProgress(currentTime: number) {
    const url = `${environment.baseUrl}/progress/${this.videoId}/`;
    this.http.post(url, {
      progress: currentTime,
    }).subscribe(
      response => {
        console.log('Fortschritt erfolgreich gespeichert:', response);
      },
      error => {
        console.error('Fehler beim Speichern des Fortschritts:', error);
      }
    );
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
    if (this.saveInterval) return; // Intervall nur einmal starten

    this.saveInterval = setInterval(() => {
      const currentTime = this.player.currentTime;
      if (typeof currentTime === 'number') {
        this.saveProgress(currentTime);
        console.log('current saved time' + currentTime);

      }
    }, 2000);
  }

  // Intervall stoppen
  stopSaveProgressInterval() {
    if (this.saveInterval) {
      clearInterval(this.saveInterval);
      this.saveInterval = null;
    }
  }

  resumeVideo() {
    // this.player.currentTime(this.savedTime);
    this.player.currentTime = this.savedTime;
    this.showResumeButton = false;
    this.player.play();
  }

  ngOnDestroy() {
    this.stopSaveProgressInterval();
  }
}
