import { Component, OnInit } from '@angular/core';
import { AlertController } from '@ionic/angular';
import { InscripcionService } from 'src/app/services/inscripcion.service';
import { PartidoService } from 'src/app/services/partido.service';
import { HttpErrorResponse } from '@angular/common/http';
import { Router } from '@angular/router';


@Component({
  selector: 'app-unirme',
  templateUrl: './unirme.component.html',
  styleUrls: ['./unirme.component.scss'],
})
export class UnirmeComponent implements OnInit {
  partidos: any[] = []
  filtro = ''; 
  errorMensaje:string

  fecha: string = new Date().toISOString();
  ocultarCalendario = true;
  

  constructor(
    private partidoService: PartidoService,
    private inscripcionService: InscripcionService,
    private alertController: AlertController,
    private router: Router,
    ) { }

  ngOnInit() {
    this.partidoService.getPartidos().subscribe((data: any[]) => {
      this.partidos = data;
      console.log(this.partidos);
    },
    (error) => {
      console.log(error);
    })
   } 

   get filteredPartidos() {
    if (this.filtro != "") {
      return this.partidos.filter(x => (x.fecha_hora + x.cant_jugadores + x.cancha.deporte.descripcion.toLowerCase()
        + x.cancha.direccion.toLowerCase() + x.tipo_partido.descripcion.toLowerCase()).
        includes(this.filtro.toLowerCase()));
    }
    return this.partidos;
  }  

  abrirCalendario() {
    this.ocultarCalendario = false;
 
  }
  seleccionarFechaHora(evento: any) {
    this.fecha = evento.detail.value;
    console.log(this.fecha); 
  }  

  filtrar() {
    console.log(this.fecha);
  }

  unirme(partido_id: number){
    this.inscripcionService.crearInscripcionPartido(partido_id).subscribe(
      (data) => {
        this.mensajeExito()
        this.router.navigateByUrl('/home');
        //console.log(data);
      },
      (error: HttpErrorResponse) => {
        this.errorMensaje = error.error[0];
        this.mensajeError(this.errorMensaje)
        //console.log(error.error[0]);
      }
    );    
  }

  async mensajeExito() {
    const alert = await this.alertController.create({
      header: 'Te uniste al partido y ganaste 5 puntos',
      message: 'Ya podes verlo en "Mis partidos"',
      buttons: ['OK'],
    });
    await alert.present();
  }
  async mensajeError(error:string) {
    const alert = await this.alertController.create({
      header: error,
      //message: 'Intenta de nuevo más tarde.',
      buttons: ['OK'],
    });
    await alert.present();
  }

}

