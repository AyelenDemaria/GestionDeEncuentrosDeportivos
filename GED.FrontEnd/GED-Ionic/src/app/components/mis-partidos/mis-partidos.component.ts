import { Component, OnInit } from '@angular/core';
import { AlertController } from '@ionic/angular';
import { InscripcionService } from 'src/app/services/inscripcion.service';
import { PartidoService } from 'src/app/services/partido.service';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-mis-partidos',
  templateUrl: './mis-partidos.component.html',
  styleUrls: ['./mis-partidos.component.scss'],
})
export class MisPartidosComponent implements OnInit {

  filtro = '';
  partidos: any[] = []


  constructor(
    private alertController: AlertController,
    private inscripcionService: InscripcionService,
    private router: Router,
    private authService: AuthService,
  ) { }

  ngOnInit() {
    this.inscripcionService.getInscripcionesUser().subscribe(
      (data: any[]) => {
        this.partidos = data;
        console.log(this.partidos);
      },
      (error: any) => {
        console.log(error);
      }
    );
  }


  get filteredPartidos() {
    if (this.filtro != "") {
      return this.partidos.filter(x => (x.partido.cancha.deporte.descripcion.toLowerCase() + x.partido.fecha_hora + x.partido.cant_jugadores
        + x.partido.cancha.direccion.toLowerCase() + x.partido.tipo_partido.descripcion.toLowerCase()).
        includes(this.filtro.toLowerCase()));
    }
    return this.partidos;
  }


  async mensajeBaja(inscripcionId: number) {
    const alert = await this.alertController.create({
      header: '¿Estas seguro que querés darte de baja del partido?',
      message: 'Si te das de baja no podrás volver a unirte',
      buttons: [
        {
          text: 'Cancelar',
          role: 'cancel',
        },
        {
          text: 'OK',
          handler: () => {
            this.bajaInscripcion(inscripcionId);
          },
        },
      ],
    });
    await alert.present();
  }

  bajaInscripcion(inscripcion_id: number) {

    const body = {
      username: this.authService.getUsername(),
      inscripcion_id: inscripcion_id
    }
    this.inscripcionService.bajaInscripcionPartido(body).subscribe(
      (data) => {
        this.mensajeExito()
        this.router.navigateByUrl('/misPartidos');
      },
      (error) => {
        console.log(error)
      });
  }

  async mensajeExito() {
    const alert = await this.alertController.create({
      header: 'Te diste de baja del partido.',
      buttons: ['OK'],
    });
    await alert.present();
  }


  partidoFechaPasada(fecha: string): boolean {
    const fechaPartido = new Date(fecha);
    const fechaActual = new Date();
    return fechaPartido > fechaActual;
  }

  invitar(id_partido: number) {
    this.router.navigate(['/invitar', id_partido]);
  }


}
