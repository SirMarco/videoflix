import { Component, OnInit } from '@angular/core';
import { DeviceService } from '../../services/device.service';
import { ActivatedRoute, NavigationEnd, Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth.service';
import { Location } from '@angular/common';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent implements OnInit {
  isDesktop: boolean = false;
  showBackButton: boolean = false;
  isLoggedIn: boolean = false;


  constructor(
    private deviceService: DeviceService,
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private authService: AuthService,
    private location: Location
  ) {
    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        const currentRoute = this.router.url;
        this.showBackButton = currentRoute === '/imprint' || currentRoute === '/privacy';
      }
    });
  }

  ngOnInit() {
    this.isDesktop = this.deviceService.isDesktop;
    this.authService.isLoggedIn().subscribe((status) => {
      this.isLoggedIn = status;
    });
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  goBack() {
    this.location.back();
  }
}
