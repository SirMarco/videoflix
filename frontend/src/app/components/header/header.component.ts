import { Component, OnInit } from '@angular/core';
import { DeviceService } from '../../services/device.service';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent implements OnInit {
  isDesktop: boolean = false;
  showLoginButton: boolean = true;
  isLoggedIn: boolean = false;

  constructor(
    private deviceService: DeviceService,
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private authService: AuthService
  ) {
    this.router.events.subscribe(() => {
      let currentRoute = this.router.url;
      if (currentRoute === '/imprint' || currentRoute === '/privacy') {
        this.showLoginButton = false;
      } else {
        this.showLoginButton = true;
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
  }

  goBack() {
    this.router.navigate(['/']);
  }
}
