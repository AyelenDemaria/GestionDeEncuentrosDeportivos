import { Component, OnInit } from '@angular/core';
import { AlertController } from '@ionic/angular';
import { PartidoService } from 'src/app/services/partido.service';


@Component({
  selector: 'app-unirme',
  templateUrl: './unirme.component.html',
  styleUrls: ['./unirme.component.scss'],
})
export class UnirmeComponent implements OnInit {
  partidos: any[] = [
    {
      deporte: 'Voley',
      cantInscriptos: '8',
      fechaHora: '20-02-23 14hs',
      cantJugadores: '10',
      cancha: 'Alverdi 458',
      tipoPartido: 'Mixto',
    },

    {
      deporte: 'Futbol',
      cantInscriptos: '8',
      fechaHora: '15-03-23 15hs',
      cantJugadores: '10',
      cancha: 'Mitre 2067',
      tipoPartido: 'Mixto',
    },

    {
      deporte: 'Futbol',
      cantInscriptos: '2',
      fechaHora: '05-03-23',
      cantJugadores: '10',
      cancha: 'Mitre 2067',
      tipoPartido: 'Mixto',
    },
  ];

  deportes: any[] = ['Tenis', 'Futbol', 'Voley', 'Paddel'];
  canchas: any[] = ['Cancha SRL', 'Cancha Tito', 'Cancha 5']

  fecha: string = new Date().toISOString();
  ocultarCalendario = true;
  

  constructor(
    private partidoService: PartidoService,
    private alertController: AlertController,
  ) { }

  ngOnInit() {
    this.partidoService.getPartidos().subscribe(x => console.log(x), err => console.log(err))

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


}

