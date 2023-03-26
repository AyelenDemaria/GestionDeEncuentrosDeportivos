import { Component, OnInit } from '@angular/core';
import { AlertController } from '@ionic/angular';
import { InscripcionService } from 'src/app/services/inscripcion.service';
import { PartidoService } from 'src/app/services/partido.service';
import { Router } from '@angular/router';

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
    private router: Router
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

  
  async mensaje() {
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
          role: 'confirm',
        },
      ],
    });
    await alert.present();
  }


  partidoFechaPasada(fecha: string): boolean {
    const fechaPartido = new Date(fecha);
    const fechaActual = new Date();
    return fechaPartido > fechaActual;
  }

  invitar(id_partido:number){
    this.router.navigate(['/invitar', id_partido]);
  } 

  
}
