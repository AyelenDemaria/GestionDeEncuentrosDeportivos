import { Component, OnInit } from '@angular/core';
import { InvitacionService } from 'src/app/services/invitacion.service';

@Component({
  selector: 'app-invitaciones',
  templateUrl: './invitaciones.component.html',
  styleUrls: ['./invitaciones.component.scss'],
})
export class InvitacionesComponent implements OnInit {

  invitaciones: any[] = []

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

  rechazar(){
    

  }

  aceptar(){

  }

}







  
