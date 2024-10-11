// auth.guard.ts
import { CanActivateFn } from '@angular/router';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from './services/auth.service';
import { map } from 'rxjs/operators';

export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService); // Inject den AuthService
  const router = inject(Router); // Inject den Router

  return authService.isLoggedIn().pipe(
    map((isLoggedIn) => {
      if (isLoggedIn) {
        return true; // Wenn eingeloggt, Zugriff erlauben
      } else {
        router.navigate(['/login']); // Umleiten, falls nicht eingeloggt
        return false;
      }
    })
  );
};
