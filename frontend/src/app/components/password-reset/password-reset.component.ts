import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { environment } from '../../../environments/environment';
import { CustomToastService } from '../../services/custom-toast.service';

@Component({
  selector: 'app-password-reset',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  templateUrl: './password-reset.component.html',
  styleUrl: './password-reset.component.scss',
})
export class PasswordResetComponent implements OnInit {
  passwordForm!: FormGroup;
  newPassword: string = '';
  confirmPassword: string = '';
  resetStatus: string = '';
  showPassword: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient,
    private router: Router,
    private fb: FormBuilder,
    private customToastService: CustomToastService
  ) { }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    const token = this.route.snapshot.paramMap.get('token');

    this.passwordForm = this.fb.group({
      newPassword: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', [Validators.required, Validators.minLength(6)]],
      rememberMe: [false],
    });
  }

  handlePasswordReset(): void {
    const id = this.route.snapshot.paramMap.get('id');
    const token = this.route.snapshot.paramMap.get('token');

    if (this.passwordForm.value.newPassword !== this.passwordForm.value.confirmPassword) {
      this.resetStatus = 'Passwords do not match.';
      return;
    }
    this.http
      .post(environment.baseUrl + '/password-reset/confirm/', {
        id,
        token,
        new_password: this.passwordForm.value.newPassword,
      })
      .subscribe({
        next: (response: any) => {
          this.resetStatus = 'Password successfully reset';
          this.showToast('Password successfully reset', 'success');
          setTimeout(() => {
            this.router.navigateByUrl('/login');
          }, 3000);
        },
        error: (error) => {
          this.resetStatus = 'Password reset failed or the link is invalid.';
          this.showToast('Password reset failed or the link is invalid.', 'error')
        }
      });
  }

  togglePasswordVisibility(): void {
    this.showPassword = !this.showPassword;
  }

  showToast(message: string, status: string) {
    this.customToastService.showToast(message, status);
  }
}
