import { CUSTOM_ELEMENTS_SCHEMA, Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Video } from '../../interfaces/video.interface';
import { environment } from '../../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { NgxSpinnerService } from 'ngx-spinner';
import { NgxSpinnerModule } from "ngx-spinner";

@Component({
  selector: 'app-video-detail',
  standalone: true,
  imports: [CommonModule, NgxSpinnerModule],
  templateUrl: './video-detail.component.html',
  styleUrls: ['./video-detail.component.scss'],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class VideoDetailComponent implements OnInit {
  videoId: string | null = null;
  videoData?: Video;
  url = environment.baseUrl + '/videos/';
  hlsUrl = environment.hlsUrl;
  pictureUrl = environment.pictureUrl;

  constructor(private route: ActivatedRoute, private http: HttpClient, private spinner: NgxSpinnerService) { }

  ngOnInit(): void {
    this.videoId = this.route.snapshot.paramMap.get('id');
    this.getSingleVideo();
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
}