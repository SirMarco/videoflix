import {
  Component,
  ElementRef,
  OnInit,
  ViewChild,
} from '@angular/core';
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
  autoplay: boolean = true
  uploadStatus = new BehaviorSubject<string[]>([]);

  @ViewChild(VideoPlayerComponent) videoPlayer!: VideoPlayerComponent;
  @ViewChild('backgroundVideo') backgroundVideo!: ElementRef;
  player: any;

  constructor(private spinner: NgxSpinnerService) { }

  ngOnInit(): void {
    this.getAllVideos();

  }

  getAllVideos() {
    this.spinner.show();
    const token = localStorage.getItem('token');
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
        this.spinner.hide();
      })
      .catch((error) => {
        console.error('Error fetching videos:', error);
        this.spinner.hide();
      });
  }

  groupVideosByCategory() {
    this.videos.forEach((video) => {
      if (video.status === "Done") {
        video.categories.forEach((category) => {
          if (!this.groupedVideos[category]) {
            this.groupedVideos[category] = [];
          }
          this.groupedVideos[category].push(video);
        });
      }
    });
  }

  selectRandomVideo() {
    if (this.videos.length > 0) {
      const randomIndex = Math.floor(Math.random() * this.videos.length);
      this.randomVideo = this.videos[randomIndex];
    }
  }

  getCategories(): string[] {
    return Object.keys(this.groupedVideos);
  }

  getFullVideoUrl(video_file: string): string {
    return video_file;
  }

  getVideosByCategory(category: string): Video[] {
    return this.groupedVideos && this.groupedVideos[category]
      ? this.groupedVideos[category]
      : [];
  }
}
