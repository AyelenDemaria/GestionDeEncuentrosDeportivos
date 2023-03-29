import { Component, OnInit } from '@angular/core';
import { Router} from '@angular/router';
import { UsuarioService } from 'src/app/services/usuario.service';

@Component({
  selector: 'app-canjear-puntos',
  templateUrl: './canjear-puntos.component.html',
  styleUrls: ['./canjear-puntos.component.scss'],
})
export class CanjearPuntosComponent implements OnInit {

  deportes: any[] = ['Tenis', 'Futbol', 'Voley', 'Paddel'];
  canchas: any[] = ['Cancha SRL', 'Cancha Tito', 'Cancha 5'];
  puntos: number;
    
  constructor(
    private router: Router,
    private usuarioService: UsuarioService,
  ) { }

  ngOnInit() {
    this.puntosUsuario()
  }


  puntosUsuario() {
    this.usuarioService.getPuntosUsuario().subscribe(res => {
      this.puntos = res
    })
  }


  
cancel() {
  this.router.navigateByUrl('home')
  }
}
