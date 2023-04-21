import { Component } from '@angular/core';
import { AlertController} from '@ionic/angular';
import { InscripcionService } from 'src/app/services/inscripcion.service';
import { PartidoService } from 'src/app/services/partido.service';
import { HttpErrorResponse } from '@angular/common/http';
import { Router } from '@angular/router';
import { PopoverController } from '@ionic/angular';
import { InscriptosPopoverComponent } from '../inscriptos-popover/inscriptos-popover.component';

@Component({
  selector: 'app-unirme',
  templateUrl: './unirme.component.html',
  styleUrls: ['./unirme.component.scss'],
})
export class UnirmeComponent {
  partidos: any[] = []
  filtro = ''; 
  errorMensaje:string

  fecha: string = new Date().toISOString();
  ocultarCalendario = true;
  inscriptos: any[];
  

  constructor(
    private partidoService: PartidoService,
    private inscripcionService: InscripcionService,
    private alertController: AlertController,
    private router: Router,  
    private popoverController: PopoverController,  
    ) { }

    ionViewDidEnter() {
    this.partidoService.getPartidos().subscribe((data: any[]) => {
      this.partidos = data;
      console.log(this.partidos);
    },
    (error) => {
      console.log(error);
    })
    this.getCantInscriptos()
   } 

   get filteredPartidos() {
    if (this.filtro != "") {
      return this.partidos.filter(x => (x.fecha_hora + x.cant_jugadores + x.cancha.cancha.deporte.descripcion.toLowerCase()
        + x.cancha.cancha.direccion.toLowerCase() + x.tipo_partido.descripcion.toLowerCase() + x.cancha.valor_uso + x.cancha.valor_referi).
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

  async mostrarInscriptos(idPartido: number) {
    const inscriptos = await this.inscripcionService.getInscriptos(idPartido).toPromise();
    const popover = await this.popoverController.create({
      component: InscriptosPopoverComponent,
      componentProps: {
        inscriptos: inscriptos
      }
    });
    await popover.present();
  }

  async getCantInscriptos() {
    this.partidos = await  this.partidoService.getPartidos().toPromise();
    for (let i = 0; i < this.partidos.length; i++) {
      const idPartido = this.partidos[i].id;
      const inscriptos = await this.inscripcionService.getInscriptos(idPartido).toPromise();
      const cantInscriptos = inscriptos.length;  
      this.partidos[i].cantInscriptos = cantInscriptos;
      this.partidos[i].inscriptos = inscriptos;
    }
  }





}