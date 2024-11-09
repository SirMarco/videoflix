import { Routes } from '@angular/router';
import { ImprintComponent } from './components/imprint/imprint.component';
import { MainComponent } from './components/main/main.component';
import { PrivacyComponent } from './components/privacy/privacy.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { ResetpasswordComponent } from './components/resetpassword/resetpassword.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { authGuard } from './auth.guard';
import { ActivateComponent } from './components/activate/activate.component';
import { PasswordResetComponent } from './components/password-reset/password-reset.component';
import { VideoDetailComponent } from './components/video-detail/video-detail.component';
import { ErrorPageComponent } from './components/error-page/error-page.component';

export const routes: Routes = [
  { path: '', component: MainComponent },
  // { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  {
    path: 'dashboard',
    component: DashboardComponent,
    canActivate: [authGuard],
  },
  {
    path: 'video/:id',
    component: VideoDetailComponent,
    canActivate: [authGuard],
  },
  { path: 'register', component: RegisterComponent },
  { path: 'resetpassword', component: ResetpasswordComponent },
  { path: 'imprint', component: ImprintComponent },
  { path: 'privacy', component: PrivacyComponent },
  { path: 'activate/:id/:token', component: ActivateComponent },
  { path: 'password-reset/:id/:token', component: PasswordResetComponent },
  { path: '**', component: ErrorPageComponent },
];
