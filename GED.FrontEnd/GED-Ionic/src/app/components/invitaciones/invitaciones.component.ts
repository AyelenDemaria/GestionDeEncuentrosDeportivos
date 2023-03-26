import { Component, OnInit } from '@angular/core';
import { InvitacionService } from 'src/app/services/invitacion.service';

@Component({
  selector: 'app-invitaciones',
  templateUrl: './invitaciones.component.html',
  styleUrls: ['./invitaciones.component.scss'],
})
export class InvitacionesComponent implements OnInit {

  invitaciones: any[] = []
  //   {deporte: 'Voley',
  //    cantInscriptos:'8',
  //    fechaHora: '20-02-23 14hs',
  //    cantJugadores:'10',
  //    cancha: 'Alverdi 458',
  //    tipoPartido:'Mixto',
  //    invitadoPor: 'Juan Perez' },
  
  //    {deporte: 'Futbol',
  //    cantInscriptos:'8',
  //    fechaHora: '15-03-23 15hs',
  //    cantJugadores:'10',
  //    cancha: 'Mitre 2067',
  //    tipoPartido:'Mixto',
  //    invitadoPor: 'Pablo Lopez' },
  
  //    {deporte: 'Futbol',
  //    cantInscriptos:'10',
  //    fechaHora: '05-03-23',
  //    cantJugadores:'10',
  //    cancha: 'Mitre 2067',
  //    tipoPartido:'Mixto',
  //    invitadoPor: 'Pablo Lopez' },
  // ] ;

  constructor(
    private invitacionesService: InvitacionService
  ) { }

  ngOnInit() {
    this.invitacionesService.invitacionesUser().subscribe(
      (data: any[]) => {
        this.invitaciones = data;
        console.log(this.invitaciones);
      },
      (error: any) => {
        console.log(error);
      }
    );    
    
  }

}







  
