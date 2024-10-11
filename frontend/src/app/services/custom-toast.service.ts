import { Injectable } from '@angular/core';
import { CustomToastComponent } from '../components/custom-toast/custom-toast.component';

@Injectable({
  providedIn: 'root',
})
export class CustomToastService {
  private toastComponent: CustomToastComponent | undefined;

  register(toastComponent: CustomToastComponent) {
    this.toastComponent = toastComponent;
  }

  showToast(message: string, status: string) {
    if (this.toastComponent) {
      this.toastComponent.show(message, status);
    }
  }
}
