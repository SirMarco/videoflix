import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { HeaderComponent } from './components/header/header.component';
import { FooterComponent } from './components/footer/footer.component';
import { MainComponent } from './components/main/main.component';
import { LoginComponent } from './components/login/login.component';
import { CustomToastComponent } from './components/custom-toast/custom-toast.component';
import { CustomToastService } from './services/custom-toast.service';

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
export class AppComponent implements AfterViewInit {
  title = 'frontend_videoflix';
  @ViewChild(CustomToastComponent) toast: CustomToastComponent | undefined;

  constructor(private customToastService: CustomToastService) {}

  ngAfterViewInit() {
    if (this.toast) {
      this.customToastService.register(this.toast);
    }
  }
}
