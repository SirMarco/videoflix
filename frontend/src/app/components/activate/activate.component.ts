import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { environment } from '../../../environments/environment';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-activate',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './activate.component.html',
  styleUrl: './activate.component.scss',
})
export class ActivateComponent implements OnInit {
  activationStatus: string = '';
  progress: number = 0;

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient,
    private router: Router
  ) { }

  ngOnInit(): void {
    const uid = this.route.snapshot.paramMap.get('id');
    const token = this.route.snapshot.paramMap.get('token');

    if (uid && token) {
      this.activateAccount(uid, token);
    }
  }

  activateAccount(id: string, token: string): void {
    console.log(environment.baseUrl);
    this.http.get(environment.baseUrl + `/activate/${id}/${token}/`).subscribe({
      next: (response: any) => {
        this.activationStatus = 'Account erfolgreich aktiviert.';

        // Start der Progress-Bar und Weiterleitung nach 2 Sekunden
        this.progress = 0; // Reset Fortschritt
        const interval = setInterval(() => {
          this.progress += 1;
          if (this.progress >= 100) {
            clearInterval(interval);
            this.router.navigate(['/login']); // Weiterleitung nach 2 Sekunden
          }
        }, 20); // 20ms Intervalle = 2 Sekunden für 100%
      },
      error: (error) => {
        this.activationStatus = 'Die Aktivierung ist fehlgeschlagen oder der Link ist ungültig.';
        console.error('Aktivierungsfehler:', error);
      },
    });
  }
}