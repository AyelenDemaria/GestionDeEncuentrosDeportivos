import { Component, OnInit } from '@angular/core';
import { AlertController } from '@ionic/angular';
import { InscripcionService } from 'src/app/services/inscripcion.service';
import { PartidoService } from 'src/app/services/partido.service';


@Component({
  selector: 'app-unirme',
  templateUrl: './unirme.component.html',
  styleUrls: ['./unirme.component.scss'],
})
export class UnirmeComponent implements OnInit {
  partidos: any[] = []
  filtro = ''; 

  fecha: string = new Date().toISOString();
  ocultarCalendario = true;
  

  constructor(
    private partidoService: PartidoService,
    private inscripcionService: InscripcionService,
    private alertController: AlertController,
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

  async mensaje() {
    const alert = await this.alertController.create({
      header: 'Te uniste a un partido!',     
      message: 'Podes verlo en "Mis partidos"',
      buttons: ['OK'],
    });
    await alert.present();
  }

  filtrar() {
    console.log(this.fecha);
  }

  unirme(partido_id: number){
    this.inscripcionService.crearInscripcionPartido(partido_id).subscribe()
    
  }

}

