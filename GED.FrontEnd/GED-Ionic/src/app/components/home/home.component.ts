import { ChangeDetectorRef, Component, NgZone, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';

import { PartidoService } from 'src/app/services/partido.service';
import { UsuarioService } from 'src/app/services/usuario.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent {

  puntos: number
  recordatorio: number

  constructor(
    private authService: AuthService,
    private router: Router,
    private usuarioService: UsuarioService,
    private partidoService: PartidoService,
    private ngZone: NgZone,
    private changeDetectorRef: ChangeDetectorRef

  ) { }

  ionViewDidEnter() {
 
    this.puntosUsuario()
    this.partidosSemana()
  
  }

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

 

  puntosUsuario() {    
    this.usuarioService.getPuntosUsuario().subscribe(res => {
      this.puntos = res;
      this.changeDetectorRef.detectChanges();
    });
  }

  partidosSemana(){
    this.partidoService.partidosSemana().subscribe(res => {
      this.recordatorio = res
      console.log(this.recordatorio)
    })
  }

  
}
