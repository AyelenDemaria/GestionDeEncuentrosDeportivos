import { Component, OnInit } from '@angular/core';
import { AlertController } from '@ionic/angular';

@Component({
  selector: 'app-mis-partidos',
  templateUrl: './mis-partidos.component.html',
  styleUrls: ['./mis-partidos.component.scss'],
})
export class MisPartidosComponent implements OnInit {

  filtro = '';

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
      cantInscriptos: '10',
      fechaHora: '05-03-23',
      cantJugadores: '10',
      cancha: 'Mitre 2067',
      tipoPartido: 'Mixto',
    },
  ];

  constructor(
    private alertController: AlertController,
  ) { }

  ngOnInit() { }

 
  get filteredPartidos() {
    if (this.filtro != "") {
      return this.partidos.filter(x => (x.deporte.toLowerCase() + x.cantInscriptos + x.fechaHora + x.cantJugadores
        + x.cancha.toLowerCase() + x.tipoPartido.toLowerCase()).
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
}
