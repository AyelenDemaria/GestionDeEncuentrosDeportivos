import { Component } from '@angular/core';
import { AuthService } from './services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.scss'],
})
export class AppComponent {
  constructor(   
    private authService: AuthService,
    private router: Router)
    {}

  cerrarSesion() {
    this.authService.logout().subscribe(
      (data) => {
        console.log(data);
        this.router.navigateByUrl('/login');
      },
      (error) => {
        console.log(error);
      }
    );
  }
}


