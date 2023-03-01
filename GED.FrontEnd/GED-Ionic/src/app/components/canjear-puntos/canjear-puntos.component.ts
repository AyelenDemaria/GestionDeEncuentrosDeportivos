import { Component, OnInit } from '@angular/core';
import { Router} from '@angular/router';

@Component({
  selector: 'app-canjear-puntos',
  templateUrl: './canjear-puntos.component.html',
  styleUrls: ['./canjear-puntos.component.scss'],
})
export class CanjearPuntosComponent implements OnInit {

  deportes: any[] = ['Tenis', 'Futbol', 'Voley', 'Paddel'];
  canchas: any[] = ['Cancha SRL', 'Cancha Tito', 'Cancha 5'];
  puntos: number = 30;
    
  constructor(
    private router: Router,
  ) { }

  ngOnInit() {}


  
cancel() {
  this.router.navigateByUrl('home')
  }
}
