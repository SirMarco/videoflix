import { CommonModule } from '@angular/common';
import { ApplicationRef, Component } from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  ValidationErrors,
  ValidatorFn,
  Validators,
} from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { CustomToastService } from '../../services/custom-toast.service';
import { NgxSpinnerService } from 'ngx-spinner';
import { NgxSpinnerModule } from "ngx-spinner";

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, RouterLink, NgxSpinnerModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss',
})
export class RegisterComponent {
  registerForm!: FormGroup;
  showPassword: boolean = false;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private route: ActivatedRoute,
    private customToastService: CustomToastService,
    private spinner: NgxSpinnerService
  ) { }

  ngOnInit(): void {
    this.registerForm = this.fb.group(
      {
        email: ['', [Validators.required, this.emailValidator()]],
        password: ['', [Validators.required, Validators.minLength(6)]],
        confirmPassword: ['', [Validators.required, Validators.minLength(6)]],
      },
      {
        validator: this.confirmPasswordValidator,
      }
    );

    // Email aus Query-Parameter holen
    this.route.queryParams.subscribe((params) => {
      const email = params['email'];
      if (email) {
        this.registerForm.patchValue({ email });
      }
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

  confirmPasswordValidator(control: AbstractControl): ValidationErrors | null {
    const password = control.get('password');
    const confirmPassword = control.get('confirmPassword');

    if (password && confirmPassword) {
      if (
        confirmPassword.errors &&
        !confirmPassword.errors['confirmPassword']
      ) {
        return null;
      }
      if (password.value !== confirmPassword.value) {
        confirmPassword.setErrors({ confirmPassword: true });
      } else {
        confirmPassword.setErrors(null);
      }
    }
    return null;
  }

  register(): void {
    if (this.registerForm.valid) {
      this.spinner.show();
      const { email, password } = this.registerForm.value;
      this.authService
        .registerNewUser(email, password)
        .then(() => {
          this.spinner.hide();
          this.showToast('Du bist registriert. Prüfe deine EMails', 'success');
          this.router.navigate(['/login']);
        })
        .catch(() => {
          this.spinner.hide();
          this.showToast('Du bist bereits registriert', 'error');
        });
    } else {
      this.spinner.hide();
      console.log('Form is invalid');
    }
  }

  togglePasswordVisibility(): void {
    this.showPassword = !this.showPassword;
  }

  showToast(message: string, status: string) {
    this.customToastService.showToast(message, status);
  }
}
