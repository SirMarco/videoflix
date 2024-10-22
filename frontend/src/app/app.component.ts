import { AfterViewInit, Component, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  NavigationEnd,
  Router,
  RouterLink,
  RouterLinkActive,
  RouterOutlet,
} from '@angular/router';
import { HeaderComponent } from './components/header/header.component';
import { FooterComponent } from './components/footer/footer.component';
import { MainComponent } from './components/main/main.component';
import { LoginComponent } from './components/login/login.component';
import { CustomToastComponent } from './components/custom-toast/custom-toast.component';
import { CustomToastService } from './services/custom-toast.service';
import { AuthService } from './services/auth.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    RouterOutlet,
    HeaderComponent,
    FooterComponent,
    MainComponent,
    RouterOutlet,
    RouterLink,
    RouterLinkActive,
    LoginComponent,
    CustomToastComponent,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent implements OnInit, AfterViewInit {
  title = 'frontend_videoflix';
  layoutClass: string = 'start';
  @ViewChild(CustomToastComponent) toast: CustomToastComponent | undefined;

  constructor(
    private customToastService: CustomToastService,
    private router: Router,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    if (this.authService.isLoggedIn()) {
      // Wenn eingeloggt, auf Dashboard weiterleiten
      this.router.navigate(['/dashboard']);
    }

    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        if (this.router.url.startsWith('/video')) {
          this.layoutClass = 'start';
        } else {
          this.layoutClass = 'center';
        }
      }
    });
  }

  ngAfterViewInit() {
    if (this.toast) {
      this.customToastService.register(this.toast);
    }
  }
}
