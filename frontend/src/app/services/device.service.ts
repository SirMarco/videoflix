import { Injectable } from '@angular/core';
import { DeviceDetectorService } from 'ngx-device-detector';

@Injectable({
  providedIn: 'root'
})
export class DeviceService {
  isMobile: boolean;
  isTablet: boolean;
  isDesktop: boolean;

  constructor(private deviceDetectorService: DeviceDetectorService) {
    this.isMobile = this.deviceDetectorService.isMobile();
    this.isTablet = this.deviceDetectorService.isTablet();
    this.isDesktop = this.deviceDetectorService.isDesktop();

    this.checkWindowSize();
    window.addEventListener('resize', () => this.checkWindowSize());
  }

  private checkWindowSize() {
    const width = window.innerWidth;
    this.isMobile = width <= 768;
    this.isTablet = width > 768 && width <= 1024;
    this.isDesktop = width > 1024;
  }
}
