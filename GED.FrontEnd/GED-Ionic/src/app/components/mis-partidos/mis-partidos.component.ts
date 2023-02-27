import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-mis-partidos',
  templateUrl: './mis-partidos.component.html',
  styleUrls: ['./mis-partidos.component.scss'],
})
export class MisPartidosComponent implements OnInit {
  partidos: any[] = [
    {deporte: 'Voley',
     cantInscriptos:'8',
     fechaHora: '20-02-23 14hs',
     cantJugadores:'10',
     cancha: 'Alverdi 458',
     tipoPartido:'Mixto',
     },
  
     {deporte: 'Futbol',
     cantInscriptos:'8',
     fechaHora: '15-03-23 15hs',
     cantJugadores:'10',
     cancha: 'Mitre 2067',
     tipoPartido:'Mixto',
     },
  
     {deporte: 'Futbol',
     cantInscriptos:'10',
     fechaHora: '05-03-23',
     cantJugadores:'10',
     cancha: 'Mitre 2067',
     tipoPartido:'Mixto',
     },
  ] ;


  constructor() { }

  ngOnInit() {}

}
