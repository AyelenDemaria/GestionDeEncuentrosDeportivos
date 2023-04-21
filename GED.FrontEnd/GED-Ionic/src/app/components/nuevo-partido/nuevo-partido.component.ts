import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AlertController } from '@ionic/angular';
import { CanchaService } from 'src/app/services/cancha.service';
import { DeporteService } from 'src/app/services/deporte.service';
import { PartidoService } from 'src/app/services/partido.service';
import { HttpErrorResponse } from '@angular/common/http';
import { NgZone } from '@angular/core';
import { UsuarioService } from 'src/app/services/usuario.service';
import { DatePipe } from '@angular/common';




@Component({
  selector: 'app-nuevo-partido',
  templateUrl: './nuevo-partido.component.html',
  styleUrls: ['./nuevo-partido.component.scss'],
})
export class NuevoPartidoComponent  {


  deportes: any[];
  canchas: any[];
  tiposPartidos: any[];
  idDeporte: number;
  idCancha: number;

  fecha: string = new Date().toISOString();
  ocultarCalendario = true;
  errorMensaje: string;
  puntos: number;
  minFechaHora: string;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private canchaService: CanchaService,
    private partidoService: PartidoService,
    private deporteService: DeporteService,
    private alertController: AlertController,
    private ngZone: NgZone,
    private usuarioService: UsuarioService,
    private datePipe: DatePipe,
  
    ) {
      const fechaHoraActual = new Date().toISOString();
      this.minFechaHora = fechaHoraActual;
     }

  public form: FormGroup = this.fb.group({
    deporte: ['', Validators.required],
    tipoPart: ['', Validators.required],
    cancha: ['', Validators.required],
    fecha: ['', Validators.required],
    cantJugadores: ['', [Validators.required, Validators.min(1), Validators.max(20), Validators.pattern("^[0-9]*$")]],
  })


  ionViewDidEnter()  {
    this.getDeportes();
    this.getTiposPartidos();
    this.canchaService.getCanchas().subscribe(res => console.log(res))
    this.partidoService.getPartidos().subscribe(res => console.log(res))

  }

  abrirCalendario() {
    this.ocultarCalendario = false;
    const ahora = this.datePipe.transform(new Date(), 'yyyy-MM-ddTHH:mm:ss');
    this.minFechaHora = ahora;

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
    this.canchaService.getCanchasByDeporte(this.idDeporte).subscribe(canchas => {
      this.canchas = canchas;
    })
  }

  seleccionarDeporte(event: any) {
    this.idDeporte = Number(event.detail.value)
    this.getListadoCanchas()
  }


  seleccionarCancha(event: any) {
    this.idCancha = Number(event.detail.value.cancha.id)
    console.log(this.idCancha)
  }

  crearPartido() {
    const body = {
      fecha_hora: this.form.controls['fecha'].value,
      cant_jugadores: Number(this.form.controls['cantJugadores'].value),
      tipo_partido: Number(this.form.controls['tipoPart'].value),
      cancha: this.idCancha,
    }    
    this.partidoService.postPartido(body).subscribe(
      (data) => {
        this.mensajeExito() 
        this.usuarioService.getPuntosUsuario().subscribe((res) => {
          // Ejecuta la tarea fuera de la zona de Angular para actualizar los puntos
          this.ngZone.run(() => {
            this.puntos = res;
          });
        }); 
        this.router.navigateByUrl('/home');
        //console.log(data);
      },
      (error: HttpErrorResponse) => {
        this.errorMensaje = error.error[0];
        this.mensajeError(this.errorMensaje)
        //console.log(error.error[0]);
      }
    );        
  }

  async mensajeExito() {
    const alert = await this.alertController.create({
      header: 'Partido creado con éxito!',
      message: 'Podes verlo en "Mis partidos"',
      buttons: ['OK'],
    });
    await alert.present();
  }
  async mensajeError(error:string) {
    const alert = await this.alertController.create({
      header: error,
      //message: 'Intenta de nuevo más tarde.',
      buttons: ['OK'],
    });
    await alert.present();
  }


   cancel() {
        this.form.reset({
        deporte: '',
        tipoPart: '',
        cancha: '',
        fecha: '',
        cantJugadores: '',
      });
    
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
