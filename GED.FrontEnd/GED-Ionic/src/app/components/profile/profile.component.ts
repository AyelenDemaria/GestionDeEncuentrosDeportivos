import { Component, OnInit } from '@angular/core';
import { UsuarioService } from 'src/app/services/usuario.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
})
export class ProfileComponent implements OnInit {

  perfil: any;

  constructor(
    private usuarioService: UsuarioService,
  ) { }

  ngOnInit() {
     this.perfilUsuario()
  }

    perfilUsuario(){
      this.usuarioService.getDataUsuario().subscribe(
        (data: any[]) => {
          this.perfil = data;
          console.log(this.perfil);
        },
        (error) => {
          console.log(error);
        }
      );      
    }
}
