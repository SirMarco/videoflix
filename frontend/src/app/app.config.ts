import { ApplicationConfig, importProvidersFrom } from '@angular/core';
import {
  InMemoryScrollingOptions,
  provideRouter,
  withInMemoryScrolling,
} from '@angular/router';

import { routes } from './app.routes';
import {
  HTTP_INTERCEPTORS,
  provideHttpClient,
  withInterceptorsFromDi,
} from '@angular/common/http';
import { AuthInterceptorService } from './services/auth-interceptor.service';

import { provideToastr } from 'ngx-toastr';
import { provideAnimations } from '@angular/platform-browser/animations';

const routerOptions: InMemoryScrollingOptions = {
  scrollPositionRestoration: 'enabled',
  anchorScrolling: 'enabled',
};

export const appConfig: ApplicationConfig = {
  providers: [
    provideAnimations(),
    provideToastr({
      positionClass: 'toast-bottom-center',
      preventDuplicates: true,
      closeButton: true,
      disableTimeOut: true,
    }),
    provideRouter(routes, withInMemoryScrolling(routerOptions)),
    provideHttpClient(withInterceptorsFromDi()),
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptorService,
      multi: true,
    },
  ],
};
