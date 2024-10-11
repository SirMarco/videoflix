import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { environment } from '../../../environments/environment';
import { Video } from '../../interfaces/video.interface';
import { CommonModule } from '@angular/common';
import { VideoPlayerComponent } from '../video-player/video-player.component';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, VideoPlayerComponent, RouterLink],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
})
export class DashboardComponent implements OnInit {
  url = environment.baseUrl + '/videos';
  pictureUrl = environment.pictureUrl;
  videos: Video[] = [];
  randomVideo: Video | null = null;
  groupedVideos: { [category: string]: Video[] } = {};

  showPlayer: boolean = false;

  @ViewChild(VideoPlayerComponent) videoPlayer!: VideoPlayerComponent;
  player: any;

  constructor() { }

  ngOnInit(): void {
    this.getAllVideos();
  }

  getAllVideos() {
    fetch(this.url)
      .then((response) => response.json())
      .then((data) => {
        this.videos = data;
        this.groupVideosByCategory();
        this.selectRandomVideo();
        console.log(this.videos);
      })
      .catch((error) => console.error('Error' + error));
  }

  // Funktion, um Videos nach Kategorien zu gruppieren
  groupVideosByCategory() {
    this.videos.forEach((video) => {
      video.categories.forEach((category) => {
        if (!this.groupedVideos[category]) {
          this.groupedVideos[category] = [];
        }
        this.groupedVideos[category].push(video);
      });
    });
    console.log(this.groupedVideos); // Prüfe die gruppierten Videos
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
    return environment.pictureUrl + thumbnail; // Füge die Base URL zur Thumbnail-URL hinzu
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
