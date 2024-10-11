import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { BehaviorSubject, Observable, lastValueFrom } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private userId: number | null = null;
  private loggedIn = new BehaviorSubject<boolean>(this.hasToken()); // Überwacht den Login-Status

  constructor(private http: HttpClient, private router: Router) {}

  public loginWithUsernameAndPassword(username: string, password: string) {
    const url = environment.baseUrl + '/login/';
    const body = {
      username: username,
      password: password,
    };
    return lastValueFrom(this.http.post(url, body)).then((response: any) => {
      this.userId = response.user_id;
      localStorage.setItem('userId', response.user_id);
      localStorage.setItem('token', response.token);
      this.loggedIn.next(true);
      return response;
    });
  }

  public registerNewUser(email: string, password: string) {
    const url = environment.baseUrl + '/register/';
    const body = { email: email, password: password };
    return lastValueFrom(this.http.post(url, body));
  }

  public logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    this.userId = null;
    this.loggedIn.next(false);
    this.router.navigate(['/login']);
  }

  private hasToken(): boolean {
    return !!localStorage.getItem('token');
  }

  public getUserId(): number | null {
    return this.userId;
  }

  isLoggedIn(): Observable<boolean> {
    return this.loggedIn.asObservable();
  }
}
