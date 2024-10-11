import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-main',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './main.component.html',
  styleUrl: './main.component.scss',
})
export class MainComponent {
  email: string = '';
  emailError: string = '';

  constructor(private router: Router) {}

  isValidEmail(email: string): boolean {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailPattern.test(email);
  }

  navigateToRegister() {
    if (this.email) {
      if (this.isValidEmail(this.email)) {
        this.router.navigate(['/register'], {
          queryParams: { email: this.email },
        });
      } else {
        this.emailError = 'Invalid email format';
      }
    } else {
      this.emailError = 'Email is required';
    }
  }
}
