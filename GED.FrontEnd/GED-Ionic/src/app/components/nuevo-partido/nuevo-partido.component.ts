import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AlertController } from '@ionic/angular';
import { CanchaService } from 'src/app/services/cancha.service';
import { DeporteService } from 'src/app/services/deporte.service';
import { PartidoService } from 'src/app/services/partido.service';

@Component({
  selector: 'app-nuevo-partido',
  templateUrl: './nuevo-partido.component.html',
  styleUrls: ['./nuevo-partido.component.scss'],
})
export class NuevoPartidoComponent implements OnInit {


  deportes: any[];
  canchas: any[] = ['1', '2', '3'];
  tiposPartidos: any[] = ['1', '5'];
  idDeporte: number;
  idCancha: number

  fecha: string = new Date().toISOString();
  ocultarCalendario = true;


  constructor(private fb: FormBuilder,
    private router: Router,
    private canchaService: CanchaService,
    private partidoService: PartidoService,
    private deporteService: DeporteService,
    private alertController: AlertController,) { }

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
    this.canchaService.getCanchas().subscribe(res => console.log(res))
    this.partidoService.getPartidos().subscribe(res => console.log(res))

  }

  abrirCalendario() {
    this.ocultarCalendario = false;

  }
  seleccionarFechaHora(evento: any) {
    this.fecha = evento.detail.value;
    console.log(this.fecha);
  }

  getTiposPartidos() {
    this.partidoService.getTiposPartidos().subscribe(tipos =>
      this.tiposPartidos = tipos)
  }

  getDeportes() {
    this.deporteService.getDeportes().subscribe(deportes => {
      this.deportes = deportes;
    })
  }

  getListadoCanchas() {
    const body = {
      deporte_id: this.idDeporte
    }
    this.canchaService.getCanchasByDeporte(body).subscribe(res => console.log(res))
  }

  seleccionarDeporte(event: any) {
    this.idDeporte = Number(event.detail.value)
    this.getListadoCanchas()
  }


  seleccionarCancha(event: any) {
    this.idCancha = Number(event.detail.value)
  }

  crearPartido() {
    const body = {
      fecha_hora: this.form.controls['fecha'].value,
      cant_jugadores: Number(this.form.controls['cantJugadores'].value),
      tipo_partido: Number(this.form.controls['tipoPart'].value),
      cancha: this.idCancha,
    }
    console.log(body)
    //this.partidoService.postPartido(body).subscribe(res => console.log(res))
    this.mensaje()
  }


  async mensaje() {
    const alert = await this.alertController.create({
      header: 'Partido creado con éxito!',
      message: 'Podes verlo en "Mis partidos"',
      buttons: ['OK'],
    });
    await alert.present();
  }


  cancel() {
    this.router.navigateByUrl('home')
  }

  // get fecha() {
  //   return this.form.get('fecha');
  // }

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
