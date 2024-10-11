import { CommonModule } from '@angular/common';
import { compileNgModule } from '@angular/compiler';
import { Component } from '@angular/core';

@Component({
  selector: 'app-custom-toast',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './custom-toast.component.html',
  styleUrl: './custom-toast.component.scss',
})
export class CustomToastComponent {
  isVisible = false;
  message = '';
  status = '';

  show(message: string, status: string, duration: number = 3000) {
    this.message = message;
    this.status = status;
    this.isVisible = true;

    setTimeout(() => {
      this.isVisible = false;
    }, duration);
  }

  close() {
    this.isVisible = false;
  }
}
