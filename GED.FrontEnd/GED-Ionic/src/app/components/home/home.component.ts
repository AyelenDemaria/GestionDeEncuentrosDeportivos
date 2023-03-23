import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';
import { UsuarioService } from 'src/app/services/usuario.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {

  puntos:number 

  constructor( 
    private authService: AuthService,
    private router: Router,
    private usuarioService: UsuarioService
  ) {}

  ngOnInit() {
   this.puntosUsuario()
  }

  cerrarSesion(){ 
    this.authService.logout().subscribe(
    (data) => {     
      console.log(data);
      this.router.navigateByUrl('/login');      
    },
    (error) => {
      console.log(error);
    }
  );      
  }

  puntosUsuario(){
    const body = {
      username: 'Julieta'
    }
    this.usuarioService.getPuntosUsuario(body).subscribe(res =>{
      this.puntos = res
    })    
  }
}
