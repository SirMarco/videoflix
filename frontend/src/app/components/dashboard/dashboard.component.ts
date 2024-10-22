import { Component, OnInit, ViewChild } from '@angular/core';
import { environment } from '../../../environments/environment';
import { Video } from '../../interfaces/video.interface';
import { CommonModule } from '@angular/common';
import { VideoPlayerComponent } from '../video-player/video-player.component';
import { RouterLink } from '@angular/router';
import { BehaviorSubject } from 'rxjs';
import { NgxSpinnerService } from 'ngx-spinner';
import { NgxSpinnerModule } from 'ngx-spinner';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, VideoPlayerComponent, RouterLink, NgxSpinnerModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
})
export class DashboardComponent implements OnInit {
  url = environment.baseUrl + '/videos';
  pictureUrl = environment.pictureUrl;
  mediaUrl = environment.mediaUrl;
  videos: Video[] = [];
  randomVideo: Video | null = null;
  groupedVideos: { [category: string]: Video[] } = {};

  showPlayer: boolean = false;
  uploadStatus = new BehaviorSubject<string[]>([]);

  @ViewChild(VideoPlayerComponent) videoPlayer!: VideoPlayerComponent;
  player: any;

  constructor(private spinner: NgxSpinnerService) {}

  ngOnInit(): void {
    this.getAllVideos();
    console.log(this.videos);
  }

  getAllVideos() {
    this.spinner.show();
    const token = localStorage.getItem('token');
    console.log(token);

    fetch(this.url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${token}`,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        this.videos = data;
        this.groupVideosByCategory();
        this.selectRandomVideo();
        const initialStatus = this.videos.map(
          (video) => video.status || 'Uploading'
        );
        this.uploadStatus.next(initialStatus);
        this.initializeWebSocket();
        this.spinner.hide();
      })
      .catch((error) => {
        console.error('Error fetching videos:', error);
        this.spinner.hide();
      });
  }

  initializeWebSocket() {
    const socket = new WebSocket(
      'wss://api.videoflix.marco-engelhardt.ch/ws/conversion-status/'
    );
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const videoIndex = this.videos.findIndex(
        (video) => video.slug === data.slug
      );
      console.log('Video Index:', videoIndex);
      if (videoIndex !== -1) {
        const currentStatus = this.uploadStatus.value;
        currentStatus[videoIndex] = data.status;
        this.uploadStatus.next(currentStatus);
      } else {
        console.log('no, video not found');
      }
    };

    socket.onerror = (error) => {
      console.error('WebSocket Fehler:', error);
    };

    socket.onclose = (event) => {
      console.log('WebSocket Verbindung geschlossen:', event);
    };
  }

  groupVideosByCategory() {
    this.videos.forEach((video) => {
      video.categories.forEach((category) => {
        if (!this.groupedVideos[category]) {
          this.groupedVideos[category] = [];
        }
        this.groupedVideos[category].push(video);
      });
    });
  }

  selectRandomVideo() {
    if (this.videos.length > 0) {
      const randomIndex = Math.floor(Math.random() * this.videos.length);
      this.randomVideo = this.videos[randomIndex];
    }
  }

  // Umwandlung von `groupedVideos` in eine Liste von Schlüssel-Wert-Paaren
  getCategories(): string[] {
    return Object.keys(this.groupedVideos); // Rückgabe der Kategorienamen
  }

  getFullThumbnailUrl(thumbnail: string): string {
    // return environment.pictureUrl + thumbnail; // Füge die Base URL zur Thumbnail-URL hinzu
    return this.mediaUrl + thumbnail; // Füge die Base URL zur Thumbnail-URL hinzu
  }
  getFullVideoUrl(video_file: string): string {
    // return environment.pictureUrl + thumbnail; // Füge die Base URL zur Thumbnail-URL hinzu
    return this.mediaUrl + video_file; // Füge die Base URL zur Thumbnail-URL hinzu
  }

  getVideosByCategory(category: string): Video[] {
    // Rückgabe eines leeren Arrays, wenn `groupedVideos` oder die Kategorie selbst nicht existieren
    return this.groupedVideos && this.groupedVideos[category]
      ? this.groupedVideos[category]
      : [];
  }

  // playVideo() {
  //   this.showPlayer = true; // Schalte den Zustand um, um den Player anzuzeigen

  //   // Falls der Player schon vorhanden ist, initialisiere und spiele das Video ab
  //   setTimeout(() => {
  //     if (this.videoPlayer) {
  //       this.videoPlayer.initializePlayer(); // Initialisiere den Player in der VideoPlayerComponent
  //       this.videoPlayer.player.play(); // Spiele das Video sofort ab
  //     }
  //   }, 0); // Stelle sicher, dass der Player sichtbar ist, bevor Video.js initialisiert wird
  // }
}
