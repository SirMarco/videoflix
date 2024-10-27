import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  ValidatorFn,
  Validators,
} from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { ToastrService } from 'ngx-toastr';
import { CustomToastService } from '../../services/custom-toast.service';
import { NgxSpinnerService } from 'ngx-spinner';
import { NgxSpinnerModule } from 'ngx-spinner';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    RouterLink,
    NgxSpinnerModule,
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
})
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;
  showPassword: boolean = false;

  constructor(
    private as: AuthService,
    private fb: FormBuilder,
    private router: Router,
    private customToastService: CustomToastService,
    private spinner: NgxSpinnerService
  ) { }

  ngOnInit(): void {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, this.emailValidator()]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      rememberMe: [false],
    });
  }

  emailValidator(): ValidatorFn {
    return (control: AbstractControl): { [key: string]: any } | null => {
      const email = control.value;
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/i;
      const valid = emailRegex.test(email);
      return valid ? null : { invalidEmail: true };
    };
  }

  async login() {
    if (this.loginForm.valid) {
      const email = this.loginForm.get('email')?.value;
      const password = this.loginForm.get('password')?.value;
      const rememberMe = this.loginForm.get('rememberMe')?.value;
      this.spinner.show();
      try {
        let resp: any = await this.as.loginWithUsernameAndPassword(
          email,
          password,
          rememberMe
        );
        localStorage.setItem('token', resp['token']);
        this.spinner.hide();
        this.showToast('Login successfully', 'success');
        setTimeout(() => {
          this.router.navigateByUrl('/dashboard');
        }, 1000);
      } catch (error) {
        this.spinner.hide();
        this.showToast('Prüfe deine Daten', 'error');
        console.log(error);
      }
    }
  }

  togglePasswordVisibility(): void {
    let message = 'Login';
    this.showPassword = !this.showPassword;
  }

  showToast(message: string, status: string) {
    this.customToastService.showToast(message, status);
  }
}
