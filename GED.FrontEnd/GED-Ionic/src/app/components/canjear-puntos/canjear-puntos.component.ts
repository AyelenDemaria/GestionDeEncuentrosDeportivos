import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UsuarioService } from 'src/app/services/usuario.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CanchaService } from 'src/app/services/cancha.service';
import { DeporteService } from 'src/app/services/deporte.service';
import { VoucherService } from 'src/app/services/voucher.service';
import { HttpErrorResponse } from '@angular/common/http';
import { AlertController } from '@ionic/angular';

@Component({
  selector: 'app-canjear-puntos',
  templateUrl: './canjear-puntos.component.html',
  styleUrls: ['./canjear-puntos.component.scss'],
})
export class CanjearPuntosComponent {

  deportes: any[];
  canchas: any[];
  tiposPartidos: any[];
  idDeporte: number;
  idCancha: number;
  puntos: number;
  errorMensaje: string

  constructor(
    private router: Router,
    private usuarioService: UsuarioService,
    private fb: FormBuilder,
    private canchaService: CanchaService,
    private deporteService: DeporteService,
    private voucherService: VoucherService,
    private alertController: AlertController,
  ) { }

  public form: FormGroup = this.fb.group({
    deporte: ['', Validators.required],
    cancha: ['', Validators.required],
  })

  ionViewDidEnter() {
    this.puntosUsuario()
    this.getDeportes();
  }


  puntosUsuario() {
    this.usuarioService.getPuntosUsuario().subscribe(res => {
      this.puntos = res
    })
  }

  cancel() {
    this.form.reset({
      deporte: '',
      cancha: '',     
    });
    this.router.navigateByUrl('home')
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
  }

  get deporte() {
    return this.form.get('deporte');
  }

  get cancha() {
    return this.form.get('cancha');
  }

  crearVoucher() {
    const body = {
      cancha_id: this.idCancha,
    }   
    this.voucherService.crearVoucher(body).subscribe(     
      (data) => {
        this.mensajeExito()
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
      header: 'Puntos canjeados!',
      message: 'Podes ver tu verlo en "Mis vouchers"',
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


}
