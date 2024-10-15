import {
  AfterViewInit,
  CUSTOM_ELEMENTS_SCHEMA,
  Component,
  OnInit,
  ViewChild,
} from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { VideoPlayerComponent } from '../video-player/video-player.component';
import { Video } from '../../interfaces/video.interface';
import { environment } from '../../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { NgxSpinnerService } from 'ngx-spinner';
import { NgxSpinnerModule } from "ngx-spinner";
// DEFAULT LAYOUT
// import 'vidstack/player/styles/default/theme.css';
// import 'vidstack/player/styles/default/layouts/video.css';
// import 'vidstack/player';
// import 'vidstack/player/layouts/default';
// import 'vidstack/player/ui';
// DEFAULT LAYOUT

// plyr THEME
import 'vidstack/player/styles/base.css';
import 'vidstack/player/styles/plyr/theme.css';
import 'vidstack/player';
import 'vidstack/player/layouts/plyr';
import 'vidstack/player/ui';
import Plyr from 'plyr';

import Hls from 'hls.js';
// plyr THEME

@Component({
  selector: 'app-video-detail',
  standalone: true,
  imports: [VideoPlayerComponent, CommonModule, NgxSpinnerModule],
  templateUrl: './video-detail.component.html',
  styleUrls: ['./video-detail.component.scss'],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class VideoDetailComponent implements OnInit, AfterViewInit {
  videoId: string | null = null;
  videoData?: Video;
  url = environment.baseUrl + '/videos/';
  hlsUrl = environment.hlsUrl;
  pictureUrl = environment.pictureUrl;

  public events: string[] = [];

  @ViewChild(VideoPlayerComponent) videoPlayer!: VideoPlayerComponent;
  // player: any;

  videoSrc = 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4';

  constructor(private route: ActivatedRoute, private http: HttpClient, private spinner: NgxSpinnerService) { }

  ngOnInit(): void {
    this.videoId = this.route.snapshot.paramMap.get('id');
    this.getSingleVideo();
  }

  ngAfterViewInit() {
    const player = new Plyr('#player', { fullscreen: { enabled: true } });
  }

  initializePlayer() {
    const mediaPlayer = document.querySelector('media-player');

    if (mediaPlayer) {
      const storageKey = mediaPlayer.getAttribute('storage-key');
      console.log('Storage Key:', storageKey);

      // Du kannst auch andere Events hier abfangen
      mediaPlayer.addEventListener('loadedmetadata', () => {
        console.log('Metadata geladen');
      });
    }
  }

  getSingleVideo() {
    this.spinner.show();
    this.http.get<Video>(this.url + this.videoId).subscribe(
      (data: Video) => {
        this.videoData = data;
        console.log(data);
        this.spinner.hide();
      },
      (error) => {
        console.error('Fehler beim Laden des Videos:', error);
      }
    );
  }
  public eventFired(event: string): void {
    this.events.push(event);
  }
}
