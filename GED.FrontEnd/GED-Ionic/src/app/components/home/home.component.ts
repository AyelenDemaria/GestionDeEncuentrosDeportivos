import { ChangeDetectorRef, Component, NgZone, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';
import { AlertController } from '@ionic/angular';
import { PartidoService } from 'src/app/services/partido.service';
import { UsuarioService } from 'src/app/services/usuario.service';
import { InscripcionService } from 'src/app/services/inscripcion.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent {
  partidos: any[] = [];
  puntos: number
  recordatorio: number

  constructor(
    private authService: AuthService,
    private router: Router,
    private usuarioService: UsuarioService,
    private partidoService: PartidoService,
    private ngZone: NgZone,
    private changeDetectorRef: ChangeDetectorRef,
    private alertController: AlertController,
    private inscripcionService: InscripcionService

  ) { }

  async ionViewDidEnter() {
    await this.getPartidos();
    this.partidosSuspendidos();
    this.puntosUsuario()
    this.partidosSemana()    
   
    
  }


  // getPartidos() {
  //   this.inscripcionService.getPartidosSuspendidos().subscribe(
  //     (data: any[]) => {
  //       this.partidos = data;
  //       console.log(this.partidos);
  //     },
  //     (error: any) => {
  //       console.log(error);
  //     }
  //   );
  // }

  async getPartidos() {
    return new Promise<void>((resolve, reject) => {
      this.inscripcionService.getPartidosSuspendidos().subscribe(
        (data: any[]) => {
          this.partidos = data;
          console.log(this.partidos);
          resolve();
        },
        (error: any) => {
          console.log(error);
          reject(error);
        }
      );
    });
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

  partidosSemana() {
    this.partidoService.partidosSemana().subscribe(res => {
      this.recordatorio = res
      console.log(this.recordatorio)
    })
  }

  async partidosSuspendidos() {
    if (this.partidos.length !== 0) {
      const alert =await  this.alertController.create({
        header: 'AVISO!',
        message: 'Se suspendieron partidos en los que estabas inscripto',
        buttons: [
          {
            text: 'Ver partidos suspendidos',
            handler: () => {
              this.router.navigateByUrl('/suspendidos');
            }
          }
        ],
        cssClass: 'my-alert'
      });
      await alert.present();
    }
  }


}
