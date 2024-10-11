import { Component, ElementRef, Input, OnDestroy, OnInit, ViewChild, ViewEncapsulation } from '@angular/core';
// import videojs from 'video.js';
import { environment } from '../../../environments/environment';
// import videojs from 'video.js'; // Haupt-Video.js-Import
// import 'videojs-contrib-quality-levels'; // Importiere das Quality Levels Plugin
// import 'videojs-hls-quality-selector'; // Importiere das HLS Quality Selector Plugin


@Component({
  selector: 'app-video-player',
  standalone: true,
  imports: [],
  templateUrl: './video-player.component.html',
  styleUrl: './video-player.component.scss',
  encapsulation: ViewEncapsulation.None,
})
export class VideoPlayerComponent {
  pictureUrl = environment.pictureUrl;
  @ViewChild('target', { static: true }) target!: ElementRef;
  @Input() videoSrc!: string;
  @Input() videoType: string = 'application/x-mpegURL';
  player!: any; // Deklariere den Player

  constructor(private elementRef: ElementRef) { }
  // initializePlayer() {
  //   if (!this.player) {
  //     // Initialisiere den Player
  //     this.player = videojs(this.target.nativeElement, {
  //       preload: "metadata",
  //       fluid: true,
  //       controls: true,
  //       autoplay: false,
  //       overrideNative: true,
  //       loop: false,
  //       controlBar: {
  //         skipButtons: {
  //           forward: 10,
  //           backward: 10,
  //         },
  //       },
  //       sources: [
  //         {
  //           src: this.videoSrc,
  //           type: this.videoType,
  //         },
  //       ],
  //       pictureInPictureToggle: false,
  //     });
  //   }
  // }



  // ngOnDestroy() {
  //   if (this.player) {
  //     this.player.dispose();
  //   }
  // }
}
