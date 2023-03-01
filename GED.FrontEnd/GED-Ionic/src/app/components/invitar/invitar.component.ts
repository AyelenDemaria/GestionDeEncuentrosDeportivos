import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-invitar',
  templateUrl: './invitar.component.html',
  styleUrls: ['./invitar.component.scss'],
})
export class InvitarComponent implements OnInit {

  jugadores: any[] = [
    {dni: '38654792',
     nombre: 'Marta Perez',
     sexo: 'Femenino',
     mail: 'marta@gmail.com',
     telefono:'3416985230',
     fechaNac: '15/03/95'
     },
  
     {dni: '35769841',
     nombre: 'Juan Navarro',
     sexo: 'Masculino',
     mail: 'juanava@gmail.com',
     telefono:'3415320147',
     fechaNac: '25/05/91'
     },
  
     {dni: '40589231',
     nombre: 'Renata Acuario',
     sexo: 'Femenino',
     mail: 'renacuario@gmail.com',
     telefono:'34156320148',
     fechaNac: '08/06/99'
     },
  ] ;

  constructor() { }

  ngOnInit() {}

}
