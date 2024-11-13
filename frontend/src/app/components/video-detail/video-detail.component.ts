import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { Video } from '../../interfaces/video.interface';
import { environment } from '../../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { NgxSpinnerService } from 'ngx-spinner';
import { NgxSpinnerModule } from 'ngx-spinner';
import { VideoPlayerComponent } from '../video-player/video-player.component';
import { Location } from '@angular/common';

@Component({
  selector: 'app-video-detail',
  standalone: true,
  imports: [CommonModule, NgxSpinnerModule, VideoPlayerComponent, RouterLink],
  templateUrl: './video-detail.component.html',
  styleUrls: ['./video-detail.component.scss'],
})
export class VideoDetailComponent implements OnInit {
  videoId: string | null = null;
  videoData?: Video;
  url = environment.baseUrl + '/videos/';
  hlsUrl = environment.hlsUrl;
  pictureUrl = environment.pictureUrl;
  mediaUrl = environment.mediaUrl;

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient,
    private spinner: NgxSpinnerService,
    private location: Location
  ) {}

  ngOnInit(): void {
    this.videoId = this.route.snapshot.paramMap.get('id');
    this.getSingleVideo();
  }

  getSingleVideo() {
    this.spinner.show();
    this.http.get<Video>(this.url + this.videoId).subscribe(
      (data: Video) => {
        this.videoData = data;
        this.spinner.hide();
      },
      (error) => {
        console.error('Fehler beim Laden des Videos:', error);
      }
    );
  }

  goBack() {
    this.location.back();
  }
}
