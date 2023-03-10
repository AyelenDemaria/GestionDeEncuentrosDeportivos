import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { CanchaService } from 'src/app/services/cancha.service';
import { DeporteService } from 'src/app/services/deporte.service';
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

  deportes: any[];
  canchas: any[] = ['1', '2', '3'];
  tiposPartidos: any[] = ['1', '5'];
  idDeporte : number;
  idCancha: number

  constructor(private fb: FormBuilder,
    private router: Router,
    private canchaService: CanchaService,
    private partidoService: PartidoService,
    private deporteService: DeporteService) { }

  public form: FormGroup = this.fb.group({
    deporte: ['', Validators.required],
    tipoPart: ['', Validators.required],
    cancha: ['', Validators.required],
    fecha: ['', Validators.required],
    cantJugadores: ['', [Validators.required, Validators.min(1), Validators.max(20), Validators.pattern("^[0-9]*$")]],
  })


  ngOnInit() {
    this.getDeportes();
    this.getTiposPartidos();
  
  }

  getTiposPartidos(){
    this.partidoService.getTiposPartidos().subscribe(tipos => 
    this.tiposPartidos = tipos)
  }

  getDeportes() {
    this.deporteService.getDeportes().subscribe(deportes => {
      this.deportes = deportes;
    })
  }

  getListadoCanchas(id:number) {
    this.canchaService.getCanchasByDeporte(id).subscribe(res => console.log(res))
  }

  seleccionarDeporte(event: any) {
    this.idDeporte = Number(event.detail.value)
    this.getListadoCanchas(this.idDeporte)
  }

  
  seleccionarCancha(event: any) {
    this.idCancha = Number(event.detail.value)
  }

  crearPartido() {
    const body = {
      fecha_hora: new Date(this.form.controls['fecha'].value),
      cant_jugadores: Number(this.form.controls['cantJugadores'].value),
      tipo_partido: Number(this.form.controls['tipoPart'].value),
      cancha: this.idCancha,
    }
    this.partidoService.postPartido(body).subscribe(res => console.log(res))
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
