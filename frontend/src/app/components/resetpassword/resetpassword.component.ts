import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
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
import { environment } from '../../../environments/environment';
import { CustomToastService } from '../../services/custom-toast.service';
import { NgxSpinnerService } from 'ngx-spinner';
import { NgxSpinnerModule } from "ngx-spinner";

@Component({
  selector: 'app-resetpassword',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, RouterLink, NgxSpinnerModule],
  templateUrl: './resetpassword.component.html',
  styleUrl: './resetpassword.component.scss',
})
export class ResetpasswordComponent {
  resetPassword!: FormGroup;
  emailSent = false;
  errorMessage = '';

  constructor(private fb: FormBuilder, private http: HttpClient, private router: Router, private customToastService: CustomToastService, private spinner: NgxSpinnerService) { }

  ngOnInit(): void {
    this.resetPassword = this.fb.group({
      email: ['', [Validators.required, this.emailValidator()]],
    });
  }

  emailValidator(): ValidatorFn {
    return (control: AbstractControl): { [key: string]: any } | null => {
      const email = control.value;
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/i;
      const valid = emailRegex.test(email);
      return valid ? null : { 'invalidEmail': true };
    };
  }

  reset(): void {
    if (this.resetPassword.valid) {
      let email = this.resetPassword.value.email;
      this.spinner.show();
      this.http
        .post(environment.baseUrl + '/password-reset/', { email: email })
        .subscribe({
          next: () => {
            this.emailSent = true;
            this.showToast('Bitte prüfe deine EMails', 'success')
            this.resetPassword.reset();
            this.spinner.hide();
          },
          error: () => {
            this.spinner.hide();
            this.showToast('Email ist nicht registriert', 'error')
          },
        });
    } else {
      console.log('Form is invalid');
    }
  }

  showToast(message: string, status: string) {
    this.customToastService.showToast(message, status);
  }
}
