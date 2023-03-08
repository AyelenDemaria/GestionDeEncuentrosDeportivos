import { Component, OnInit } from '@angular/core';
import { UsuarioService } from 'src/app/services/usuario.service';

@Component({
  selector: 'app-invitar',
  templateUrl: './invitar.component.html',
  styleUrls: ['./invitar.component.scss'],
})
export class InvitarComponent implements OnInit {

  jugadores:any[] = [];
  
  constructor(
    private usuarioService: UsuarioService,
  ) { }

  ngOnInit() {
    

    this.usuarioService.getUsuarios().subscribe(
      (data: any[]) => {
        this.jugadores = data;
        console.log(this.jugadores);
      },
      (error) => {
        console.log(error);
      }
    );



  } 
  

}
