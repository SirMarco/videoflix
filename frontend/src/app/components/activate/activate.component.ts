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
  activationStatus: string = ''; // Um den Status der Aktivierung zu speichern

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient,
    private router: Router
  ) {}

  ngOnInit(): void {
    const uid = this.route.snapshot.paramMap.get('id');
    const token = this.route.snapshot.paramMap.get('token');

    if (uid && token) {
      this.activateAccount(uid, token);
    }
  }

  activateAccount(id: string, token: string): void {
    // Sende Aktivierungsdaten an das Django-Backend
    this.http.get(environment.baseUrl + `/activate/${id}/${token}/`).subscribe({
      next: (response: any) => {
        this.activationStatus = 'Account erfolgreich aktiviert.';
      },
      error: (error) => {
        this.activationStatus =
          'Die Aktivierung ist fehlgeschlagen oder der Link ist ungültig.';
        console.log(error.error.error);
      },
    });
  }
}
