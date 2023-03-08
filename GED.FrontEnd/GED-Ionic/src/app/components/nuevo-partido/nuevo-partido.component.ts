import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router} from '@angular/router';
import { CanchaService} from 'src/app/services/cancha.service';
import { PartidoService } from 'src/app/services/partido.service';

@Component({
  selector: 'app-nuevo-partido',
  templateUrl: './nuevo-partido.component.html',
  styleUrls: ['./nuevo-partido.component.scss'],
})
export class NuevoPartidoComponent implements OnInit {

  // deportes: any[] = ['Tenis', 'Futbol', 'Voley', 'Paddel'];
  // canchas: any[] = ['Cancha SRL', 'Cancha Tito', 'Cancha 5'];
  // tipos: any[] = ['Femenino', 'Masculino', 'Mixto']

  deportes: any[] = ['1', '2'];
  canchas: any[] = ['1', '2', '3'];
  tipos: any[] = ['1', '5']

  constructor(private fb: FormBuilder, 
    private router: Router,
    private canchaService: CanchaService,
    private partidoService:PartidoService) { }  

public form: FormGroup = this.fb.group({
deporte: ['', Validators.required],
tipoPart:['', Validators.required],
cancha: ['', Validators.required],
fecha: ['', Validators.required],  
cantJugadores: ['', [Validators.required, Validators.min(1), Validators.max(20), Validators.pattern("^[0-9]*$")]],
})


ngOnInit() { 
// this.getListadoCanchas();
}

// getListadoCanchas(){
// this.canchaService.getCanchas().subscribe(res=>console.log(res))
// }

crearPartido(){
  const body = {
    fechaHora: this.form.controls['fecha'].value,
    cantJugadores:this.form.controls['cantJugadores'].value,
    tipoPartido: this.form.controls['tipoPart'].value,
    cancha: this.form.controls['cancha'].value,
  }
  this.partidoService.postPartido(body).subscribe(res=>console.log(res))
}


cancel() {
this.router.navigateByUrl('home')
}

get fecha() {
  return this.form.get('fecha');
}

get deporte() {
  return this.form.get('deporte');
}

get tipoPart() {
  return this.form.get('tipoPart');
}

get cantJugadores() {
  return this.form.get('cantJugadores');
}

get cancha() {
  return this.form.get('cancha');
}
}
